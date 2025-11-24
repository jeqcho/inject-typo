"""TypoGen: A Rule-Based Typographical Noise Generator.

This package introduces controlled, realistic typographical errors into text.
Error types and probabilities are based on empirical research by Conijn et al. (2019).
"""

from .core import generate_typos
from .keyboard import DEFAULT_ERROR_PROBS, KEY_ADJACENCY

__version__ = "0.1.0"
__all__ = ["generate_typos", "DEFAULT_ERROR_PROBS", "KEY_ADJACENCY"]
