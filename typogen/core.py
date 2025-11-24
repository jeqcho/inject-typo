"""Core algorithm for typographical noise generation."""

from .keyboard import DEFAULT_ERROR_PROBS
from .errors import (
    apply_substitution,
    apply_deletion,
    apply_insertion,
    apply_transposition,
)
from .utils import validate_inputs, create_rng, select_error_type


# Map error type names to their functions
ERROR_FUNCTIONS = {
    "substitution": apply_substitution,
    "insertion": apply_insertion,
    "transposition": apply_transposition,
    "deletion": apply_deletion,
}


def generate_typos(
    text: str,
    strength: float,
    seed: int | None = None,
    error_probs: dict[str, float] | None = None,
) -> str:
    """Generate typographical errors in the input text.

    Args:
        text: The input text to introduce typos into.
        strength: Error rate in [0.0, 1.0]. Determines probability that each
            character undergoes a typo event.
        seed: Random seed for reproducibility. If None, results are
            nondeterministic.
        error_probs: Optional custom error type probabilities. If None,
            uses DEFAULT_ERROR_PROBS.

    Returns:
        Text with typographical errors introduced.

    Raises:
        TypeError: If text is not a string or seed is not int/None.
        ValueError: If strength is not in [0.0, 1.0].
    """
    validate_inputs(text, strength, seed)

    if not text or strength == 0.0:
        return text

    rng = create_rng(seed)
    probs = error_probs if error_probs is not None else DEFAULT_ERROR_PROBS

    chars = list(text)
    # Process from end to start to handle index shifts from deletions/insertions
    # We need to first determine which positions will be modified
    positions_to_modify = []
    for i in range(len(chars)):
        if rng.random() < strength:
            positions_to_modify.append(i)

    # Process in reverse order to handle index changes correctly
    for i in reversed(positions_to_modify):
        # Ensure index is still valid (could be affected by previous deletions)
        if i >= len(chars):
            continue

        error_type = select_error_type(rng, probs)
        error_func = ERROR_FUNCTIONS[error_type]
        error_func(chars, i, rng)

    return "".join(chars)
