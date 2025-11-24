"""Reproducibility tests for typogen."""

import pytest
from typogen import generate_typos


class TestReproducibility:
    """Tests for deterministic behavior with seeds."""

    def test_same_seed_produces_same_output(self):
        """Same seed should produce identical results."""
        text = "hello"
        seed = 1234
        strength = 0.5

        result1 = generate_typos(text, strength, seed=seed)
        result2 = generate_typos(text, strength, seed=seed)

        assert result1 == result2

    def test_different_seeds_produce_different_output(self):
        """Different seeds should (usually) produce different results."""
        text = "The quick brown fox jumps over the lazy dog."
        strength = 0.5

        result1 = generate_typos(text, strength, seed=42)
        result2 = generate_typos(text, strength, seed=43)

        # With enough text and strength, different seeds should differ
        assert result1 != result2

    def test_reproducibility_with_longer_text(self):
        """Reproducibility should work with longer texts."""
        text = "The quick brown fox jumps over the lazy dog. " * 10
        seed = 9999
        strength = 0.3

        result1 = generate_typos(text, strength, seed=seed)
        result2 = generate_typos(text, strength, seed=seed)

        assert result1 == result2

    def test_reproducibility_with_max_strength(self):
        """Reproducibility should work at maximum strength."""
        text = "hello world"
        seed = 5678
        strength = 1.0

        result1 = generate_typos(text, strength, seed=seed)
        result2 = generate_typos(text, strength, seed=seed)

        assert result1 == result2

    def test_no_seed_is_nondeterministic(self):
        """Without seed, results should vary (probabilistically)."""
        text = "The quick brown fox jumps over the lazy dog."
        strength = 0.5

        # Run multiple times and check if we get different results
        results = set()
        for _ in range(10):
            result = generate_typos(text, strength, seed=None)
            results.add(result)

        # With high probability, we should get multiple different results
        # This test could theoretically fail, but probability is extremely low
        assert len(results) > 1, "Without seed, results should vary"

    def test_zero_seed_is_valid(self):
        """Seed of 0 should be a valid seed."""
        text = "hello"
        strength = 0.5

        result1 = generate_typos(text, strength, seed=0)
        result2 = generate_typos(text, strength, seed=0)

        assert result1 == result2
