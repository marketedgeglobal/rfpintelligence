# RFP Intelligence Scoring Module

This module provides scoring functionality for RFP (Request for Proposal) items.

## Installation

The module requires Python 3.6 or higher. No external dependencies are required.

## Usage

### Basic Example

```python
from datetime import datetime, timezone
from src.scoring import score_item

# Define your configuration
config = {
    "keywords": ["software", "development"],
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
        "grants.gov": 0.8
    }
}

# Define an RFP item
item = {
    "title": "Software Development Project",
    "summary": "Looking for software development services",
    "published_utc": datetime.now(timezone.utc),
    "budget_value": 50000,
    "source": "sam.gov"
}

# Calculate the score
score = score_item(item, config)
print(f"Score: {score}")
```

## Scoring Components

The `score_item` function computes a final score using four weighted components:

### 1. Keyword Score (0..1)
- Fraction of configured keywords found in title + summary
- Case-insensitive matching
- Default weight: 0.45

### 2. Budget Score (0..1)
- Scales between `min_budget` and `10 * min_budget`
- Clamped to range [0, 1]
- Returns 0 if budget_value is None
- Default weight: 0.25

### 3. Recency Score (0..1)
- Linear decay where newest = 1.0, oldest in window = 0.0
- Based on `days_window` configuration
- Returns 0 if published_utc is None
- Default weight: 0.2

### 4. Source Score (0..1)
- Uses `apply_source_weighting` for source pattern matching
- Default value: 0.5 (if no match found)
- Default weight: 0.1

### Final Score Calculation

```
final_score = (keyword_score * keyword_weight + 
               budget_score * budget_weight + 
               recency_score * recency_weight + 
               source_score * source_weight) / total_weight
```

The final score is normalized to the range [0, 1].

## Configuration

### Required Item Fields

- `title` (str): RFP title
- `summary` (str): RFP summary/description
- `published_utc` (datetime): Publication date (UTC timezone)
- `budget_value` (float or None): Budget amount
- `source` (str): Source identifier

### Configuration Parameters

- `keywords` (list): List of keywords to match
- `min_budget` (float): Minimum budget threshold
- `days_window` (int): Time window in days for recency scoring
- `weights` (dict): Weight values for each scoring component
  - `keyword` (float): Default 0.45
  - `budget` (float): Default 0.25
  - `recency` (float): Default 0.2
  - `source` (float): Default 0.1
- `source_weights` (dict): Mapping of source patterns to weight values

## Testing

Run the test suite:

```bash
python -m unittest tests.test_score_item -v
```

All 20 tests should pass, covering:
- Source weighting functionality
- Keyword matching (case-insensitive)
- Budget scoring (with edge cases)
- Recency scoring
- Missing/null values handling
- Custom weight configurations
- Edge cases (zero weights, empty keywords, etc.)

## API Reference

### `score_item(item, config)`

Computes the final score for an RFP item.

**Parameters:**
- `item` (dict): RFP item with required fields
- `config` (dict): Configuration dictionary

**Returns:**
- `float`: Final score in range [0, 1]

### `apply_source_weighting(source, source_weights)`

Applies source weighting based on pattern matching.

**Parameters:**
- `source` (str): Source identifier
- `source_weights` (dict): Mapping of patterns to weights

**Returns:**
- `float`: Weight value in range [0, 1], defaults to 0.5 if no match

## Security

The implementation has been verified with CodeQL security scanning and contains no known vulnerabilities.

## License

See repository LICENSE file for details.
