#!/usr/bin/env python3
"""
Tests for RFP collection script functions.

Tests validate core functionality including:
- Link validation with mocking
- Budget extraction patterns
- Source weighting application
- Scoring logic
"""

import pytest
from unittest.mock import Mock, patch
from datetime import datetime, timezone
import sys
import os

# Add scripts directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'scripts'))

from collect_rfps import (
    validate_link,
    extract_budget,
    apply_source_weighting,
    calculate_score,
    score_keyword_match,
    score_budget,
    score_recency,
    filter_entries,
    generate_markdown_output,
    get_priority_band,
)


class TestValidateLink:
    """Tests for validate_link function."""
    
    @patch('collect_rfps.requests.head')
    def test_validate_link_success(self, mock_head):
        """Test validate_link with successful response."""
        # Mock successful response
        mock_response = Mock()
        mock_response.status_code = 200
        mock_head.return_value = mock_response
        
        result = validate_link('https://example.com')
        
        assert result is True
        mock_head.assert_called_once()
    
    @patch('collect_rfps.requests.head')
    def test_validate_link_not_found(self, mock_head):
        """Test validate_link with 404 error."""
        # Mock 404 response
        mock_response = Mock()
        mock_response.status_code = 404
        mock_head.return_value = mock_response
        
        result = validate_link('https://example.com/notfound')
        
        assert result is False
    
    @patch('collect_rfps.requests.head')
    def test_validate_link_server_error(self, mock_head):
        """Test validate_link with server error."""
        # Mock 500 response
        mock_response = Mock()
        mock_response.status_code = 500
        mock_head.return_value = mock_response
        
        result = validate_link('https://example.com/error')
        
        assert result is False
    
    @patch('collect_rfps.requests.head')
    def test_validate_link_timeout(self, mock_head):
        """Test validate_link with timeout exception."""
        import requests
        # Mock timeout exception
        mock_head.side_effect = requests.Timeout()
        
        result = validate_link('https://example.com/timeout')
        
        assert result is False
    
    @patch('collect_rfps.requests.head')
    def test_validate_link_connection_error(self, mock_head):
        """Test validate_link with connection error."""
        import requests
        # Mock connection error
        mock_head.side_effect = requests.ConnectionError()
        
        result = validate_link('https://example.com/error')
        
        assert result is False


class TestExtractBudget:
    """Tests for extract_budget function."""
    
    def test_extract_budget_simple_dollar(self):
        """Test extracting simple dollar amount."""
        text = "Budget: $100,000"
        result = extract_budget(text)
        assert result == 100000.0
    
    def test_extract_budget_with_million(self):
        """Test extracting amount with 'million' suffix."""
        text = "Estimated value: $2.5 million"
        result = extract_budget(text)
        assert result == 2500000.0
    
    def test_extract_budget_usd_format(self):
        """Test extracting USD format."""
        text = "Budget: USD 500,000"
        result = extract_budget(text)
        assert result == 500000.0
    
    def test_extract_budget_k_suffix(self):
        """Test extracting amount with 'K' suffix."""
        text = "Worth: USD 250K"
        result = extract_budget(text)
        assert result == 250000.0
    
    def test_extract_budget_euro(self):
        """Test extracting Euro amount."""
        text = "Budget: €750,000"
        result = extract_budget(text)
        assert result == 750000.0
    
    def test_extract_budget_million_shorthand(self):
        """Test extracting amount with 'M' suffix."""
        text = "Value: 1.5M USD"
        result = extract_budget(text)
        assert result == 1500000.0
    
    def test_extract_budget_no_match(self):
        """Test extract_budget returns None when no pattern matches."""
        text = "This is a project description with no budget information"
        result = extract_budget(text)
        assert result is None
    
    def test_extract_budget_empty_text(self):
        """Test extract_budget returns None for empty text."""
        result = extract_budget("")
        assert result is None
    
    def test_extract_budget_none_text(self):
        """Test extract_budget returns None for None input."""
        result = extract_budget(None)
        assert result is None
    
    def test_extract_budget_with_commas(self):
        """Test extracting amount with comma separators."""
        text = "Total budget is $1,250,000.00 for this project"
        result = extract_budget(text)
        assert result == 1250000.0


class TestApplySourceWeighting:
    """Tests for apply_source_weighting function."""
    
    def test_apply_source_weighting_configured(self):
        """Test source weighting with configured source."""
        config = {
            'source_weights': {
                'trusted.gov': 1.5,
                'medium.com': 1.0,
            }
        }
        
        result = apply_source_weighting('https://trusted.gov/feed', config)
        assert result == 1.5
    
    def test_apply_source_weighting_default(self):
        """Test source weighting returns default for unconfigured source."""
        config = {
            'source_weights': {
                'trusted.gov': 1.5,
            }
        }
        
        result = apply_source_weighting('https://unknown.com/feed', config)
        assert result == 1.0
    
    def test_apply_source_weighting_no_weights(self):
        """Test source weighting with empty weights configuration."""
        config = {
            'source_weights': {}
        }
        
        result = apply_source_weighting('https://example.com/feed', config)
        assert result == 1.0
    
    def test_apply_source_weighting_missing_key(self):
        """Test source weighting when source_weights key is missing."""
        config = {}
        
        result = apply_source_weighting('https://example.com/feed', config)
        assert result == 1.0
    
    def test_apply_source_weighting_partial_match(self):
        """Test source weighting with partial URL match."""
        config = {
            'source_weights': {
                'example.com': 1.8,
            }
        }
        
        result = apply_source_weighting('https://example.com/path/to/feed', config)
        assert result == 1.8


class TestScoreItem:
    """Tests for scoring functions and calculate_score."""
    
    def test_score_keyword_match_all_keywords(self):
        """Test keyword scoring with all keywords present."""
        text = "Software development and IT consulting services needed"
        keywords = ['software', 'IT', 'consulting']
        
        score = score_keyword_match(text, keywords)
        assert score == 1.0
    
    def test_score_keyword_match_partial(self):
        """Test keyword scoring with partial matches."""
        text = "Software development services"
        keywords = ['software', 'IT', 'consulting']
        
        score = score_keyword_match(text, keywords)
        assert score == pytest.approx(0.333, rel=0.01)
    
    def test_score_keyword_match_no_matches(self):
        """Test keyword scoring with no matches."""
        text = "Marketing campaign management"
        keywords = ['software', 'IT', 'consulting']
        
        score = score_keyword_match(text, keywords)
        assert score == 0.0
    
    def test_score_budget_above_threshold(self):
        """Test budget scoring above minimum."""
        budget = 200000.0
        min_budget = 100000.0
        
        score = score_budget(budget, min_budget)
        assert score == 1.0
    
    def test_score_budget_at_threshold(self):
        """Test budget scoring at minimum."""
        budget = 100000.0
        min_budget = 100000.0
        
        score = score_budget(budget, min_budget)
        assert score == 0.5
    
    def test_score_budget_below_threshold(self):
        """Test budget scoring below minimum."""
        budget = 50000.0
        min_budget = 100000.0
        
        score = score_budget(budget, min_budget)
        assert score == 0.0
    
    def test_score_budget_none(self):
        """Test budget scoring with no budget."""
        score = score_budget(None, 100000.0)
        assert score == 0.0
    
    def test_score_recency_recent(self):
        """Test recency scoring for recent entry."""
        now = datetime.now(timezone.utc)
        published = now.isoformat()
        
        score = score_recency(published, max_age_days=30)
        assert score == 1.0
    
    def test_score_recency_old(self):
        """Test recency scoring for old entry."""
        from datetime import timedelta
        now = datetime.now(timezone.utc)
        old_date = now - timedelta(days=40)
        published = old_date.isoformat()
        
        score = score_recency(published, max_age_days=30)
        assert score == 0.0
    
    def test_calculate_score_with_keywords_and_budget(self):
        """Test calculate_score produces higher scores with keywords and budget."""
        config = {
            'keywords': ['software', 'IT'],
            'min_budget': 100000,
            'max_age_days': 30,
            'source_weights': {}
        }
        
        # Entry with keywords and budget
        entry_with = {
            'title': 'Software Development RFP',
            'description': 'IT services project worth $500,000',
            'published': datetime.now(timezone.utc).isoformat(),
            'source': 'https://example.com'
        }
        
        # Entry without keywords and budget
        entry_without = {
            'title': 'Marketing Campaign',
            'description': 'Need marketing services',
            'published': datetime.now(timezone.utc).isoformat(),
            'source': 'https://example.com'
        }
        
        score_with = calculate_score(entry_with, config)
        score_without = calculate_score(entry_without, config)
        
        assert score_with > score_without
        assert score_with > 0.5  # Should have meaningful score
        assert score_without < 0.31  # Should have low score (using tolerance for floating point)
    
    def test_calculate_score_stores_budget(self):
        """Test that calculate_score stores extracted budget in entry."""
        config = {
            'keywords': ['software'],
            'min_budget': 100000,
            'max_age_days': 30,
            'source_weights': {}
        }
        
        entry = {
            'title': 'Software RFP',
            'description': 'Budget: $250,000',
            'published': datetime.now(timezone.utc).isoformat(),
            'source': 'https://example.com'
        }
        
        calculate_score(entry, config)
        
        assert 'budget' in entry
        assert entry['budget'] == 250000.0

    def test_calculate_score_region_relevance_boost(self):
        """Test that region mentions increase score when region groups are configured."""
        config = {
            'keywords': ['software'],
            'regions': ['East Asia and Pacific (EAP): Includes China, Indonesia, Pacific Island States, and Philippines.'],
            'min_budget': 100000,
            'max_age_days': 30,
            'source_weights': {}
        }

        entry_with_region = {
            'title': 'Software Procurement Program',
            'description': 'Implementation support for agencies in Indonesia',
            'published': datetime.now(timezone.utc).isoformat(),
            'source': 'https://example.com'
        }

        entry_without_region = {
            'title': 'Software Procurement Program',
            'description': 'Implementation support for agencies in Germany',
            'published': datetime.now(timezone.utc).isoformat(),
            'source': 'https://example.com'
        }

        score_with_region = calculate_score(entry_with_region, config)
        score_without_region = calculate_score(entry_without_region, config)

        assert score_with_region > score_without_region
        assert entry_with_region.get('matched_regions') == ['EAP']


class TestRegionFiltering:
    """Tests for semantic region annotation behavior."""

    def test_filter_entries_semantic_region_group_matching(self):
        """Test filtering annotates semantic region matches without excluding unmatched entries."""
        config = {
            'regions': [
                'East Asia and Pacific (EAP): Includes China, Indonesia, Pacific Island States, and Philippines.'
            ],
            'max_age_days': 30,
        }

        now_iso = datetime.now(timezone.utc).isoformat()
        entries = [
            {
                'title': 'Digital Services Program',
                'description': 'National rollout planned in Indonesia and neighboring markets.',
                'published': now_iso,
                'source': 'https://example.com',
                'link': 'https://example.com/1',
            },
            {
                'title': 'Digital Services Program',
                'description': 'National rollout planned in Germany and Austria.',
                'published': now_iso,
                'source': 'https://example.com',
                'link': 'https://example.com/2',
            },
        ]

        diagnostics = {}
        filtered = filter_entries(entries, config, diagnostics=diagnostics)

        assert len(filtered) == 2
        assert filtered[0]['link'] == 'https://example.com/1'
        assert filtered[0].get('matched_regions') == ['EAP']
        assert 'matched_regions' not in filtered[1]
        assert diagnostics['region_matched'] == 1
        assert diagnostics['region_unmatched'] == 1

    def test_filter_entries_accepts_dict_region_config_entries(self):
        """Test filtering handles YAML dict-shaped region entries and keeps unmatched items."""
        config = {
            'regions': [
                {
                    'East Asia and Pacific (EAP)': (
                        'Includes China, Indonesia, Pacific Island States, and Philippines.'
                    )
                }
            ],
            'max_age_days': 30,
        }

        now_iso = datetime.now(timezone.utc).isoformat()
        entries = [
            {
                'title': 'Digital Services Program',
                'description': 'National rollout planned in Indonesia and neighboring markets.',
                'published': now_iso,
                'source': 'https://example.com',
                'link': 'https://example.com/1',
            },
            {
                'title': 'Digital Services Program',
                'description': 'National rollout planned in Germany and Austria.',
                'published': now_iso,
                'source': 'https://example.com',
                'link': 'https://example.com/2',
            },
        ]

        diagnostics = {}
        filtered = filter_entries(entries, config, diagnostics=diagnostics)

        assert len(filtered) == 2
        assert filtered[0]['link'] == 'https://example.com/1'
        assert filtered[0].get('matched_regions') == ['EAP']
        assert 'matched_regions' not in filtered[1]
        assert diagnostics['region_matched'] == 1
        assert diagnostics['region_unmatched'] == 1


class TestMarkdownOutput:
    """Tests for markdown output generation."""

    def test_get_priority_band_thresholds(self):
        """Test priority band mapping at threshold boundaries."""
        assert get_priority_band(0.60) == 'High'
        assert get_priority_band(0.59) == 'Medium'
        assert get_priority_band(0.40) == 'Medium'
        assert get_priority_band(0.39) == 'Low'

    def test_generate_markdown_output_includes_mvp_sections(self, tmp_path):
        """Test generated markdown contains MVP sections and opportunity details."""
        output_path = tmp_path / 'index.md'
        entries = [
            {
                'title': 'AI Procurement Platform',
                'link': 'https://example.com/rfp-1',
                'description': '<span>Implementation of an AI-powered procurement platform.</span>',
                'published': '2026-02-17T10:00:00+00:00',
                'source': 'https://example.com/feed',
                'source_name': 'Example Agency',
                'score': 0.67,
                'budget': 250000.0,
                'matched_regions': ['EAP'],
            },
            {
                'title': 'Digital Transformation Services',
                'link': 'https://example.com/rfp-2',
                'description': 'Advisory support for digital transformation.',
                'published': '2026-02-16T10:00:00+00:00',
                'source': 'https://sample.org/rss',
                'source_name': 'Sample Development Bank',
                'score': 0.45,
            },
        ]
        metrics = {
            'fetched': 100,
            'filtered': 50,
            'deduplicated': 45,
            'selected': 2,
        }

        generate_markdown_output(entries, metrics, str(output_path))
        content = output_path.read_text()

        assert '## Executive Summary' in content
        assert '- **Total scanned:** 100' in content
        assert '- **Qualifying opportunities:** 2' in content
        assert '- **Priority split:** High 1, Medium 1, Low 0' in content

        assert '## Priority Bands' in content
        assert '**High Priority (score ≥ 0.600):**' in content
        assert '**Medium Priority (0.400–0.599):**' in content
        assert '**Low Priority (score < 0.400):**' in content
        assert '## Region Coverage' in content
        assert '- **Matched region groups:** EAP (1)' in content

        assert '## Top Opportunities' in content
        assert '### 1. [AI Procurement Platform](https://example.com/rfp-1)' in content
        assert '- **Score:** 0.670 (High)' in content
        assert '- **Budget:** $250,000' in content
        assert '- **Matched Regions:** EAP' in content
        assert '- **Summary:** Implementation of an AI-powered procurement platform.' in content
        assert '<span>' not in content
        assert '### 2. [Digital Transformation Services](https://example.com/rfp-2)' in content
        assert '- **Score:** 0.450 (Medium)' in content
        assert '- **Budget:** Not detected' in content

    def test_generate_markdown_output_handles_empty_entries(self, tmp_path):
        """Test generated markdown for empty result sets."""
        output_path = tmp_path / 'index.md'
        metrics = {
            'fetched': 20,
            'filtered': 0,
            'deduplicated': 0,
            'selected': 0,
        }

        generate_markdown_output([], metrics, str(output_path))
        content = output_path.read_text()

        assert '## Executive Summary' in content
        assert '- **Qualifying opportunities:** 0' in content
        assert '- **Priority split:** High 0, Medium 0, Low 0' in content
        assert '## Region Coverage' in content
        assert '- **Matched region groups:** No matched regions detected' in content
        assert '## Top Opportunities' in content
        assert 'No qualifying opportunities for this run.' in content


if __name__ == '__main__':
    pytest.main([__file__, '-v'])
