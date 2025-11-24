"""Error type functions for typographical noise generation."""

import random
import string

from .keyboard import KEY_ADJACENCY


def get_adjacent_key(char: str, rng: random.Random) -> str:
    """Get a random adjacent key for the given character.

    Args:
        char: The character to find an adjacent key for.
        rng: Random number generator instance.

    Returns:
        An adjacent key if available, otherwise a random letter.
    """
    lower_char = char.lower()
    if lower_char in KEY_ADJACENCY:
        adjacent = rng.choice(KEY_ADJACENCY[lower_char])
        # Preserve case
        return adjacent.upper() if char.isupper() else adjacent
    else:
        # No adjacency list, return random letter preserving case
        new_char = rng.choice(string.ascii_lowercase)
        return new_char.upper() if char.isupper() else new_char


def apply_substitution(chars: list[str], index: int, rng: random.Random) -> None:
    """Replace character at index with an adjacent keyboard key.

    Args:
        chars: Mutable list of characters.
        index: Position to apply substitution.
        rng: Random number generator instance.
    """
    chars[index] = get_adjacent_key(chars[index], rng)


def apply_deletion(chars: list[str], index: int, rng: random.Random) -> None:
    """Remove character at index.

    Args:
        chars: Mutable list of characters.
        index: Position to delete.
        rng: Random number generator instance (unused but kept for consistent API).
    """
    # Only delete if string has at least 2 characters
    if len(chars) >= 2:
        chars.pop(index)


def apply_insertion(chars: list[str], index: int, rng: random.Random) -> None:
    """Insert an adjacent key after the character at index.

    Args:
        chars: Mutable list of characters.
        index: Position after which to insert.
        rng: Random number generator instance.
    """
    new_char = get_adjacent_key(chars[index], rng)
    chars.insert(index + 1, new_char)


def apply_transposition(chars: list[str], index: int, rng: random.Random) -> None:
    """Swap character at index with the next character.

    Args:
        chars: Mutable list of characters.
        index: Position to swap.
        rng: Random number generator instance (unused but kept for consistent API).
    """
    # If at last index, fallback to substitution
    if index >= len(chars) - 1:
        apply_substitution(chars, index, rng)
    else:
        chars[index], chars[index + 1] = chars[index + 1], chars[index]
