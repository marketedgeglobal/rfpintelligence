#!/usr/bin/env python3
"""
RFP Aggregator - Collect and Score RFPs from RSS/Atom Feeds
"""
import sys
import os
import logging
import time
import hashlib
import json
from datetime import datetime, timedelta, timezone
from pathlib import Path
from typing import Dict, List, Optional, Any, Tuple
import re

import feedparser
import yaml
import requests
from dateutil import parser as dateutil_parser

# Configure structured logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%dT%H:%M:%SZ'
)
logger = logging.getLogger(__name__)

# Constants
BASE_DIR = Path(__file__).resolve().parent.parent
FEEDS_FILE = BASE_DIR / "feeds.txt"
CONFIG_FILE = BASE_DIR / "config.yml"
OUTPUT_MD = BASE_DIR / "docs" / "index.md"
OUTPUT_JSON = BASE_DIR / "data" / "last_run.json"
MAX_RETRIES = 3
INITIAL_BACKOFF = 1.0


def validate_link(url: str, timeout: int = 8, max_redirects: int = 5) -> Dict[str, Any]:
    """
    Validate a URL by performing a HEAD then GET if needed.
    Returns a dict:
      {
        "url": final_url,
        "status": "ok" | "not_found" | "error" | "redirected",
        "http_status": int or None,
        "final_url": str or None,
        "content_type": str or None,
        "notes": str or None
      }
    Behavior:
    - Try HEAD first. If HEAD returns 200 and content-type present, return ok.
    - If HEAD returns 405 or no useful headers, perform GET with stream=True and read minimal bytes.
    - Follow redirects up to max_redirects and record final_url.
    - Treat 200 as ok, 3xx as redirected (record final_url), 4xx/5xx as not_found or error.
    - Catch network errors and return error with notes.
    """
    try:
        session = requests.Session()
        resp = session.head(url, allow_redirects=True, timeout=timeout)
        final = resp.url
        status_code = resp.status_code
        content_type = resp.headers.get("Content-Type")
        if status_code == 200 and content_type:
            return {"url": url, "status": "ok", "http_status": 200, "final_url": final, "content_type": content_type, "notes": None}
        # If HEAD not helpful, try GET minimal
        resp = session.get(url, allow_redirects=True, timeout=timeout, stream=True)
        final = resp.url
        status_code = resp.status_code
        content_type = resp.headers.get("Content-Type")
        if status_code == 200:
            return {"url": url, "status": "ok", "http_status": 200, "final_url": final, "content_type": content_type, "notes": None}
        if 300 <= status_code < 400:
            return {"url": url, "status": "redirected", "http_status": status_code, "final_url": final, "content_type": content_type, "notes": "redirect"}
        if 400 <= status_code < 600:
            return {"url": url, "status": "not_found", "http_status": status_code, "final_url": final, "content_type": content_type, "notes": None}
        return {"url": url, "status": "error", "http_status": status_code, "final_url": final, "content_type": content_type, "notes": "unexpected status"}
    except requests.RequestException as e:
        return {"url": url, "status": "error", "http_status": None, "final_url": None, "content_type": None, "notes": str(e)}


def load_feeds() -> List[str]:
    """Load RSS/Atom feed URLs from feeds.txt."""
    if not FEEDS_FILE.exists():
        logger.error(f"Feeds file not found: {FEEDS_FILE}")
        sys.exit(1)
    
    feeds = []
    with open(FEEDS_FILE, 'r') as f:
        for line in f:
            line = line.strip()
            if line and not line.startswith('#'):
                feeds.append(line)
    
    logger.info(f"Loaded {len(feeds)} feed URLs")
    return feeds


def load_config() -> Dict[str, Any]:
    """Load and validate configuration from config.yml."""
    if not CONFIG_FILE.exists():
        logger.error(f"Config file not found: {CONFIG_FILE}")
        sys.exit(1)
    
    with open(CONFIG_FILE, 'r') as f:
        config = yaml.safe_load(f)
    
    # Validate required fields
    required_fields = ['keywords', 'min_budget', 'regions', 'source_weights', 
                       'weights', 'top_n', 'days_window']
    for field in required_fields:
        if field not in config:
            logger.error(f"Missing required config field: {field}")
            sys.exit(1)
    
    # Validate weights subfields
    if 'weights' in config:
        required_weight_fields = ['keyword', 'budget', 'recency', 'source']
        for field in required_weight_fields:
            if field not in config['weights']:
                logger.error(f"Missing required config field: weights.{field}")
                sys.exit(1)
    
    # Check for null values that should be populated
    if config.get('top_n') is None:
        logger.error("Config field 'top_n' must be set to a valid integer")
        sys.exit(1)
    
    if config.get('days_window') is None:
        logger.error("Config field 'days_window' must be set to a valid integer")
        sys.exit(1)
    
    if config.get('weights', {}).get('keyword') is None:
        logger.error("Config field 'weights.keyword' must be set to a valid number")
        sys.exit(1)
    
    if config.get('weights', {}).get('budget') is None:
        logger.error("Config field 'weights.budget' must be set to a valid number")
        sys.exit(1)
    
    if config.get('weights', {}).get('recency') is None:
        logger.error("Config field 'weights.recency' must be set to a valid number")
        sys.exit(1)
    
    if config.get('weights', {}).get('source') is None:
        logger.error("Config field 'weights.source' must be set to a valid number")
        sys.exit(1)
    
    logger.info("Configuration loaded and validated successfully")
    return config


def fetch_feed_with_retry(feed_url: str) -> Optional[feedparser.FeedParserDict]:
    """Fetch a feed with exponential backoff retry logic."""
    for attempt in range(MAX_RETRIES):
        try:
            logger.info(f"Fetching feed: {feed_url} (attempt {attempt + 1}/{MAX_RETRIES})")
            response = requests.get(feed_url, timeout=30)
            response.raise_for_status()
            feed = feedparser.parse(response.content)
            
            if feed.bozo:
                logger.warning(f"Feed parse warning for {feed_url}: {feed.get('bozo_exception', 'Unknown error')}")
            
            return feed
        except requests.RequestException as e:
            logger.warning(f"Failed to fetch {feed_url} on attempt {attempt + 1}: {e}")
            if attempt < MAX_RETRIES - 1:
                backoff = INITIAL_BACKOFF * (2 ** attempt)
                logger.info(f"Retrying in {backoff} seconds...")
                time.sleep(backoff)
    
    logger.error(f"Failed to fetch {feed_url} after {MAX_RETRIES} attempts")
    return None


def get_last_modified_from_url(url: str) -> Optional[datetime]:
    """Attempt to get Last-Modified header from URL."""
    try:
        response = requests.head(url, timeout=10, allow_redirects=True)
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            return dateutil_parser.parse(last_modified).astimezone(timezone.utc)
        
        # Try GET if HEAD didn't work
        response = requests.get(url, timeout=10, stream=True)
        last_modified = response.headers.get('Last-Modified')
        if last_modified:
            return dateutil_parser.parse(last_modified).astimezone(timezone.utc)
    except Exception as e:
        logger.debug(f"Could not get Last-Modified from {url}: {e}")
    
    return None


def normalize_published_date(entry: Dict[str, Any], entry_link: str) -> Optional[datetime]:
    """
    Normalize published date to UTC.
    If missing, try Last-Modified from the entry URL.
    """
    # Try standard feedparser date fields
    for date_field in ['published_parsed', 'updated_parsed', 'created_parsed']:
        if hasattr(entry, date_field):
            date_tuple = getattr(entry, date_field)
            if date_tuple:
                try:
                    dt = datetime(*date_tuple[:6], tzinfo=timezone.utc)
                    return dt
                except (TypeError, ValueError):
                    pass
    
    # Try string date fields
    for date_field in ['published', 'updated', 'created']:
        if hasattr(entry, date_field):
            date_str = getattr(entry, date_field)
            if date_str:
                try:
                    dt = dateutil_parser.parse(date_str)
                    return dt.astimezone(timezone.utc)
                except (ValueError, TypeError):
                    pass
    
    # Fallback to Last-Modified from URL
    logger.debug(f"No published date in entry, trying Last-Modified from {entry_link}")
    last_modified = get_last_modified_from_url(entry_link)
    if last_modified:
        logger.info(f"Using Last-Modified date for {entry_link}")
        return last_modified
    
    return None


def extract_region(text: str) -> str:
    """Heuristic to extract region from text."""
    text_lower = text.lower()
    
    regions = {
        'North America': ['usa', 'united states', 'canada', 'mexico', 'north america'],
        'Europe': ['europe', 'uk', 'united kingdom', 'germany', 'france', 'spain', 'italy'],
        'Asia': ['asia', 'china', 'japan', 'india', 'singapore', 'korea'],
        'Africa': ['africa', 'south africa', 'nigeria', 'kenya'],
        'South America': ['south america', 'brazil', 'argentina', 'chile'],
        'Australia': ['australia', 'new zealand', 'oceania'],
        'Middle East': ['middle east', 'uae', 'dubai', 'saudi arabia', 'israel'],
    }
    
    for region, keywords in regions.items():
        for keyword in keywords:
            if keyword in text_lower:
                return region
    
    return 'Unknown'


def extract_budget(text: str) -> Optional[float]:
    """Heuristic to extract budget from text."""
    # Look for currency patterns like $1,000, $1M, $1.5M, USD 1000, etc.
    patterns = [
        r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)\s*(?:million|m)',  # $1.5 million
        r'\$\s*(\d+(?:,\d{3})*(?:\.\d+)?)',  # $1,000 or $1000
        r'usd\s*(\d+(?:,\d{3})*(?:\.\d+)?)',  # USD 1000
        r'budget[:\s]+\$?\s*(\d+(?:,\d{3})*(?:\.\d+)?)',  # budget: $1000
    ]
    
    for pattern in patterns:
        matches = re.findall(pattern, text.lower())
        if matches:
            amount_str = matches[0].replace(',', '')
            try:
                amount = float(amount_str)
                # If pattern included "million" or "m", multiply
                if 'million' in pattern or pattern.endswith('m)'):
                    amount *= 1_000_000
                return amount
            except ValueError:
                pass
    
    return None


def calculate_hash(title: str, summary: str) -> str:
    """Calculate SHA256 hash of title + summary for deduplication."""
    content = f"{title}{summary}".encode('utf-8')
    return hashlib.sha256(content).hexdigest()


def score_keyword_match(item: Dict[str, Any], keywords: List[str], weight: float) -> float:
    """Score based on keyword matches."""
    if not keywords:
        return 0.0
    
    text = f"{item.get('title', '')} {item.get('summary', '')}".lower()
    matches = sum(1 for keyword in keywords if keyword.lower() in text)
    return matches * weight


def score_budget(item: Dict[str, Any], min_budget: Optional[float], weight: float) -> float:
    """Score based on budget."""
    budget = item.get('budget')
    if budget is None or min_budget is None:
        return 0.0
    
    if budget >= min_budget:
        return weight * (budget / min_budget)
    return 0.0


def score_recency(item: Dict[str, Any], weight: float) -> float:
    """Score based on recency (newer is better)."""
    published = item.get('published_utc')
    if not published:
        return 0.0
    
    now = datetime.now(timezone.utc)
    age_hours = (now - published).total_seconds() / 3600
    
    # Decay score over time (exponential decay)
    # Items within 24 hours get full score, then decay
    decay_factor = 24.0  # hours
    recency_score = weight * (1.0 / (1.0 + age_hours / decay_factor))
    return recency_score


def score_source(item: Dict[str, Any], source_weights: Dict[str, float], weight: float) -> float:
    """Score based on source weight."""
    source = item.get('source', '')
    source_weight = source_weights.get(source, 1.0)
    return weight * source_weight


def calculate_score(item: Dict[str, Any], config: Dict[str, Any]) -> float:
    """Calculate total score for an item."""
    score = 0.0
    score += score_keyword_match(item, config.get('keywords', []), config['weights']['keyword'])
    score += score_budget(item, config.get('min_budget'), config['weights']['budget'])
    score += score_recency(item, config['weights']['recency'])
    score += score_source(item, config.get('source_weights', {}), config['weights']['source'])
    return score


def process_feeds(feeds: List[str], config: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Process all feeds and return scored items."""
    now = datetime.now(timezone.utc)
    cutoff = now - timedelta(days=config['days_window'])
    
    all_items = []
    seen_links = set()
    seen_hashes = set()
    
    for feed_url in feeds:
        feed = fetch_feed_with_retry(feed_url)
        if not feed:
            continue
        
        feed_title = feed.feed.get('title', feed_url)
        logger.info(f"Processing {len(feed.entries)} entries from {feed_title}")
        
        for entry in feed.entries:
            # Get link
            link = entry.get('link', '')
            if not link:
                logger.debug("Skipping entry without link")
                continue
            
            # Get published date
            published = normalize_published_date(entry, link)
            if not published:
                logger.debug(f"Skipping entry without published date: {link}")
                continue
            
            # Filter by date window
            if published < cutoff:
                logger.debug(f"Skipping old entry (published {published.isoformat()}): {link}")
                continue
            
            # Get title and summary
            title = entry.get('title', 'No title')
            summary = entry.get('summary', entry.get('description', ''))
            
            # Deduplicate by link
            if link in seen_links:
                logger.debug(f"Skipping duplicate link: {link}")
                continue
            seen_links.add(link)
            
            # Deduplicate by content hash
            content_hash = calculate_hash(title, summary)
            if content_hash in seen_hashes:
                logger.debug(f"Skipping duplicate content: {title}")
                continue
            seen_hashes.add(content_hash)
            
            # Extract structured fields
            text_content = f"{title} {summary}"
            region = extract_region(text_content)
            budget = extract_budget(text_content)
            
            # Validate link
            logger.debug(f"Validating link: {link}")
            link_validation = validate_link(link)
            
            item = {
                'title': title,
                'link': link,
                'summary': summary,
                'published_utc': published,
                'region': region,
                'budget': budget,
                'source': feed_title,
                'link_status': link_validation['status'],
                'link_validation': link_validation,
            }
            
            # Calculate score
            item['score'] = calculate_score(item, config)
            
            all_items.append(item)
            logger.info(f"Added item: {title[:50]}... (score: {item['score']:.2f})")
    
    logger.info(f"Collected {len(all_items)} total items")
    return all_items


def format_budget(budget: Optional[float]) -> str:
    """Format budget for display."""
    if budget is None:
        return 'N/A'
    if budget >= 1_000_000:
        return f'${budget / 1_000_000:.1f}M'
    if budget >= 1_000:
        return f'${budget / 1_000:.0f}K'
    return f'${budget:.0f}'


def generate_markdown(items: List[Dict[str, Any]], config: Dict[str, Any]) -> str:
    """Generate Markdown output with YAML frontmatter."""
    now = datetime.now(timezone.utc)
    
    # Sort by score and take top N
    sorted_items = sorted(items, key=lambda x: x['score'], reverse=True)
    top_items = sorted_items[:config['top_n']]
    
    # Build YAML frontmatter
    frontmatter = {
        'title': 'RFP Intelligence Report',
        'generated_at': now.isoformat(),
        'criteria': {
            'keywords': config.get('keywords', []),
            'min_budget': config.get('min_budget'),
            'regions': config.get('regions', []),
            'source_weights': config.get('source_weights', {}),
            'weights': config.get('weights', {}),
            'top_n': config.get('top_n'),
            'days_window': config.get('days_window'),
        }
    }
    
    # Build markdown
    lines = ['---']
    lines.append(yaml.dump(frontmatter, default_flow_style=False, sort_keys=False).strip())
    lines.append('---')
    lines.append('')
    lines.append(f'# RFP Intelligence Report')
    lines.append('')
    lines.append(f'Generated: {now.strftime("%Y-%m-%d %H:%M:%S UTC")}')
    lines.append('')
    lines.append(f'## Top {len(top_items)} RFPs')
    lines.append('')
    lines.append('| Score | Title | Published (UTC) | Region | Budget | Link | Source | LinkStatus |')
    lines.append('|-------|-------|-----------------|--------|--------|------|--------|------------|')
    
    for item in top_items:
        score = f"{item['score']:.2f}"
        title = item['title'][:50] + ('...' if len(item['title']) > 50 else '')
        published = item['published_utc'].strftime('%Y-%m-%d %H:%M')
        region = item['region']
        budget = format_budget(item.get('budget'))
        link = item['link']
        source = item['source'][:30] + ('...' if len(item['source']) > 30 else '')
        link_status = item['link_status']
        
        lines.append(f"| {score} | {title} | {published} | {region} | {budget} | [Link]({link}) | {source} | {link_status} |")
    
    lines.append('')
    return '\n'.join(lines)


def write_json_output(items: List[Dict[str, Any]]) -> None:
    """Write all items to JSON file."""
    # Convert datetime objects to ISO format strings
    serializable_items = []
    for item in items:
        item_copy = item.copy()
        if 'published_utc' in item_copy and isinstance(item_copy['published_utc'], datetime):
            item_copy['published_utc'] = item_copy['published_utc'].isoformat()
        serializable_items.append(item_copy)
    
    OUTPUT_JSON.parent.mkdir(parents=True, exist_ok=True)
    with open(OUTPUT_JSON, 'w') as f:
        json.dump({
            'generated_at': datetime.now(timezone.utc).isoformat(),
            'total_items': len(items),
            'items': serializable_items
        }, f, indent=2)
    
    logger.info(f"Wrote JSON output to {OUTPUT_JSON}")


def is_content_changed(new_content: str) -> bool:
    """Check if markdown content has changed."""
    if not OUTPUT_MD.exists():
        return True
    
    with open(OUTPUT_MD, 'r') as f:
        old_content = f.read()
    
    return old_content != new_content


def write_markdown_output(content: str) -> bool:
    """Write markdown output and return True if content changed."""
    OUTPUT_MD.parent.mkdir(parents=True, exist_ok=True)
    
    changed = is_content_changed(content)
    
    with open(OUTPUT_MD, 'w') as f:
        f.write(content)
    
    logger.info(f"Wrote Markdown output to {OUTPUT_MD}")
    return changed


def commit_if_changed() -> None:
    """Commit docs/index.md if it has changed (idempotent)."""
    try:
        # Check if there are changes to commit
        result = os.popen('cd /home/runner/work/rfpintelligence/rfpintelligence && git status --porcelain docs/index.md').read()
        
        if result.strip():
            logger.info("Changes detected in docs/index.md, committing...")
            os.system('cd /home/runner/work/rfpintelligence/rfpintelligence && git add docs/index.md')
            os.system('cd /home/runner/work/rfpintelligence/rfpintelligence && git commit -m "Update RFP report"')
            logger.info("Committed changes to docs/index.md")
        else:
            logger.info("No changes to docs/index.md, skipping commit")
    except Exception as e:
        logger.warning(f"Could not commit changes: {e}")


def main() -> int:
    """Main entry point."""
    logger.info("Starting RFP aggregator")
    
    try:
        # Load configuration
        config = load_config()
        feeds = load_feeds()
        
        # Process feeds
        items = process_feeds(feeds, config)
        
        if not items:
            logger.warning("No items collected")
            return 0
        
        # Generate outputs
        markdown_content = generate_markdown(items, config)
        write_json_output(items)
        
        # Write markdown and commit if changed
        changed = write_markdown_output(markdown_content)
        if changed:
            commit_if_changed()
        
        logger.info("RFP aggregator completed successfully")
        return 0
    
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        return 1


if __name__ == "__main__":
    sys.exit(main())
