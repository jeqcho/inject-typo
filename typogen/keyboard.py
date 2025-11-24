"""QWERTY keyboard adjacency maps and constants."""

# QWERTY keyboard adjacency map
# Each key maps to its physically adjacent keys on a standard QWERTY keyboard
KEY_ADJACENCY = {
    # Top row
    "q": ["w", "a", "s"],
    "w": ["q", "e", "a", "s", "d"],
    "e": ["w", "r", "s", "d", "f"],
    "r": ["e", "t", "d", "f", "g"],
    "t": ["r", "y", "f", "g", "h"],
    "y": ["t", "u", "g", "h", "j"],
    "u": ["y", "i", "h", "j", "k"],
    "i": ["u", "o", "j", "k", "l"],
    "o": ["i", "p", "k", "l"],
    "p": ["o", "l"],
    # Middle row
    "a": ["q", "w", "s", "z"],
    "s": ["q", "w", "e", "a", "d", "z", "x"],
    "d": ["w", "e", "r", "s", "f", "x", "c"],
    "f": ["e", "r", "t", "d", "g", "c", "v"],
    "g": ["r", "t", "y", "f", "h", "v", "b"],
    "h": ["t", "y", "u", "g", "j", "b", "n"],
    "j": ["y", "u", "i", "h", "k", "n", "m"],
    "k": ["u", "i", "o", "j", "l", "m"],
    "l": ["i", "o", "p", "k"],
    # Bottom row
    "z": ["a", "s", "x"],
    "x": ["s", "d", "z", "c"],
    "c": ["d", "f", "x", "v"],
    "v": ["f", "g", "c", "b"],
    "b": ["g", "h", "v", "n"],
    "n": ["h", "j", "b", "m"],
    "m": ["j", "k", "n"],
}

# Default error type probabilities based on empirical distribution
# (Conijn et al., 2019)
DEFAULT_ERROR_PROBS = {
    "substitution": 0.57,
    "insertion": 0.18,
    "transposition": 0.13,
    "deletion": 0.11,
}
