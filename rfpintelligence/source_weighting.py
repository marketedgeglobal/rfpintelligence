"""Source weighting functionality for RFP Intelligence."""


def apply_source_weighting(item_source_url, source_weights_config):
    """
    Return a numeric weight for the source.
    - If exact match in source_weights_config, return that value.
    - If domain matches a configured key, return that value.
    - Otherwise return source_weights_config.get('default', 0.5)
    """
    if not source_weights_config:
        return 0.5
    if item_source_url in source_weights_config:
        return float(source_weights_config[item_source_url])
    try:
        from urllib.parse import urlparse
        domain = urlparse(item_source_url).netloc
        for key, val in source_weights_config.items():
            if key == "default":
                continue
            if key in domain or domain in key:
                return float(val)
    except Exception:
        pass
    return float(source_weights_config.get("default", 0.5))
