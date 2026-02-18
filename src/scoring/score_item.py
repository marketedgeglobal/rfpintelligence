"""Score calculation for RFP items."""
from datetime import datetime, timezone
import re


# Constants
BUDGET_MULTIPLIER = 10
SECONDS_PER_DAY = 86400.0

REGION_GROUP_TERMS = {
    "EAP": [
        "east asia and pacific",
        "eap",
        "china",
        "indonesia",
        "philippines",
        "pacific island states",
    ],
    "LAC": [
        "latin america and caribbean",
        "lac",
        "south america",
        "central america",
        "caribbean",
    ],
    "MENAP": [
        "middle east",
        "north africa",
        "afghanistan",
        "pakistan",
        "menap",
    ],
    "SAR": [
        "south asia",
        "sar",
        "india",
        "pakistan",
        "bangladesh",
        "afghanistan",
    ],
    "SSA": [
        "sub-saharan africa",
        "ssa",
        "sahara",
    ],
}


def normalize_region_group(region_label):
    """Normalize a configured region label to a canonical region group code."""
    if not region_label:
        return None

    value = region_label.strip().upper()
    for group in REGION_GROUP_TERMS:
        if f"({group})" in value or re.search(rf"\b{group}\b", value):
            return group

    if "EAST ASIA" in value or "PACIFIC" in value:
        return "EAP"
    if "LATIN AMERICA" in value or "CARIBBEAN" in value:
        return "LAC"
    if "MIDDLE EAST" in value or "NORTH AFRICA" in value:
        return "MENAP"
    if "SOUTH ASIA" in value:
        return "SAR"
    if "SUB-SAHARAN" in value:
        return "SSA"

    return None


def get_configured_region_groups(regions):
    """Return canonical region group codes configured by the user."""
    configured_groups = set()
    for region in regions or []:
        group = normalize_region_group(region)
        if group:
            configured_groups.add(group)
    return configured_groups


def get_matched_region_groups(text, configured_regions):
    """Find semantic region-group matches from text for configured regions."""
    if not text or not configured_regions:
        return set()

    configured_groups = get_configured_region_groups(configured_regions)
    if not configured_groups:
        return set()

    text_lower = text.lower()
    matched_groups = set()
    for group in configured_groups:
        terms = REGION_GROUP_TERMS.get(group, [])
        for term in terms:
            if re.search(rf"\b{re.escape(term.lower())}\b", text_lower):
                matched_groups.add(group)
                break

    return matched_groups


def apply_source_weighting(source, source_weights):
    """
    Apply source weighting based on the source string.
    
    Args:
        source: Source string to look up
        source_weights: Dictionary mapping source patterns to weight values
        
    Returns:
        float: Weight value between 0.0 and 1.0
    """
    if not source_weights:
        return 0.5
    
    source_lower = source.lower()
    for pattern, weight in source_weights.items():
        if pattern.lower() in source_lower:
            return float(weight)
    
    return 0.5


def score_item(item, config):
    """
    Compute final score using config.weights and helper signals.
    item must include:
      - title, summary, published_utc (datetime), budget_value (float or None), source
    Scoring components:
      - keyword_score: fraction of config keywords found in title+summary (0..1)
      - budget_score: if budget_value present, scale between min_budget and 10*min_budget; clamp 0..1
      - recency_score: linear decay where newest = 1.0, oldest in window = 0.0
      - source_score: apply_source_weighting
            - region_score: semantic match of configured region groups (country/group terms)
    Final score = sum(component * weight) normalized to 0..1
    """
    weights = config.get("weights", {})
    now = datetime.now(timezone.utc)
    days_window = config.get("days_window", 30)
    text = (item.get("title", "") + " " + item.get("summary", "")).lower()
    keywords = [k.lower() for k in config.get("keywords", [])]
    if keywords:
        matches = sum(1 for k in keywords if k in text)
        keyword_score = matches / len(keywords)
    else:
        keyword_score = 0.0
    min_budget = float(config.get("min_budget", 0) or 0)
    bval = item.get("budget_value")
    if bval is None:
        budget_score = 0.0
    else:
        top = max(min_budget * BUDGET_MULTIPLIER, min_budget + 1)
        budget_score = min(max((bval - min_budget) / (top - min_budget), 0.0), 1.0)
    pub = item.get("published_utc")
    if not pub:
        recency_score = 0.0
    else:
        age_days = (now - pub).total_seconds() / SECONDS_PER_DAY
        recency_score = max(0.0, min(1.0, (days_window - age_days) / days_window))
    source_score = apply_source_weighting(item.get("source", ""), config.get("source_weights", {}))
    matched_region_groups = get_matched_region_groups(text, config.get("regions", []))
    region_score = 1.0 if matched_region_groups else 0.0
    kw_w = float(weights.get("keyword", 0.45) or 0)
    bd_w = float(weights.get("budget", 0.25) or 0)
    rc_w = float(weights.get("recency", 0.2) or 0)
    so_w = float(weights.get("source", 0.1) or 0)
    rg_w = float(weights.get("region", 0.1 if config.get("regions") else 0.0) or 0)
    if config.get("regions") and "region" not in weights:
        kw_w = max(0.0, kw_w - rg_w)
    raw = (
        keyword_score * kw_w
        + budget_score * bd_w
        + recency_score * rc_w
        + source_score * so_w
        + region_score * rg_w
    )
    total_w = kw_w + bd_w + rc_w + so_w + rg_w
    if matched_region_groups:
        item["matched_regions"] = sorted(matched_region_groups)
    final = raw / total_w if total_w > 0 else raw
    return float(final)
