"""Source weighting functionality for RFP Intelligence."""

from urllib.parse import urlparse


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
        domain = urlparse(item_source_url).netloc
        if domain:  # Only match if domain is not empty
            for key, val in source_weights_config.items():
                if key == "default":
                    continue
                # Check if key is in domain (subdomain match) or exact match
                # This handles cases like 'github.com' matching 'api.github.com'
                if key in domain or domain == key:
                    return float(val)
    except (ValueError, TypeError):
        # Handle URL parsing errors or type conversion issues
        pass
    return float(source_weights_config.get("default", 0.5))
