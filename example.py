#!/usr/bin/env python
"""
Example usage of the extract_budget function.
"""

import sys
import os

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from budget_extraction import extract_budget


def main():
    """Demonstrate budget extraction with various examples."""
    
    examples = [
        "The budget is $1,000,000",
        "Cost: USD 500k",
        "Estimated at 2.5m USD",
        "Range from $50k to $200k",
        "Budget: $50k-$200k",
        "under $50k",
        "small purchase",
        "No budget info here",
        "Not to exceed budget limits",
        "Budget: $1500.50",
        "Proposal for USD 750000 project",
    ]
    
    print("Budget Extraction Examples")
    print("=" * 60)
    print()
    
    for text in examples:
        result = extract_budget(text, min_budget_config=0)
        print(f"Input:    {text}")
        print(f"Value:    {result['budget_value']}")
        print(f"Currency: {result['budget_currency']}")
        print(f"Matched:  {result['budget_text']}")
        print("-" * 60)


if __name__ == "__main__":
    main()
