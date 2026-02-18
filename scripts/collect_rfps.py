#!/usr/bin/env python3
"""
RFP Intelligence Collection Script

This script collects RFPs from RSS feeds, filters and scores them based on
configured criteria, and outputs the top-ranked results to a Markdown file.

Pipeline flow:
1. Fetch feeds from feeds.txt
2. Parse entries from each feed
3. Filter entries (keywords, budget, regions, time)
4. Deduplicate entries
5. Score entries (keyword match, budget, recency, source weight)
6. Rank and select top N
7. Output to docs/index.md
"""

import feedparser
import hashlib
import json
import os
import re
import sys
import yaml
from datetime import datetime, timezone, timedelta
from pathlib import Path
from typing import Dict, List, Optional, Any
from urllib.parse import urlparse
import requests
from email.utils import parsedate_to_datetime


def load_config(config_path: str = "config.yml") -> Dict[str, Any]:
    """
    Load and validate configuration from YAML file.
    
    Args:
        config_path: Path to configuration file
        
    Returns:
        Configuration dictionary
        
    Raises:
        SystemExit: If config file is missing or has invalid values
    """
    if not os.path.exists(config_path):
        print(f"Error: Configuration file '{config_path}' not found.", file=sys.stderr)
        print("Please create config.yml with your criteria.", file=sys.stderr)
        sys.exit(1)
    
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate required fields
    required_fields = ['keywords', 'regions', 'min_budget', 'max_age_days', 'max_results']
    for field in required_fields:
        if field not in config:
            print(f"Error: Required field '{field}' missing in config.yml", file=sys.stderr)
            sys.exit(1)
        if config[field] is None:
            print(f"Error: Field '{field}' in config.yml is null. Please provide a value.", file=sys.stderr)
            print(f"Example values:", file=sys.stderr)
            if field == 'keywords':
                print(f"  keywords: ['software', 'IT', 'consulting']", file=sys.stderr)
            elif field == 'regions':
                print(f"  regions: ['US', 'EU', 'UK']", file=sys.stderr)
            elif field == 'min_budget':
                print(f"  min_budget: 10000", file=sys.stderr)
            elif field == 'max_age_days':
                print(f"  max_age_days: 30", file=sys.stderr)
            elif field == 'max_results':
                print(f"  max_results: 20", file=sys.stderr)
            sys.exit(1)
    
    return config


def load_feeds(feeds_path: str = "feeds.txt") -> List[str]:
    """
    Load RSS feed URLs from file.
    
    Args:
        feeds_path: Path to feeds file
        
    Returns:
        List of feed URLs
    """
    if not os.path.exists(feeds_path):
        print(f"Error: Feeds file '{feeds_path}' not found.", file=sys.stderr)
        print("Please create feeds.txt with RSS feed URLs (one per line).", file=sys.stderr)
        sys.exit(1)
    
    with open(feeds_path, 'r') as f:
        feeds = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    
    if not feeds:
        print(f"Warning: No feeds found in '{feeds_path}'", file=sys.stderr)
    
    return feeds


def validate_link(url: str, timeout: int = 5) -> bool:
    """
    Validate that a URL is accessible.
    
    Args:
        url: URL to validate
        timeout: Request timeout in seconds
        
    Returns:
        True if URL is accessible, False otherwise
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        return response.status_code < 400
    except (requests.RequestException, ValueError, Exception):
        return False


def extract_budget(text: str) -> Optional[float]:
    """
    Extract budget amount from text using common patterns.
    
    Recognizes patterns like:
    - $1,000,000
    - USD 500K
    - €250,000
    - 1.5M
    - Budget: $100,000
    
    Args:
        text: Text to extract budget from
        
    Returns:
        Budget amount in USD, or None if not found
    """
    if not text:
        return None
    
    # Common patterns for budget mentions
    # Pattern 1: decimal number followed by million/M (e.g., "2.5 million", "1.5M")
    pattern = r'(\d+(?:\.\d+)?)\s*(?:million|M)\s*(?:USD|\$|dollars)?'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            amount = float(match.group(1))
            return amount * 1_000_000
        except (ValueError, AttributeError, IndexError):
            pass
    
    # Pattern 2: $ or USD with K suffix
    pattern = r'(?:\$|USD)\s*(\d{1,3}(?:,\d{3})*(?:\.\d+)?)\s*K'
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        try:
            amount_str = match.group(1).replace(',', '')
            amount = float(amount_str)
            return amount * 1_000
        except (ValueError, AttributeError, IndexError):
            pass
    
    # Pattern 3: standard formats with $ or USD
    patterns = [
        r'\$\s*(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)',
        r'USD\s*(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)',
        r'(?:budget|value|worth)[\s:]*\$?\s*(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)',
        r'€\s*(\d{1,3}(?:,\d{3})+(?:\.\d{2})?)',
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            try:
                amount_str = match.group(1).replace(',', '')
                amount = float(amount_str)
                return amount
            except (ValueError, AttributeError, IndexError):
                continue
    
    return None


def get_last_modified_from_url(url: str, timeout: int = 5) -> Optional[datetime]:
    """
    Get Last-Modified header from URL.
    
    Args:
        url: URL to check
        timeout: Request timeout in seconds
        
    Returns:
        Last-Modified datetime in UTC, or None if not available
    """
    try:
        response = requests.head(url, timeout=timeout, allow_redirects=True)
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            dt = parsedate_to_datetime(last_modified)
            return dt.astimezone(timezone.utc)
    except (requests.RequestException, ValueError, Exception):
        pass
    return None


def normalize_published_date(entry: Dict[str, Any], feed_url: str) -> Optional[datetime]:
    """
    Extract and normalize published date from feed entry.
    
    Falls back to Last-Modified header if entry has no published date.
    
    Args:
        entry: Feed entry dictionary
        feed_url: URL of the feed source
        
    Returns:
        Published datetime in UTC, or None if not available
    """
    # Try to get published date from entry
    if hasattr(entry, 'published_parsed') and entry.published_parsed:
        try:
            dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            return dt
        except (ValueError, TypeError):
            pass
    
    if hasattr(entry, 'updated_parsed') and entry.updated_parsed:
        try:
            dt = datetime(*entry.updated_parsed[:6], tzinfo=timezone.utc)
            return dt
        except (ValueError, TypeError):
            pass
    
    # Fallback to Last-Modified from entry link
    if hasattr(entry, 'link'):
        return get_last_modified_from_url(entry.link)
    
    return None


def fetch_and_parse_feeds(feed_urls: List[str]) -> List[Dict[str, Any]]:
    """
    Fetch and parse entries from multiple RSS feeds.
    
    Args:
        feed_urls: List of RSS feed URLs
        
    Returns:
        List of parsed entry dictionaries
    """
    entries = []
    
    for feed_url in feed_urls:
        try:
            print(f"Fetching feed: {feed_url}")
            feed = feedparser.parse(feed_url)
            
            for entry in feed.entries:
                # Skip entries without required fields
                if not hasattr(entry, 'title') or not hasattr(entry, 'link'):
                    continue
                
                published = normalize_published_date(entry, feed_url)
                if not published:
                    print(f"Skipping entry without date: {entry.get('title', 'Unknown')}")
                    continue
                
                # Extract entry data
                entry_data = {
                    'title': entry.title,
                    'link': entry.link,
                    'description': entry.get('summary', entry.get('description', '')),
                    'published': published.isoformat(),
                    'source': feed_url,
                    'source_name': feed.feed.get('title', urlparse(feed_url).netloc),
                }
                
                entries.append(entry_data)
        
        except Exception as e:
            print(f"Error fetching feed {feed_url}: {e}", file=sys.stderr)
            continue
    
    return entries


def apply_source_weighting(source: str, config: Dict[str, Any]) -> float:
    """
    Get weight for a given source.
    
    Args:
        source: Source URL
        config: Configuration dictionary
        
    Returns:
        Weight value (default 1.0 if not configured)
    """
    source_weights = config.get('source_weights', {})
    
    # Check if source URL matches any configured pattern
    for pattern, weight in source_weights.items():
        if pattern in source:
            return weight
    
    return 1.0


def score_keyword_match(text: str, keywords: List[str]) -> float:
    """
    Calculate keyword match score.
    
    Args:
        text: Text to search for keywords
        keywords: List of keywords to match
        
    Returns:
        Score based on keyword matches (0.0 to 1.0+)
    """
    if not text or not keywords:
        return 0.0
    
    text_lower = text.lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text_lower)
    
    # Normalize by number of keywords (but allow scores > 1.0 for multiple matches)
    return matches / max(len(keywords), 1)


def score_budget(budget: Optional[float], min_budget: float) -> float:
    """
    Calculate budget score.
    
    Args:
        budget: Extracted budget amount
        min_budget: Minimum budget threshold
        
    Returns:
        Score based on budget (0.0 to 1.0)
    """
    if budget is None:
        return 0.0
    
    if budget < min_budget:
        return 0.0
    
    # Scale score: min_budget gets 0.5, 2x min_budget gets 1.0
    if budget >= min_budget * 2:
        return 1.0
    
    # Clamp to ensure score doesn't exceed 1.0 due to floating point arithmetic
    return min(1.0, 0.5 + (budget - min_budget) / (min_budget * 2))


def score_recency(published: str, max_age_days: int) -> float:
    """
    Calculate recency score with decay.
    
    Args:
        published: ISO 8601 timestamp
        max_age_days: Maximum age in days
        
    Returns:
        Score based on recency (0.0 to 1.0)
    """
    try:
        pub_date = datetime.fromisoformat(published)
        now = datetime.now(timezone.utc)
        age_days = (now - pub_date).days
        
        if age_days < 0:
            return 1.0  # Future dates get full score
        
        if age_days > max_age_days:
            return 0.0
        
        # Linear decay from 1.0 to 0.0
        return 1.0 - (age_days / max_age_days)
    
    except (ValueError, TypeError):
        return 0.0


def calculate_score(entry: Dict[str, Any], config: Dict[str, Any]) -> float:
    """
    Calculate overall score for an entry.
    
    Args:
        entry: Entry dictionary
        config: Configuration dictionary
        
    Returns:
        Total score
    """
    # Combine title and description for keyword matching
    text = f"{entry.get('title', '')} {entry.get('description', '')}"
    
    # Extract budget from text
    budget = extract_budget(text)
    
    # Calculate component scores
    keyword_score = score_keyword_match(text, config['keywords'])
    budget_score = score_budget(budget, config['min_budget'])
    recency_score = score_recency(entry['published'], config['max_age_days'])
    source_weight = apply_source_weighting(entry['source'], config)
    
    # Weighted combination
    total_score = (
        keyword_score * 0.4 +
        budget_score * 0.3 +
        recency_score * 0.2 +
        source_weight * 0.1
    )
    
    # Store budget in entry for display
    if budget:
        entry['budget'] = budget
    
    return total_score


def filter_entries(entries: List[Dict[str, Any]], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Filter entries based on criteria.
    
    Args:
        entries: List of entry dictionaries
        config: Configuration dictionary
        
    Returns:
        Filtered list of entries
    """
    filtered = []
    
    for entry in entries:
        # Check age
        try:
            pub_date = datetime.fromisoformat(entry['published'])
            now = datetime.now(timezone.utc)
            age_days = (now - pub_date).days
            
            if age_days > config['max_age_days']:
                continue
        except (ValueError, TypeError):
            continue
        
        filtered.append(entry)
    
    return filtered


def deduplicate_entries(entries: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Remove duplicate entries based on link URL.
    
    Args:
        entries: List of entry dictionaries
        
    Returns:
        Deduplicated list of entries
    """
    seen_links = set()
    unique_entries = []
    
    for entry in entries:
        link = entry.get('link', '')
        if link and link not in seen_links:
            seen_links.add(link)
            unique_entries.append(entry)
    
    return unique_entries


def generate_entry_id(entry: Dict[str, Any]) -> str:
    """
    Generate unique ID for an entry.
    
    Args:
        entry: Entry dictionary
        
    Returns:
        Unique ID string
    """
    link = entry.get('link', '')
    title = entry.get('title', '')
    content = f"{link}|{title}"
    return hashlib.md5(content.encode()).hexdigest()[:12]


def load_last_run(last_run_path: str = "data/last_run.json") -> Dict[str, Any]:
    """
    Load last run data.
    
    Args:
        last_run_path: Path to last run file
        
    Returns:
        Last run data dictionary
    """
    if os.path.exists(last_run_path):
        with open(last_run_path, 'r') as f:
            return json.load(f)
    return {'timestamp': None, 'entry_ids': []}


def save_last_run(entries: List[Dict[str, Any]], last_run_path: str = "data/last_run.json"):
    """
    Save last run data.
    
    Args:
        entries: List of entry dictionaries
        last_run_path: Path to last run file
    """
    os.makedirs(os.path.dirname(last_run_path), exist_ok=True)
    
    data = {
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'entry_ids': [generate_entry_id(entry) for entry in entries]
    }
    
    with open(last_run_path, 'w') as f:
        json.dump(data, f, indent=2)


def generate_markdown_output(entries: List[Dict[str, Any]], output_path: str = "docs/index.md"):
    """
    Generate Markdown output file.
    
    Args:
        entries: List of scored and ranked entries
        output_path: Path to output file
    """
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    # Read existing file to check if content would be different
    existing_content = ""
    if os.path.exists(output_path):
        with open(output_path, 'r') as f:
            existing_content = f.read()
    
    # Generate new content
    timestamp = datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S UTC')
    
    lines = [
        "---",
        "title: RFP Intelligence",
        f"updated: {timestamp}",
        "---",
        "",
        "# RFP Intelligence",
        "",
        f"*Last updated: {timestamp}*",
        "",
        f"Found {len(entries)} relevant opportunities:",
        "",
    ]
    
    for i, entry in enumerate(entries, 1):
        lines.append(f"## {i}. {entry['title']}")
        lines.append("")
        lines.append(f"**Link:** [{entry['link']}]({entry['link']})")
        lines.append("")
        lines.append(f"**Published:** {entry['published']}")
        lines.append("")
        lines.append(f"**Source:** {entry.get('source_name', 'Unknown')}")
        lines.append("")
        
        if 'budget' in entry:
            lines.append(f"**Estimated Budget:** ${entry['budget']:,.0f}")
            lines.append("")
        
        if entry.get('description'):
            # Truncate long descriptions
            desc = entry['description']
            if len(desc) > 500:
                desc = desc[:500] + "..."
            lines.append(f"**Description:** {desc}")
            lines.append("")
        
        lines.append("---")
        lines.append("")
    
    new_content = "\n".join(lines)
    
    # Only write if content changed (idempotency)
    if new_content != existing_content:
        with open(output_path, 'w') as f:
            f.write(new_content)
        print(f"Generated output: {output_path}")
    else:
        print(f"No changes to output: {output_path}")


def main():
    """Main execution function."""
    print("RFP Intelligence Collection Script")
    print("=" * 40)
    
    # Load configuration
    config = load_config()
    print(f"Loaded configuration: {config.get('max_results', 0)} max results")
    
    # Load feeds
    feeds = load_feeds()
    print(f"Loaded {len(feeds)} feed(s)")
    
    if not feeds:
        print("No feeds to process. Exiting.")
        sys.exit(0)
    
    # Fetch and parse feeds
    entries = fetch_and_parse_feeds(feeds)
    print(f"Fetched {len(entries)} total entries")
    
    # Filter entries
    entries = filter_entries(entries, config)
    print(f"After filtering: {len(entries)} entries")
    
    # Deduplicate
    entries = deduplicate_entries(entries)
    print(f"After deduplication: {len(entries)} entries")
    
    # Score entries
    for entry in entries:
        entry['score'] = calculate_score(entry, config)
    
    # Sort by score (descending)
    entries.sort(key=lambda x: x['score'], reverse=True)
    
    # Take top N results
    max_results = config.get('max_results', 20)
    top_entries = entries[:max_results]
    print(f"Selected top {len(top_entries)} entries")
    
    # Generate output
    generate_markdown_output(top_entries)
    
    # Save last run data
    save_last_run(top_entries)
    print("Saved last run data")
    
    print("=" * 40)
    print("Collection complete!")


if __name__ == "__main__":
    main()
