"""Tests for score_item function."""
import unittest
from datetime import datetime, timezone, timedelta
from src.scoring.score_item import score_item, apply_source_weighting


class TestApplySourceWeighting(unittest.TestCase):
    """Tests for apply_source_weighting function."""
    
    def test_empty_source_weights(self):
        """Test with no source weights returns default 0.5."""
        result = apply_source_weighting("example.com", {})
        self.assertEqual(result, 0.5)
    
    def test_matching_source(self):
        """Test matching source returns correct weight."""
        source_weights = {"example.com": 0.8, "other.com": 0.3}
        result = apply_source_weighting("example.com/feed", source_weights)
        self.assertEqual(result, 0.8)
    
    def test_case_insensitive_matching(self):
        """Test case insensitive matching."""
        source_weights = {"Example.Com": 0.9}
        result = apply_source_weighting("example.com/feed", source_weights)
        self.assertEqual(result, 0.9)
    
    def test_no_match_returns_default(self):
        """Test no match returns default 0.5."""
        source_weights = {"example.com": 0.8}
        result = apply_source_weighting("other.com", source_weights)
        self.assertEqual(result, 0.5)
    
    def test_partial_match(self):
        """Test partial string matching."""
        source_weights = {"gov": 0.95}
        result = apply_source_weighting("sam.gov/feed", source_weights)
        self.assertEqual(result, 0.95)


class TestScoreItem(unittest.TestCase):
    """Tests for score_item function."""
    
    def setUp(self):
        """Set up common test data."""
        self.now = datetime.now(timezone.utc)
        self.base_config = {
            "keywords": ["software", "development"],
            "min_budget": 10000,
            "days_window": 30,
            "weights": {
                "keyword": 0.45,
                "budget": 0.25,
                "recency": 0.2,
                "source": 0.1
            },
            "source_weights": {
                "sam.gov": 0.9,
                "grants.gov": 0.8
            }
        }
        self.base_item = {
            "title": "Software Development Project",
            "summary": "Looking for software development services",
            "published_utc": self.now - timedelta(days=5),
            "budget_value": 50000,
            "source": "sam.gov"
        }
    
    def test_perfect_score(self):
        """Test item with all optimal values."""
        item = {
            "title": "Software Development Project",
            "summary": "Looking for software development services",
            "published_utc": self.now,
            "budget_value": 100000,
            "source": "sam.gov"
        }
        score = score_item(item, self.base_config)
        self.assertGreater(score, 0.8)
        self.assertLessEqual(score, 1.0)
    
    def test_keyword_matching(self):
        """Test keyword score calculation."""
        # Item with all keywords
        item = dict(self.base_item)
        item["title"] = "Software Development"
        item["summary"] = "Project description"
        score1 = score_item(item, self.base_config)
        
        # Item with one keyword
        item2 = dict(self.base_item)
        item2["title"] = "Software Project"
        item2["summary"] = "No matching words here"
        score2 = score_item(item2, self.base_config)
        
        # Item with no keywords
        item3 = dict(self.base_item)
        item3["title"] = "Hardware"
        item3["summary"] = "Equipment purchase"
        score3 = score_item(item3, self.base_config)
        
        self.assertGreater(score1, score2)
        self.assertGreater(score2, score3)
    
    def test_budget_scoring(self):
        """Test budget score calculation."""
        config = dict(self.base_config)
        config["min_budget"] = 10000
        
        # Budget at min
        item1 = dict(self.base_item)
        item1["budget_value"] = 10000
        score1 = score_item(item1, config)
        
        # Budget at max (10x min)
        item2 = dict(self.base_item)
        item2["budget_value"] = 100000
        score2 = score_item(item2, config)
        
        # Budget above max (should clamp to 1.0)
        item3 = dict(self.base_item)
        item3["budget_value"] = 200000
        score3 = score_item(item3, config)
        
        self.assertLess(score1, score2)
        self.assertAlmostEqual(score2, score3, places=5)
    
    def test_no_budget_value(self):
        """Test item with no budget value."""
        item = dict(self.base_item)
        item["budget_value"] = None
        score = score_item(item, self.base_config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_recency_scoring(self):
        """Test recency score calculation."""
        config = dict(self.base_config)
        config["days_window"] = 30
        
        # Very recent
        item1 = dict(self.base_item)
        item1["published_utc"] = self.now - timedelta(days=1)
        score1 = score_item(item1, config)
        
        # Mid-range
        item2 = dict(self.base_item)
        item2["published_utc"] = self.now - timedelta(days=15)
        score2 = score_item(item2, config)
        
        # Old (at edge of window)
        item3 = dict(self.base_item)
        item3["published_utc"] = self.now - timedelta(days=29)
        score3 = score_item(item3, config)
        
        # Outside window
        item4 = dict(self.base_item)
        item4["published_utc"] = self.now - timedelta(days=35)
        score4 = score_item(item4, config)
        
        self.assertGreater(score1, score2)
        self.assertGreater(score2, score3)
        # score4 should have recency_score = 0
    
    def test_no_published_date(self):
        """Test item with no published date."""
        item = dict(self.base_item)
        item["published_utc"] = None
        score = score_item(item, self.base_config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_source_weighting(self):
        """Test source weighting impact."""
        config = dict(self.base_config)
        
        # High-weight source
        item1 = dict(self.base_item)
        item1["source"] = "sam.gov"
        score1 = score_item(item1, config)
        
        # Medium-weight source
        item2 = dict(self.base_item)
        item2["source"] = "grants.gov"
        score2 = score_item(item2, config)
        
        # Unknown source (should get default)
        item3 = dict(self.base_item)
        item3["source"] = "unknown.com"
        score3 = score_item(item3, config)
        
        self.assertGreater(score1, score2)

    def test_region_relevance_scoring(self):
        """Test semantic region matching increases score for configured groups."""
        config = dict(self.base_config)
        config["regions"] = [
            "East Asia and Pacific (EAP): Includes China, Indonesia, Pacific Island States, and Philippines."
        ]

        item1 = dict(self.base_item)
        item1["summary"] = "Program support across Indonesia ministries"
        score1 = score_item(item1, config)

        item2 = dict(self.base_item)
        item2["summary"] = "Program support across Germany ministries"
        score2 = score_item(item2, config)

        self.assertGreater(score1, score2)
        self.assertEqual(item1.get("matched_regions"), ["EAP"])

    def test_region_weight_override(self):
        """Test custom region weight in config.weights is applied."""
        config = dict(self.base_config)
        config["regions"] = [
            "South Asia (SAR): Includes India, Pakistan, Bangladesh, and Afghanistan."
        ]
        config["weights"] = {
            "keyword": 0.3,
            "budget": 0.25,
            "recency": 0.2,
            "source": 0.1,
            "region": 0.15,
        }

        item1 = dict(self.base_item)
        item1["summary"] = "Program expansion in India and Bangladesh"
        score1 = score_item(item1, config)

        item2 = dict(self.base_item)
        item2["summary"] = "Program expansion in Canada and Mexico"
        score2 = score_item(item2, config)

        self.assertGreater(score1, score2)
        self.assertEqual(item1.get("matched_regions"), ["SAR"])
    
    def test_custom_weights(self):
        """Test with custom weight configuration."""
        config = dict(self.base_config)
        config["weights"] = {
            "keyword": 0.7,
            "budget": 0.1,
            "recency": 0.1,
            "source": 0.1
        }
        score = score_item(self.base_item, config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_zero_total_weight(self):
        """Test with zero total weight."""
        config = dict(self.base_config)
        config["weights"] = {
            "keyword": 0,
            "budget": 0,
            "recency": 0,
            "source": 0
        }
        score = score_item(self.base_item, config)
        self.assertEqual(score, 0.0)
    
    def test_missing_config_values(self):
        """Test with minimal config using defaults."""
        config = {}
        item = {
            "title": "Test",
            "summary": "Description",
            "published_utc": self.now,
            "budget_value": 5000,
            "source": "test.com"
        }
        score = score_item(item, config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_empty_keywords(self):
        """Test with empty keywords list."""
        config = dict(self.base_config)
        config["keywords"] = []
        score = score_item(self.base_item, config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_min_budget_zero(self):
        """Test budget scoring when min_budget is 0."""
        config = dict(self.base_config)
        config["min_budget"] = 0
        item = dict(self.base_item)
        item["budget_value"] = 5000
        score = score_item(item, config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_min_budget_none(self):
        """Test budget scoring when min_budget is None."""
        config = dict(self.base_config)
        config["min_budget"] = None
        item = dict(self.base_item)
        item["budget_value"] = 5000
        score = score_item(item, config)
        self.assertIsInstance(score, float)
        self.assertGreaterEqual(score, 0.0)
        self.assertLessEqual(score, 1.0)
    
    def test_case_insensitive_keywords(self):
        """Test that keyword matching is case insensitive."""
        config = dict(self.base_config)
        config["keywords"] = ["SOFTWARE", "DEVELOPMENT"]
        item = {
            "title": "software development",
            "summary": "lowercase text",
            "published_utc": self.now,
            "budget_value": 50000,
            "source": "test.com"
        }
        score = score_item(item, config)
        self.assertGreater(score, 0.0)
    
    def test_return_type_is_float(self):
        """Test that score_item always returns a float."""
        score = score_item(self.base_item, self.base_config)
        self.assertIsInstance(score, float)


if __name__ == "__main__":
    unittest.main()
