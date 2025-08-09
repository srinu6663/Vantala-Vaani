from typing import List, Dict, Any
import re

def parse_ingredients(text: str) -> List[Dict[str, str]]:
    """
    Parse ingredients from textarea input.
    Expected format: "ingredient name — quantity" or "ingredient name - quantity"
    One ingredient per line.

    Args:
        text: Multi-line string with ingredients

    Returns:
        List of dictionaries with 'name_te' and 'qty' keys
    """
    if not text or not text.strip():
        return []

    ingredients = []
    lines = text.strip().split('\n')

    for line in lines:
        line = line.strip()
        if not line:
            continue

        # Try to split on various separators
        # Priority: — (em dash), - (hyphen), , (comma)
        parts = None
        for separator in ['—', '-', ',']:
            if separator in line:
                parts = line.split(separator, 1)
                break

        if parts and len(parts) == 2:
            name = parts[0].strip()
            qty = parts[1].strip()
        else:
            # No separator found, treat entire line as ingredient name
            name = line
            qty = ""

        if name:  # Only add if we have a name
            ingredients.append({
                "name_te": name,
                "qty": qty
            })

    return ingredients

def validate_audio_file(file_bytes: bytes, filename: str, allowed_types: List[str], max_mb: int) -> tuple[bool, str]:
    """
    Validate audio file size and type.

    Args:
        file_bytes: File content as bytes
        filename: Original filename
        allowed_types: List of allowed file extensions
        max_mb: Maximum file size in MB

    Returns:
        Tuple of (is_valid, error_message)
    """
    if not file_bytes:
        return False, "No file content found"

    # Check file size
    size_mb = len(file_bytes) / (1024 * 1024)
    if size_mb > max_mb:
        return False, f"File size ({size_mb:.1f}MB) exceeds maximum allowed size ({max_mb}MB)"

    # Check file extension
    if '.' not in filename:
        return False, "File must have an extension"

    extension = filename.split('.')[-1].lower()
    if extension not in [t.lower() for t in allowed_types]:
        return False, f"File type '{extension}' not allowed. Allowed types: {', '.join(allowed_types)}"

    return True, ""

def format_file_size(size_bytes: int) -> str:
    """Format file size in human readable format"""
    if size_bytes < 1024:
        return f"{size_bytes} B"
    elif size_bytes < 1024 * 1024:
        return f"{size_bytes / 1024:.1f} KB"
    else:
        return f"{size_bytes / (1024 * 1024):.1f} MB"
