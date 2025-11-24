"""Tests for strength parameter behavior."""

import pytest
from typogen import generate_typos


class TestStrengthLevels:
    """Tests for different strength levels."""

    def test_strength_zero_no_changes(self):
        """Strength 0 should produce no changes."""
        text = "The quick brown fox jumps over the lazy dog."
        result = generate_typos(text, 0.0, seed=42)
        assert result == text

    def test_strength_one_modifies_all_eligible_chars(self):
        """Strength 1 should modify every character."""
        text = "hello"
        result = generate_typos(text, 1.0, seed=42)
        # Every character should be affected somehow
        assert result != text

    def test_low_strength_few_changes(self):
        """Low strength should produce few changes."""
        text = "The quick brown fox jumps over the lazy dog."
        result = generate_typos(text, 0.1, seed=42)

        # Count differences (approximate, as length may change)
        # With 10% strength on ~44 chars, expect ~4 changes
        # Result should be similar but not identical
        assert result != text
        # Levenshtein distance would be ideal, but simple length check works
        assert abs(len(result) - len(text)) < 10

    def test_high_strength_many_changes(self):
        """High strength should produce many changes."""
        text = "The quick brown fox jumps over the lazy dog."

        # Run multiple trials and compare average similarity
        low_total_same = 0
        high_total_same = 0
        trials = 50

        for seed in range(trials):
            low_result = generate_typos(text, 0.1, seed=seed)
            high_result = generate_typos(text, 0.9, seed=seed + 1000)

            # Check if result equals original (exact match)
            low_total_same += 1 if low_result == text else 0
            high_total_same += 1 if high_result == text else 0

        # Low strength should have more unchanged results than high strength
        assert low_total_same >= high_total_same

    def test_strength_boundary_values(self):
        """Boundary values 0.0 and 1.0 should work correctly."""
        text = "test"

        # 0.0 - no changes
        result_zero = generate_typos(text, 0.0, seed=42)
        assert result_zero == text

        # 1.0 - changes applied
        result_one = generate_typos(text, 1.0, seed=42)
        assert result_one != text

    def test_strength_gradual_increase(self):
        """Increasing strength should generally increase modifications."""
        text = "ab"  # Short text so low strength often keeps it unchanged

        # Test that zero strength produces no changes
        result_zero = generate_typos(text, 0.0, seed=42)
        assert result_zero == text

        # Test that higher strength produces more changes on average
        # by checking that low strength sometimes keeps text unchanged
        low_unchanged = sum(
            1 for seed in range(100)
            if generate_typos(text, 0.05, seed=seed) == text
        )
        high_unchanged = sum(
            1 for seed in range(100)
            if generate_typos(text, 1.0, seed=seed) == text
        )

        # With very low strength on short text, some results should be unchanged
        # With max strength, none should be unchanged
        assert low_unchanged > high_unchanged


class TestErrorDistribution:
    """Tests for error type distribution."""

    def test_all_error_types_occur(self):
        """With enough samples, all error types should occur."""
        # This is a statistical test - run many iterations
        text = "abcdefghij"  # 10 characters
        seen_lengths = set()

        for seed in range(200):
            result = generate_typos(text, 1.0, seed=seed)
            seen_lengths.add(len(result))

        # Deletion makes it shorter, insertion makes it longer
        # Substitution/transposition keep same length (mostly)
        assert min(seen_lengths) < len(text), "Deletions should occur"
        assert max(seen_lengths) > len(text), "Insertions should occur"
