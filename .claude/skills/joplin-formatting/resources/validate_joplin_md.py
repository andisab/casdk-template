#!/usr/bin/env python3
"""
Joplin Markdown Formatting Validator
=====================================
Checks a markdown file against joplin-formatting rules and reports violations.

Usage:
    python validate_joplin_md.py <file.md>
    python validate_joplin_md.py <file.md> --fix  # auto-fix what's possible

Exit codes:
    0 = no violations
    1 = violations found (printed to stdout as structured report)

Checked rules:
    1. --- only after h3 (never after h1, h2, h4, h5, h6)
    2. Two blank lines before h2, one before h3-h6, zero after any heading
    3. >[toc] present at document start for long documents (>80 lines)
    4. No unescaped +/- in advantages/disadvantages sections
    5. Heading hierarchy (no jumps like h2 → h5)
    6. Code blocks have language tags
    7. No duplicate h1
    8. Content starts immediately after heading (no blank line)
"""

import re
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class Violation:
    line: int
    rule: str
    severity: str  # "error" | "warning"
    message: str
    fixable: bool = False


@dataclass
class ValidationResult:
    violations: list[Violation] = field(default_factory=list)
    stats: dict = field(default_factory=dict)

    @property
    def passed(self) -> bool:
        return not any(v.severity == "error" for v in self.violations)

    def summary(self) -> str:
        errors = sum(1 for v in self.violations if v.severity == "error")
        warnings = sum(1 for v in self.violations if v.severity == "warning")
        lines = []
        if not self.violations:
            lines.append("✅ All checks passed.")
        else:
            lines.append(f"{'❌' if errors else '⚠️'} {errors} error(s), {warnings} warning(s)\n")
            for v in self.violations:
                icon = "❌" if v.severity == "error" else "⚠️"
                fix = " [fixable]" if v.fixable else ""
                lines.append(f"  {icon} Line {v.line}: [{v.rule}] {v.message}{fix}")
        return "\n".join(lines)


# --- Heading utilities ---

HEADING_RE = re.compile(r"^(#{1,6})\s+(.*)$")
HR_RE = re.compile(r"^---\s*$")
TOC_RE = re.compile(r"^>\[toc\]\s*$", re.IGNORECASE)
CODE_FENCE_RE = re.compile(r"^```(\w*)")
UNESCAPED_PLUS_RE = re.compile(r"^\+\s")
UNESCAPED_MINUS_RE = re.compile(r"^-\s")
ESCAPED_PLUS_RE = re.compile(r"^\\\+\s")
ESCAPED_MINUS_RE = re.compile(r"^\\-\s")


def heading_level(line: str) -> int | None:
    """Return heading level (1-6) or None."""
    m = HEADING_RE.match(line)
    return len(m.group(1)) if m else None


def is_blank(line: str) -> bool:
    return line.strip() == ""


def count_preceding_blanks(lines: list[str], idx: int) -> int:
    """Count blank lines immediately before lines[idx]."""
    count = 0
    i = idx - 1
    while i >= 0 and is_blank(lines[i]):
        count += 1
        i -= 1
    return count


def validate(text: str, filename: str = "<input>") -> ValidationResult:
    result = ValidationResult()
    lines = text.split("\n")
    n = len(lines)

    result.stats["total_lines"] = n
    result.stats["filename"] = filename

    # Track state
    in_code_block = False
    h1_count = 0
    last_heading_level = 0
    last_heading_line = 0
    in_advantages_section = False  # heuristic: after "Advantages" or "Disadvantages" text

    # --- Rule 4: >[toc] for long documents ---
    has_toc = any(TOC_RE.match(line.strip()) for line in lines[:5])
    if n > 80 and not has_toc:
        result.violations.append(Violation(
            line=1,
            rule="toc-missing",
            severity="error",
            message="Document is >80 lines but missing >[toc] at start.",
            fixable=True,
        ))

    for i, raw_line in enumerate(lines):
        lineno = i + 1
        line = raw_line.rstrip()

        # Track code fences
        fence_match = CODE_FENCE_RE.match(line)
        if fence_match:
            if in_code_block:
                in_code_block = False
                continue
            else:
                in_code_block = True
                # --- Rule 6: code blocks need language tags ---
                lang = fence_match.group(1)
                if not lang:
                    result.violations.append(Violation(
                        line=lineno,
                        rule="code-no-lang",
                        severity="warning",
                        message="Code fence missing language tag (e.g., ```python).",
                        fixable=False,
                    ))
                continue

        if in_code_block:
            continue

        hlevel = heading_level(line)

        # --- Heading-related rules ---
        if hlevel is not None:
            # Rule 7: no duplicate h1
            if hlevel == 1:
                h1_count += 1
                if h1_count > 1:
                    result.violations.append(Violation(
                        line=lineno,
                        rule="duplicate-h1",
                        severity="error",
                        message="Multiple h1 headings found. Joplin uses note title as h1.",
                        fixable=False,
                    ))

            # Rule 5: heading hierarchy (no jumps > 1 level)
            if last_heading_level > 0 and hlevel > last_heading_level + 1:
                result.violations.append(Violation(
                    line=lineno,
                    rule="heading-jump",
                    severity="warning",
                    message=f"Heading jumps from h{last_heading_level} to h{hlevel} (skips h{last_heading_level + 1}).",
                    fixable=False,
                ))

            # Rule 2: spacing BEFORE headings
            preceding_blanks = count_preceding_blanks(lines, i)
            if hlevel == 2 and i > 0:
                # First h2 after >[toc] gets zero blank lines
                is_first_h2_after_toc = has_toc and not any(
                    heading_level(lines[j]) == 2
                    for j in range(i)
                    if not is_blank(lines[j])
                )
                expected = 0 if is_first_h2_after_toc else 2
                if preceding_blanks != expected:
                    result.violations.append(Violation(
                        line=lineno,
                        rule="spacing-before-h2",
                        severity="error",
                        message=f"h2 needs {expected} blank line(s) before it, found {preceding_blanks}.",
                        fixable=True,
                    ))
            elif hlevel >= 3 and i > 0:
                if preceding_blanks < 1:
                    # Exception: if previous line is --- (h3 with separator pattern)
                    prev_nonblank = lines[i - 1].strip() if i > 0 else ""
                    if not HR_RE.match(prev_nonblank):
                        result.violations.append(Violation(
                            line=lineno,
                            rule=f"spacing-before-h{hlevel}",
                            severity="error",
                            message=f"h{hlevel} needs 1 blank line before it, found {preceding_blanks}.",
                            fixable=True,
                        ))

            # Rule 2: ZERO blank lines AFTER heading
            if i + 1 < n and is_blank(lines[i + 1]):
                # Exception: h3 followed by --- on next non-blank line is OK
                next_nonblank_idx = i + 1
                while next_nonblank_idx < n and is_blank(lines[next_nonblank_idx]):
                    next_nonblank_idx += 1
                if next_nonblank_idx < n and HR_RE.match(lines[next_nonblank_idx].strip()):
                    # h3 + blank + --- is still wrong; --- should be immediately after h3
                    if hlevel == 3:
                        result.violations.append(Violation(
                            line=lineno,
                            rule="spacing-after-heading",
                            severity="error",
                            message="Blank line between h3 and ---. The --- should follow immediately.",
                            fixable=True,
                        ))
                else:
                    # Heading-to-heading transition: if the next non-blank
                    # line is itself a heading, the blank line belongs to the
                    # next heading's "before" requirement — not a violation.
                    next_nb_idx = i + 1
                    while next_nb_idx < n and is_blank(lines[next_nb_idx]):
                        next_nb_idx += 1
                    next_is_heading = (
                        next_nb_idx < n
                        and heading_level(lines[next_nb_idx].rstrip()) is not None
                    )

                    if not next_is_heading:
                        result.violations.append(Violation(
                            line=lineno,
                            rule="spacing-after-heading",
                            severity="error",
                            message=f"Blank line after h{hlevel} heading. Content must start immediately.",
                            fixable=True,
                        ))

            last_heading_level = hlevel
            last_heading_line = lineno

        # --- Rule 1: --- only after h3 ---
        if HR_RE.match(line):
            # Find the nearest preceding heading
            prev_heading_level = None
            j = i - 1
            while j >= 0:
                pl = heading_level(lines[j])
                if pl is not None:
                    prev_heading_level = pl
                    break
                if not is_blank(lines[j]):
                    break  # non-heading, non-blank content before ---
                j -= 1

            if prev_heading_level is not None and prev_heading_level != 3:
                result.violations.append(Violation(
                    line=lineno,
                    rule="hr-wrong-heading",
                    severity="error",
                    message=f"--- found after h{prev_heading_level}. Only allowed after h3.",
                    fixable=True,
                ))
            elif prev_heading_level is None:
                # --- not preceded by any heading — could be a standalone separator
                result.violations.append(Violation(
                    line=lineno,
                    rule="hr-standalone",
                    severity="warning",
                    message="Standalone --- not preceded by a heading. Consider removing.",
                    fixable=False,
                ))

            # Check no blank line between --- and the content after it
            if i + 1 < n and is_blank(lines[i + 1]):
                result.violations.append(Violation(
                    line=lineno,
                    rule="spacing-after-hr",
                    severity="error",
                    message="Blank line after ---. Content must start immediately.",
                    fixable=True,
                ))

        # --- Rule 4 (advantages/disadvantages): detect section ---
        lower = line.lower()
        if "advantages" in lower or "disadvantages" in lower:
            in_advantages_section = True
        elif hlevel is not None:
            in_advantages_section = False

        if in_advantages_section:
            if UNESCAPED_PLUS_RE.match(line) and not ESCAPED_PLUS_RE.match(line):
                result.violations.append(Violation(
                    line=lineno,
                    rule="unescaped-plus",
                    severity="error",
                    message="Unescaped `+` in advantages section. Use `\\+`.",
                    fixable=True,
                ))
            if UNESCAPED_MINUS_RE.match(line) and not ESCAPED_MINUS_RE.match(line):
                # Be careful: `-` is also a list marker. Only flag if in adv/disadv context.
                result.violations.append(Violation(
                    line=lineno,
                    rule="unescaped-minus",
                    severity="error",
                    message="Unescaped `-` in disadvantages section. Use `\\-`.",
                    fixable=True,
                ))

    # --- Consistency check: if any h3 has ---, all should ---
    h3_lines = []
    h3_with_hr = []
    in_code = False
    for i, raw_line in enumerate(lines):
        if CODE_FENCE_RE.match(raw_line.rstrip()):
            in_code = not in_code
            continue
        if in_code:
            continue
        if heading_level(raw_line.rstrip()) == 3:
            h3_lines.append(i + 1)
            # Check if next non-blank line is ---
            j = i + 1
            while j < n and is_blank(lines[j]):
                j += 1
            if j < n and HR_RE.match(lines[j].strip()):
                h3_with_hr.append(i + 1)

    if h3_lines and h3_with_hr and len(h3_with_hr) != len(h3_lines):
        missing = set(h3_lines) - set(h3_with_hr)
        for ml in sorted(missing):
            result.violations.append(Violation(
                line=ml,
                rule="h3-hr-inconsistent",
                severity="warning",
                message="This h3 lacks --- but other h3s have it. Be consistent.",
                fixable=True,
            ))

    return result


def apply_fixes(text: str) -> str:
    """Best-effort auto-fix for fixable violations. Returns corrected text."""
    lines = text.split("\n")
    result_lines: list[str] = []
    n = len(lines)
    in_code_block = False
    i = 0

    # Ensure >[toc] at start for long docs
    has_toc = any(TOC_RE.match(line.strip()) for line in lines[:5])
    if n > 80 and not has_toc:
        result_lines.append(">[toc]")
        has_toc = True

    seen_h2 = False  # track first h2 after >[toc]

    while i < n:
        line = lines[i]
        stripped = line.rstrip()

        # Track code fences
        if CODE_FENCE_RE.match(stripped):
            in_code_block = not in_code_block
            result_lines.append(line)
            i += 1
            continue

        if in_code_block:
            result_lines.append(line)
            i += 1
            continue

        hlevel = heading_level(stripped)

        if hlevel is not None:
            # Fix spacing before heading
            # Remove trailing blanks from result_lines, then add correct count
            while result_lines and is_blank(result_lines[-1]):
                result_lines.pop()

            if result_lines:  # don't add blanks before the very first line
                # Don't add blank lines after --- (HR must have content immediately)
                last_nonblank = result_lines[-1].rstrip() if result_lines else ""
                if HR_RE.match(last_nonblank):
                    pass  # no spacing after ---
                elif hlevel == 2 and has_toc and not seen_h2:
                    pass  # no blank line between >[toc] and first h2
                else:
                    blank_count = 2 if hlevel == 2 else 1
                    for _ in range(blank_count):
                        result_lines.append("")

            if hlevel == 2:
                seen_h2 = True

            result_lines.append(line)
            i += 1

            # Skip any blank lines immediately after heading
            while i < n and is_blank(lines[i]):
                i += 1

            # For h3: ensure --- follows immediately, then content
            if hlevel == 3:
                if i < n and HR_RE.match(lines[i].strip()):
                    result_lines.append("---")
                    i += 1
                    # Skip blanks after ---
                    while i < n and is_blank(lines[i]):
                        i += 1
            continue

        # Fix --- after non-h3 headings: remove it
        if HR_RE.match(stripped):
            # Check if preceded by a heading that is NOT h3
            j = len(result_lines) - 1
            while j >= 0 and is_blank(result_lines[j]):
                j -= 1
            if j >= 0:
                prev_level = heading_level(result_lines[j].rstrip())
                if prev_level is not None and prev_level != 3:
                    i += 1  # skip this ---
                    # Also skip blank line after removed ---
                    while i < n and is_blank(lines[i]):
                        i += 1
                    continue

            result_lines.append(line)
            i += 1
            # Skip blanks after ---
            while i < n and is_blank(lines[i]):
                i += 1
            continue

        # Fix unescaped +/- in advantages sections
        if UNESCAPED_PLUS_RE.match(stripped) and not ESCAPED_PLUS_RE.match(stripped):
            result_lines.append("\\+" + stripped[1:])
            i += 1
            continue
        if UNESCAPED_MINUS_RE.match(stripped) and not ESCAPED_MINUS_RE.match(stripped):
            # Only fix if we're near "advantages"/"disadvantages" context
            # Simple heuristic: check last 20 lines for the keywords
            context = "\n".join(result_lines[-20:]).lower()
            if "advantage" in context or "disadvantage" in context:
                result_lines.append("\\-" + stripped[1:])
                i += 1
                continue

        result_lines.append(line)
        i += 1

    return "\n".join(result_lines)


def main():
    if len(sys.argv) < 2:
        print("Usage: python validate_joplin_md.py <file.md> [--fix]")
        sys.exit(1)

    filepath = Path(sys.argv[1])
    do_fix = "--fix" in sys.argv

    if not filepath.exists():
        print(f"Error: {filepath} not found.")
        sys.exit(1)

    text = filepath.read_text(encoding="utf-8")
    result = validate(text, str(filepath))
    print(result.summary())

    if do_fix and result.violations:
        fixed = apply_fixes(text)
        filepath.write_text(fixed, encoding="utf-8")

        # Re-validate to show remaining issues
        recheck = validate(fixed, str(filepath))
        print(f"\n--- After auto-fix ---")
        print(recheck.summary())

    sys.exit(0 if result.passed else 1)


if __name__ == "__main__":
    main()
