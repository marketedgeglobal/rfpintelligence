"""Score calculation for RFP items."""
from datetime import datetime, timezone


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
    Final score = sum(component * weight) normalized to 0..1
    """
    weights = config.get("weights", {})
    now = datetime.now(timezone.utc)
    days_window = config.get("days_window", 30)
    text = (item.get("title","") + " " + item.get("summary","")).lower()
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
        top = max(min_budget * 10, min_budget + 1)
        budget_score = min(max((bval - min_budget) / (top - min_budget), 0.0), 1.0)
    pub = item.get("published_utc")
    if not pub:
        recency_score = 0.0
    else:
        age_days = (now - pub).total_seconds() / 86400.0
        recency_score = max(0.0, min(1.0, (days_window - age_days) / days_window))
    source_score = apply_source_weighting(item.get("source", ""), config.get("source_weights", {}))
    kw_w = float(weights.get("keyword", 0.45) or 0)
    bd_w = float(weights.get("budget", 0.25) or 0)
    rc_w = float(weights.get("recency", 0.2) or 0)
    so_w = float(weights.get("source", 0.1) or 0)
    raw = keyword_score * kw_w + budget_score * bd_w + recency_score * rc_w + source_score * so_w
    total_w = kw_w + bd_w + rc_w + so_w
    final = raw / total_w if total_w > 0 else raw
    return float(final)
