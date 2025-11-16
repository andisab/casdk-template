# Multi-line Input and Image Attachment Guide

## Overview

The research agent supports:
- **Multi-line prompts by default** - Type longer, formatted prompts across multiple lines
- **Image attachments** - Attach images for the agent to analyze
- **Shift+Enter for newlines** - Natural chat interface experience

## Usage

### Multi-line Mode (Default)

The agent always uses multi-line mode. Use keyboard shortcuts to control input:

```
You: Research the following topics about quantum computing: [Shift+Enter]
...
...  1. Recent hardware developments [Shift+Enter]
...  2. Commercial applications [Shift+Enter]
...  3. Timeline to quantum advantage [Shift+Enter]
...  [Shift+Enter]
...  Focus on 2024-2025 developments. [Enter to submit]
```

**Key Controls:**
- **Shift+Enter**: Insert a new line
- **Enter**: Submit your prompt
- **Ctrl+C**: Cancel input

### Attaching Images

Use the `@image:` prefix anywhere in your prompt:

```
You: Analyze this architecture diagram and suggest improvements: [Shift+Enter]
...  [Shift+Enter]
...  @image:~/Documents/system_architecture.png
  ✓ Image attached: ~/Documents/system_architecture.png
...  [Shift+Enter]
...  What are the potential bottlenecks? [Enter to submit]
```

**Supported image formats:**
- PNG (`.png`)
- JPEG (`.jpg`, `.jpeg`)
- GIF (`.gif`)
- WebP (`.webp`)

### Multiple Images

Attach multiple images in one prompt:

```
You: Compare these two UI mockups and suggest which is better: [Shift+Enter]
...  [Shift+Enter]
...  @image:~/mockup_v1.png
  ✓ Image attached: ~/mockup_v1.png
...  @image:~/mockup_v2.png
  ✓ Image attached: ~/mockup_v2.png
...  [Shift+Enter]
...  Consider usability and modern design trends. [Enter to submit]
```

## Examples

### Example 1: Long Research Request

```
You: I need a comprehensive research report on electric vehicles that covers: [Shift+Enter]
...  [Shift+Enter]
...  - Battery technology advancements in 2024-2025 [Shift+Enter]
...  - Major manufacturers (Tesla, Rivian, BYD, etc.) [Shift+Enter]
...  - Charging infrastructure developments [Shift+Enter]
...  - Market adoption rates by region [Shift+Enter]
...  - Government incentives and policies [Shift+Enter]
...  [Shift+Enter]
...  Please prioritize recent news and industry reports. [Enter to submit]
```

### Example 2: Image Analysis with Context

```
You: @image:~/Downloads/dashboard_screenshot.png
  ✓ Image attached: ~/Downloads/dashboard_screenshot.png
...  [Shift+Enter]
...  This is our current analytics dashboard. Please: [Shift+Enter]
...  1. Identify what metrics are being tracked [Shift+Enter]
...  2. Suggest additional KPIs we should monitor [Shift+Enter]
...  3. Recommend UI improvements for better readability [Enter to submit]
```

### Example 3: Code Review with Screenshot

```
You: I'm getting an error in my application: [Shift+Enter]
...  [Shift+Enter]
...  @image:~/Desktop/error_screenshot.png
  ✓ Image attached: ~/Desktop/error_screenshot.png
...  [Shift+Enter]
...  The error appears when users try to submit the form. [Shift+Enter]
...  Can you help diagnose what might be causing this? [Enter to submit]
```

## Tips

1. **Keyboard shortcuts:**
   - **Shift+Enter**: New line (continue typing)
   - **Enter**: Submit prompt (send to agent)
   - **Ctrl+C**: Cancel current input

2. **Path formats:**
   - Absolute: `/Users/andis/Documents/image.png`
   - Home directory: `~/Documents/image.png`
   - Relative: `./images/diagram.png`

3. **Image size:** Keep images under 5MB for best performance

4. **Natural workflow:** Type naturally with Shift+Enter for newlines, just like modern chat applications

## Implementation Details

- **Location:** `research_agent/utils/enhanced_input.py`
- **Integration:** Automatically used by `research_agent/agent.py`
- **Transcript logging:** Images are noted in session transcripts as `[N image(s) attached]`
- **Content blocks:** Images are base64-encoded and sent as proper Claude message content blocks

## Troubleshooting

**Image not found error:**
```
Warning: Image not found: /path/to/image.png
```
- Check the file path is correct
- Use absolute paths or `~/` for home directory
- Verify the file exists: `ls -la /path/to/image.png`

**Can't submit prompt:**
- Make sure you're pressing Enter (not Shift+Enter)
- Press Ctrl+C to cancel the current input and start over
