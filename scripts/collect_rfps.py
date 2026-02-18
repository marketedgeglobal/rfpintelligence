#!/usr/bin/env python3
"""
RFP Aggregator - Collect and score RFPs from multiple feeds

This script implements a pipeline to:
1. Fetch RSS/Atom feeds from configured sources
2. Parse feed entries into structured RFP data
3. Filter RFPs based on keywords, budget, regions, and time window
4. Deduplicate similar RFPs
5. Score and rank RFPs based on relevance
6. Output top N RFPs to docs/index.md
"""

import sys
from pathlib import Path
from datetime import datetime, timedelta
from typing import List, Dict, Any, Set
import logging

# Standard library imports
import json
import hashlib
import re

# Third-party imports
import feedparser
import yaml
import requests
from dateutil import parser as date_parser
from bs4 import BeautifulSoup


# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)


def load_config(config_path: str = 'config.yml') -> Dict[str, Any]:
    """
    Load configuration from YAML file.
    
    Args:
        config_path: Path to config.yml
        
    Returns:
        Dictionary containing configuration values
    """
    logger.info(f"Loading configuration from {config_path}")
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f) or {}
    
    # Set defaults if values are not provided
    config.setdefault('keywords', [])
    config.setdefault('min_budget', 0)
    config.setdefault('regions', [])
    config.setdefault('source_weights', {})
    config.setdefault('weights', {
        'keyword_match': 1.0,
        'recency': 1.0,
        'budget': 1.0,
        'source': 1.0
    })
    config.setdefault('top_n', 10)
    config.setdefault('days_window', 7)
    
    return config


def load_feeds(feeds_path: str = 'feeds.txt') -> List[str]:
    """
    Load feed URLs from feeds.txt file.
    
    Args:
        feeds_path: Path to feeds.txt
        
    Returns:
        List of feed URLs (excluding comments and empty lines)
    """
    logger.info(f"Loading feed URLs from {feeds_path}")
    feeds = []
    
    with open(feeds_path, 'r') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if line and not line.startswith('#'):
                feeds.append(line)
    
    logger.info(f"Loaded {len(feeds)} feed URLs")
    return feeds


def fetch_feed(url: str) -> feedparser.FeedParserDict:
    """
    Fetch and parse a single RSS/Atom feed.
    
    Args:
        url: Feed URL to fetch
        
    Returns:
        Parsed feed data
    """
    logger.info(f"Fetching feed: {url}")
    try:
        response = requests.get(url, timeout=30)
        response.raise_for_status()
        feed = feedparser.parse(response.content)
        logger.info(f"Successfully fetched {len(feed.entries)} entries from {url}")
        return feed
    except Exception as e:
        logger.error(f"Error fetching feed {url}: {e}")
        return feedparser.FeedParserDict()


def parse_rfp_entry(entry: Any, source_url: str) -> Dict[str, Any]:
    """
    Parse a feed entry into a structured RFP object.
    
    Args:
        entry: Feed entry from feedparser
        source_url: Source feed URL
        
    Returns:
        Dictionary containing RFP data
    """
    # Extract basic fields
    title = entry.get('title', 'Untitled RFP')
    link = entry.get('link', '')
    description = entry.get('description', '') or entry.get('summary', '')
    
    # Parse publication date
    published = entry.get('published', entry.get('updated', ''))
    try:
        pub_date = date_parser.parse(published) if published else datetime.now()
    except (ValueError, TypeError):
        pub_date = datetime.now()
    
    # Extract text content for keyword matching
    soup = BeautifulSoup(description, 'html.parser')
    text_content = soup.get_text()
    
    return {
        'title': title,
        'link': link,
        'description': description,
        'text_content': text_content,
        'published': pub_date,
        'source_url': source_url,
        'id': hashlib.md5(f"{link}_{title}".encode()).hexdigest()
    }


def filter_rfps(rfps: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter RFPs based on configuration criteria.
    
    Filters by:
    - Time window (days_window)
    - Keywords (if specified)
    - Budget (min_budget, if extractable)
    - Regions (if specified)
    
    Args:
        rfps: List of RFP dictionaries
        config: Configuration dictionary
        
    Returns:
        Filtered list of RFPs
    """
    logger.info(f"Filtering {len(rfps)} RFPs")
    
    cutoff_date = datetime.now() - timedelta(days=config['days_window'])
    filtered = []
    
    for rfp in rfps:
        # Time window filter
        if rfp['published'] < cutoff_date:
            continue
        
        # Keyword filter (if keywords are specified)
        if config['keywords']:
            text_lower = (rfp['title'] + ' ' + rfp['text_content']).lower()
            if not any(keyword.lower() in text_lower for keyword in config['keywords']):
                continue
        
        # TODO: Extract and filter by budget and regions when applicable
        
        filtered.append(rfp)
    
    logger.info(f"Filtered to {len(filtered)} RFPs")
    return filtered


def deduplicate_rfps(rfps: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate RFPs based on similarity.
    
    Uses multiple strategies:
    - Exact URL matching
    - Content hash similarity
    - Title similarity (fuzzy matching)
    
    Args:
        rfps: List of RFP dictionaries
        
    Returns:
        Deduplicated list of RFPs
    """
    logger.info(f"Deduplicating {len(rfps)} RFPs")
    
    seen_ids: Set[str] = set()
    seen_links: Set[str] = set()
    unique_rfps = []
    
    for rfp in rfps:
        # Check for duplicate by ID or link
        if rfp['id'] in seen_ids or rfp['link'] in seen_links:
            continue
        
        # TODO: Implement fuzzy title matching for near-duplicates
        
        seen_ids.add(rfp['id'])
        if rfp['link']:
            seen_links.add(rfp['link'])
        unique_rfps.append(rfp)
    
    logger.info(f"Deduplicated to {len(unique_rfps)} unique RFPs")
    return unique_rfps


def score_rfp(rfp: Dict[str, Any], config: Dict[str, Any]) -> float:
    """
    Calculate relevance score for an RFP.
    
    Scoring factors:
    - Keyword match count
    - Recency (newer is better)
    - Budget size (if extractable)
    - Source reputation (from source_weights)
    
    Args:
        rfp: RFP dictionary
        config: Configuration dictionary
        
    Returns:
        Calculated score (float)
    """
    score = 0.0
    weights = config['weights']
    
    # Keyword matching score
    if config['keywords']:
        text_lower = (rfp['title'] + ' ' + rfp['text_content']).lower()
        keyword_matches = sum(1 for kw in config['keywords'] if kw.lower() in text_lower)
        score += keyword_matches * weights.get('keyword_match', 1.0)
    
    # Recency score (more recent = higher score)
    days_old = (datetime.now() - rfp['published']).days
    recency_score = max(0, 7 - days_old) / 7.0  # Normalize to 0-1
    score += recency_score * weights.get('recency', 1.0)
    
    # Source reputation score
    source_weight = config['source_weights'].get(rfp['source_url'], 1.0)
    score += source_weight * weights.get('source', 1.0)
    
    # TODO: Add budget scoring when budget extraction is implemented
    
    return score


def rank_rfps(rfps: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Score and rank RFPs by relevance.
    
    Args:
        rfps: List of RFP dictionaries
        config: Configuration dictionary
        
    Returns:
        Sorted list of RFPs (highest score first)
    """
    logger.info(f"Scoring and ranking {len(rfps)} RFPs")
    
    # Calculate scores
    for rfp in rfps:
        rfp['score'] = score_rfp(rfp, config)
    
    # Sort by score (descending)
    ranked = sorted(rfps, key=lambda x: x['score'], reverse=True)
    
    logger.info(f"Ranked RFPs, top score: {ranked[0]['score']:.2f}" if ranked else "No RFPs to rank")
    return ranked


def generate_output(rfps: List[Dict[str, Any]], config: Dict[str, Any], output_path: str = 'docs/index.md'):
    """
    Generate markdown output with top N RFPs.
    
    Args:
        rfps: Ranked list of RFP dictionaries
        config: Configuration dictionary
        output_path: Path to output markdown file
    """
    logger.info(f"Generating output to {output_path}")
    
    # Take top N RFPs
    top_rfps = rfps[:config['top_n']]
    
    # Generate markdown content
    lines = [
        "# Weekly RFP Intelligence Report",
        "",
        f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}",
        f"**Total RFPs Analyzed:** {len(rfps)}",
        f"**Top RFPs:** {len(top_rfps)}",
        "",
        "---",
        ""
    ]
    
    for i, rfp in enumerate(top_rfps, 1):
        lines.extend([
            f"## {i}. {rfp['title']}",
            "",
            f"**Score:** {rfp['score']:.2f}",
            f"**Published:** {rfp['published'].strftime('%Y-%m-%d')}",
            f"**Source:** {rfp['source_url']}",
            f"**Link:** [{rfp['link']}]({rfp['link']})",
            "",
            f"{rfp['text_content'][:300]}..." if len(rfp['text_content']) > 300 else rfp['text_content'],
            "",
            "---",
            ""
        ])
    
    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    
    # Write output
    with open(output_path, 'w') as f:
        f.write('\n'.join(lines))
    
    logger.info(f"Output written to {output_path}")


def main():
    """
    Main pipeline for RFP aggregation.
    
    Pipeline steps:
    1. Load configuration and feed URLs
    2. Fetch all feeds
    3. Parse entries into RFP objects
    4. Filter RFPs by criteria
    5. Deduplicate RFPs
    6. Score and rank RFPs
    7. Generate output markdown
    """
    logger.info("Starting RFP aggregation pipeline")
    
    try:
        # Step 1: Load configuration and feeds
        config = load_config()
        feed_urls = load_feeds()
        
        if not feed_urls:
            logger.warning("No feed URLs found in feeds.txt")
            return
        
        # Step 2: Fetch all feeds
        all_rfps = []
        for url in feed_urls:
            feed = fetch_feed(url)
            
            # Step 3: Parse entries
            for entry in feed.entries:
                rfp = parse_rfp_entry(entry, url)
                all_rfps.append(rfp)
        
        logger.info(f"Total RFPs collected: {len(all_rfps)}")
        
        if not all_rfps:
            logger.warning("No RFPs collected from feeds")
            return
        
        # Step 4: Filter RFPs
        filtered_rfps = filter_rfps(all_rfps, config)
        
        # Step 5: Deduplicate
        unique_rfps = deduplicate_rfps(filtered_rfps)
        
        # Step 6: Score and rank
        ranked_rfps = rank_rfps(unique_rfps, config)
        
        # Step 7: Generate output
        generate_output(ranked_rfps, config)
        
        logger.info("RFP aggregation pipeline completed successfully")
        
    except Exception as e:
        logger.error(f"Error in RFP aggregation pipeline: {e}")
        sys.exit(1)


if __name__ == '__main__':
    main()
