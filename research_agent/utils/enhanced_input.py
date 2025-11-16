"""Enhanced input handler for multi-line prompts and image attachments."""

import base64
from pathlib import Path
from typing import List, Dict, Any
from prompt_toolkit import PromptSession
from prompt_toolkit.key_binding import KeyBindings


async def get_multiline_input() -> tuple[str, List[str]]:
    """
    Get multi-line input from user with optional image attachments.

    Returns:
        tuple: (prompt_text, list_of_image_paths)

    Key bindings:
        - Meta+Enter or Escape,Enter: Insert newline
        - Enter: Submit prompt
        - Ctrl+C: Cancel input
    """
    # Create key bindings
    bindings = KeyBindings()

    @bindings.add('enter')
    def _(event):
        """Submit on Enter."""
        event.current_buffer.validate_and_handle()

    @bindings.add('escape', 'enter')  # Meta+Enter or Escape,Enter
    def _(event):
        """Insert newline on Meta+Enter."""
        event.current_buffer.insert_text('\n')

    try:
        # Get multi-line input using async session
        session = PromptSession(
            multiline=True,
            key_bindings=bindings,
            prompt_continuation="...  "
        )
        user_text = await session.prompt_async("\nYou: ")
    except (EOFError, KeyboardInterrupt):
        return "", []

    # Process the input for image attachments
    lines = user_text.split('\n')
    prompt_lines = []
    image_paths = []

    for line in lines:
        # Check for image attachment
        if line.strip().startswith("@image:"):
            image_path = line.strip()[7:].strip()  # Remove @image: prefix
            image_paths.append(image_path)
            print(f"  ✓ Image attached: {image_path}")
        else:
            prompt_lines.append(line)

    prompt_text = "\n".join(prompt_lines).strip()
    return prompt_text, image_paths


def create_message_content(prompt_text: str, image_paths: List[str]) -> List[Dict[str, Any]]:
    """
    Create message content blocks from text and images.

    Args:
        prompt_text: The text prompt
        image_paths: List of paths to image files

    Returns:
        List of content blocks for Claude SDK
    """
    content_blocks = []

    # Add images first
    for image_path in image_paths:
        path = Path(image_path).expanduser()

        if not path.exists():
            print(f"Warning: Image not found: {image_path}")
            continue

        # Determine media type from extension
        ext = path.suffix.lower()
        media_type_map = {
            '.png': 'image/png',
            '.jpg': 'image/jpeg',
            '.jpeg': 'image/jpeg',
            '.gif': 'image/gif',
            '.webp': 'image/webp'
        }

        media_type = media_type_map.get(ext, 'image/png')

        # Read and encode image
        with open(path, 'rb') as f:
            image_data = base64.standard_b64encode(f.read()).decode('utf-8')

        content_blocks.append({
            'type': 'image',
            'source': {
                'type': 'base64',
                'media_type': media_type,
                'data': image_data
            }
        })

    # Add text prompt
    if prompt_text:
        content_blocks.append({
            'type': 'text',
            'text': prompt_text
        })

    return content_blocks


async def get_user_input(multiline_mode: bool = True) -> tuple[str, List[Dict[str, Any]] | None]:
    """
    Get user input with multi-line and image support.

    Args:
        multiline_mode: If True, use multi-line input mode (default: True)

    Returns:
        tuple: (display_text, content_blocks or None)
        - If no images: (text, None) - can use simple string prompt
        - If images: (text, content_blocks) - use content blocks
    """
    # Multi-line mode (default)
    prompt_text, image_paths = await get_multiline_input()

    if not prompt_text:
        return "", None

    if not image_paths:
        return prompt_text, None

    content_blocks = create_message_content(prompt_text, image_paths)
    return prompt_text, content_blocks
