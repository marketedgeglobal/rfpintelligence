#!/usr/bin/env python3
"""Demonstration of the score_item function.

Run with:
    PYTHONPATH=/path/to/rfpintelligence python examples/demo_scoring.py
"""
from datetime import datetime, timezone, timedelta
from src.scoring import score_item


def main():
    """Run scoring examples."""
    # Configuration
    config = {
        "keywords": ["software", "development", "cloud"],
        "min_budget": 10000,
        "days_window": 30,
        "weights": {
            "keyword": 0.45,
            "budget": 0.25,
            "recency": 0.2,
            "source": 0.1
        },
        "source_weights": {
            "sam.gov": 0.9,
            "grants.gov": 0.8,
            "example.com": 0.5
        }
    }
    
    now = datetime.now(timezone.utc)
    
    # Example 1: High-scoring RFP
    item1 = {
        "title": "Software Development and Cloud Migration",
        "summary": "Seeking software development expertise for cloud infrastructure",
        "published_utc": now - timedelta(days=2),
        "budget_value": 75000,
        "source": "sam.gov"
    }
    
    # Example 2: Medium-scoring RFP
    item2 = {
        "title": "IT Consulting Services",
        "summary": "Need consulting for infrastructure upgrade",
        "published_utc": now - timedelta(days=15),
        "budget_value": 25000,
        "source": "example.com"
    }
    
    # Example 3: Low-scoring RFP (old, low budget)
    item3 = {
        "title": "Hardware Purchase",
        "summary": "Equipment procurement for office",
        "published_utc": now - timedelta(days=28),
        "budget_value": 5000,
        "source": "example.com"
    }
    
    # Calculate scores
    score1 = score_item(item1, config)
    score2 = score_item(item2, config)
    score3 = score_item(item3, config)
    
    # Display results
    print("RFP Scoring Demonstration")
    print("=" * 60)
    print(f"\nExample 1: High-Quality Match")
    print(f"  Title: {item1['title']}")
    print(f"  Budget: ${item1['budget_value']:,}")
    print(f"  Age: {(now - item1['published_utc']).days} days")
    print(f"  Score: {score1:.4f}")
    
    print(f"\nExample 2: Medium Match")
    print(f"  Title: {item2['title']}")
    print(f"  Budget: ${item2['budget_value']:,}")
    print(f"  Age: {(now - item2['published_utc']).days} days")
    print(f"  Score: {score2:.4f}")
    
    print(f"\nExample 3: Low Match")
    print(f"  Title: {item3['title']}")
    print(f"  Budget: ${item3['budget_value']:,}")
    print(f"  Age: {(now - item3['published_utc']).days} days")
    print(f"  Score: {score3:.4f}")
    
    print("\n" + "=" * 60)
    print(f"Scores ranked: {score1:.4f} > {score2:.4f} > {score3:.4f}")


if __name__ == "__main__":
    main()
