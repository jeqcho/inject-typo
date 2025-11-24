"""Basic functionality tests for typogen."""

import pytest
from typogen import generate_typos, DEFAULT_ERROR_PROBS, KEY_ADJACENCY


class TestGenerateTypos:
    """Tests for the generate_typos function."""

    def test_empty_string_returns_empty(self):
        """Empty input should return empty output."""
        result = generate_typos("", 0.5, seed=42)
        assert result == ""

    def test_zero_strength_returns_original(self):
        """Strength of 0 should return unchanged text."""
        text = "Hello, World!"
        result = generate_typos(text, 0.0, seed=42)
        assert result == text

    def test_returns_string(self):
        """Output should be a string."""
        result = generate_typos("test", 0.5, seed=42)
        assert isinstance(result, str)

    def test_modifies_text_with_high_strength(self):
        """High strength should modify the text."""
        text = "Hello, World!"
        result = generate_typos(text, 1.0, seed=42)
        assert result != text

    def test_preserves_approximate_length(self):
        """Output length should be roughly similar to input."""
        text = "The quick brown fox jumps over the lazy dog."
        result = generate_typos(text, 0.5, seed=42)
        # Length can vary due to insertions/deletions but shouldn't be wildly different
        assert len(result) > len(text) * 0.5
        assert len(result) < len(text) * 2


class TestInputValidation:
    """Tests for input validation."""

    def test_invalid_text_type_raises_error(self):
        """Non-string text should raise TypeError."""
        with pytest.raises(TypeError):
            generate_typos(123, 0.5)

    def test_strength_below_zero_raises_error(self):
        """Strength below 0 should raise ValueError."""
        with pytest.raises(ValueError):
            generate_typos("test", -0.1)

    def test_strength_above_one_raises_error(self):
        """Strength above 1 should raise ValueError."""
        with pytest.raises(ValueError):
            generate_typos("test", 1.5)

    def test_invalid_seed_type_raises_error(self):
        """Non-int seed should raise TypeError."""
        with pytest.raises(TypeError):
            generate_typos("test", 0.5, seed="invalid")

    def test_none_seed_is_valid(self):
        """None seed should be accepted."""
        result = generate_typos("test", 0.5, seed=None)
        assert isinstance(result, str)


class TestKeyboardAdjacency:
    """Tests for keyboard adjacency behavior."""

    def test_substitution_uses_adjacent_keys(self):
        """Substitution should use adjacent keys from the map."""
        # Use a seed that we know produces substitution
        # Test multiple times with different seeds to find substitutions
        found_adjacent = False
        for seed in range(100):
            result = generate_typos("a", 1.0, seed=seed)
            if len(result) == 1 and result != "a":
                # Check if the result is an adjacent key
                if result.lower() in KEY_ADJACENCY.get("a", []):
                    found_adjacent = True
                    break
        assert found_adjacent, "Substitution should produce adjacent keys"

    def test_case_preservation(self):
        """Case should be preserved in substitutions."""
        # Test uppercase
        found_upper = False
        for seed in range(100):
            result = generate_typos("A", 1.0, seed=seed)
            if len(result) == 1 and result.isupper():
                found_upper = True
                break
        assert found_upper, "Uppercase should be preserved"


class TestExports:
    """Tests for package exports."""

    def test_default_error_probs_exported(self):
        """DEFAULT_ERROR_PROBS should be accessible."""
        assert isinstance(DEFAULT_ERROR_PROBS, dict)
        assert "substitution" in DEFAULT_ERROR_PROBS
        assert "deletion" in DEFAULT_ERROR_PROBS
        assert "insertion" in DEFAULT_ERROR_PROBS
        assert "transposition" in DEFAULT_ERROR_PROBS

    def test_key_adjacency_exported(self):
        """KEY_ADJACENCY should be accessible."""
        assert isinstance(KEY_ADJACENCY, dict)
        assert "a" in KEY_ADJACENCY
        assert isinstance(KEY_ADJACENCY["a"], list)
