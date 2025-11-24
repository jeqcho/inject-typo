"""Utility functions for validation and randomness."""

import random


def validate_inputs(text: str, strength: float, seed: int | None) -> None:
    """Validate input parameters for generate_typos.

    Args:
        text: Input text string.
        strength: Error rate between 0.0 and 1.0.
        seed: Random seed (int or None).

    Raises:
        TypeError: If text is not a string or seed is not int/None.
        ValueError: If strength is not in [0.0, 1.0].
    """
    if not isinstance(text, str):
        raise TypeError(f"text must be str, got {type(text).__name__}")

    if not isinstance(strength, (int, float)):
        raise TypeError(f"strength must be a number, got {type(strength).__name__}")

    if not 0.0 <= strength <= 1.0:
        raise ValueError(f"strength must be in [0.0, 1.0], got {strength}")

    if seed is not None and not isinstance(seed, int):
        raise TypeError(f"seed must be int or None, got {type(seed).__name__}")


def create_rng(seed: int | None) -> random.Random:
    """Create a random number generator with optional seed.

    Args:
        seed: Random seed. If None, RNG is not seeded (nondeterministic).

    Returns:
        A Random instance.
    """
    rng = random.Random()
    if seed is not None:
        rng.seed(seed)
    return rng


def select_error_type(rng: random.Random, error_probs: dict[str, float]) -> str:
    """Select an error type based on probability distribution.

    Args:
        rng: Random number generator instance.
        error_probs: Dictionary mapping error types to probabilities.

    Returns:
        Selected error type name.
    """
    rand_val = rng.random()
    cumulative = 0.0

    for error_type, prob in error_probs.items():
        cumulative += prob
        if rand_val < cumulative:
            return error_type

    # Fallback to last error type (should not reach here with valid probs)
    return list(error_probs.keys())[-1]
