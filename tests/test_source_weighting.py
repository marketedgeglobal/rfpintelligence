"""Tests for apply_source_weighting function."""

import unittest
from rfpintelligence import apply_source_weighting


class TestApplySourceWeighting(unittest.TestCase):
    """Test cases for apply_source_weighting function."""

    def test_empty_config_returns_default(self):
        """Test that empty config returns 0.5."""
        result = apply_source_weighting("https://example.com", None)
        self.assertEqual(result, 0.5)
        
        result = apply_source_weighting("https://example.com", {})
        self.assertEqual(result, 0.5)

    def test_exact_url_match(self):
        """Test exact URL match in config."""
        config = {
            "https://example.com/page": 0.8,
            "default": 0.5
        }
        result = apply_source_weighting("https://example.com/page", config)
        self.assertEqual(result, 0.8)

    def test_domain_match(self):
        """Test domain matching in config."""
        config = {
            "example.com": 0.9,
            "default": 0.5
        }
        result = apply_source_weighting("https://example.com/some/path", config)
        self.assertEqual(result, 0.9)

    def test_domain_partial_match(self):
        """Test partial domain matching."""
        config = {
            "github.com": 0.7,
            "default": 0.5
        }
        result = apply_source_weighting("https://api.github.com/repos", config)
        self.assertEqual(result, 0.7)

    def test_default_fallback(self):
        """Test fallback to default value."""
        config = {
            "example.com": 0.9,
            "default": 0.3
        }
        result = apply_source_weighting("https://other.com/page", config)
        self.assertEqual(result, 0.3)

    def test_default_fallback_no_default_key(self):
        """Test fallback when no default key exists."""
        config = {
            "example.com": 0.9
        }
        result = apply_source_weighting("https://other.com/page", config)
        self.assertEqual(result, 0.5)

    def test_numeric_string_values(self):
        """Test that string numeric values are converted to float."""
        config = {
            "example.com": "0.8",
            "default": "0.5"
        }
        result = apply_source_weighting("https://example.com/page", config)
        self.assertEqual(result, 0.8)
        self.assertIsInstance(result, float)

    def test_malformed_url_handling(self):
        """Test handling of malformed URLs."""
        # When URL is malformed, empty domain may match config keys
        # This tests the actual behavior
        config = {
            "default": 0.4
        }
        result = apply_source_weighting("not a url", config)
        self.assertEqual(result, 0.4)

    def test_multiple_domain_keys(self):
        """Test with multiple domain keys, first match wins."""
        config = {
            "github.com": 0.7,
            "api.github.com": 0.9,
            "default": 0.5
        }
        # Since Python 3.7+, dict order is guaranteed, so github.com matches first
        result = apply_source_weighting("https://api.github.com/repos", config)
        self.assertEqual(result, 0.7)

    def test_exact_match_takes_precedence_over_domain(self):
        """Test that exact URL match takes precedence over domain match."""
        config = {
            "https://example.com/page": 0.95,
            "example.com": 0.7,
            "default": 0.5
        }
        result = apply_source_weighting("https://example.com/page", config)
        self.assertEqual(result, 0.95)

    def test_default_key_is_skipped_in_domain_matching(self):
        """Test that 'default' key is not used for domain matching."""
        config = {
            "default": 0.5
        }
        result = apply_source_weighting("https://default.com/page", config)
        # Should return 0.5 (the default value), not match "default" as a domain
        self.assertEqual(result, 0.5)


if __name__ == '__main__':
    unittest.main()
