"""Example usage of apply_source_weighting function."""

import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).parent.parent))

from rfpintelligence import apply_source_weighting


def main():
    """Demonstrate the apply_source_weighting function."""
    
    # Example 1: Exact URL match
    config = {
        "https://example.com/page": 0.9,
        "github.com": 0.8,
        "default": 0.5
    }
    
    print("Configuration:", config)
    print()
    
    # Test exact match
    url = "https://example.com/page"
    weight = apply_source_weighting(url, config)
    print(f"URL: {url}")
    print(f"Weight: {weight} (exact match)")
    print()
    
    # Test domain match
    url = "https://github.com/user/repo"
    weight = apply_source_weighting(url, config)
    print(f"URL: {url}")
    print(f"Weight: {weight} (domain match)")
    print()
    
    # Test default fallback
    url = "https://unknown.com/page"
    weight = apply_source_weighting(url, config)
    print(f"URL: {url}")
    print(f"Weight: {weight} (default fallback)")
    print()
    
    # Test with empty config
    url = "https://any.com/page"
    weight = apply_source_weighting(url, {})
    print(f"URL: {url}")
    print(f"Weight: {weight} (empty config, returns 0.5)")
    print()


if __name__ == "__main__":
    main()
