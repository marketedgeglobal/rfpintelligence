import re

def extract_budget(text, min_budget_config):
    """
    Heuristic budget extraction from text.
    Returns a dict:
      {
        "budget_value": float or None,
        "budget_currency": "USD" or None,
        "budget_text": matched_text or None
      }
    Heuristics:
    - Look for patterns like $1,000,000 or USD 1,000,000 or 1,000,000 USD
    - Look for ranges like $50k-$200k or $50,000 to $200,000
    - Normalize 'k' and 'm' suffixes
    - If multiple matches, return the largest numeric value found
    - If no numeric budget found but phrases like "small purchase" or "under $50k" appear, return None but include matched_text
    - Use min_budget_config to decide whether a found value is meaningful
    
    Args:
        text: The text to extract budget from
        min_budget_config: Minimum budget threshold (reserved for future use to filter low values)
    """
    if not text:
        return {"budget_value": None, "budget_currency": None, "budget_text": None}
    
    # Check for phrases indicating no specific budget first
    if re.search(r"under \$?\s?(\d+)(k|K)?|small purchase|not to exceed", text, re.IGNORECASE):
        return {"budget_value": None, "budget_currency": "USD", "budget_text": "indicated small/under threshold"}
    
    text = text.replace(",", "")
    
    candidates = []
    
    # First, extract ranges separately to handle both values
    range_pattern = r"(\d+(?:\.\d+)?)([kKmM]?)[ ]?-(?:[ ]?)(\d+(?:\.\d+)?)([kKmM]?)"
    for m in re.finditer(range_pattern, text):
        try:
            # Process first value in range
            val1 = float(m.group(1))
            suffix1 = m.group(2) if m.group(2) else ""
            if suffix1 and suffix1.lower() == "k":
                val1 = val1 * 1_000
            if suffix1 and suffix1.lower() == "m":
                val1 = val1 * 1_000_000
            candidates.append((val1, m.group(0)))
            
            # Process second value in range
            val2 = float(m.group(3))
            suffix2 = m.group(4) if m.group(4) else ""
            if suffix2 and suffix2.lower() == "k":
                val2 = val2 * 1_000
            if suffix2 and suffix2.lower() == "m":
                val2 = val2 * 1_000_000
            candidates.append((val2, m.group(0)))
        except Exception:
            continue
    
    # Then process other patterns
    patterns = [
        r"\$ ?(\d+(?:\.\d+)?)([kKmM]?)",
        r"USD ?(\d+(?:\.\d+)?)([kKmM]?)",
        r"(\d+(?:\.\d+)?)([kKmM]?) ?USD",
    ]
    for p in patterns:
        for m in re.finditer(p, text):
            try:
                if len(m.groups()) >= 1:
                    g1 = m.group(1)
                    suffix = m.group(2) if len(m.groups()) >= 2 else ""
                    val = float(g1)
                    if suffix and suffix.lower() == "k":
                        val = val * 1_000
                    if suffix and suffix.lower() == "m":
                        val = val * 1_000_000
                    candidates.append((val, m.group(0)))
            except Exception:
                continue
    if not candidates:
        return {"budget_value": None, "budget_currency": None, "budget_text": None}
    best_val, best_text = max(candidates, key=lambda x: x[0])
    return {"budget_value": float(best_val), "budget_currency": "USD", "budget_text": best_text}
