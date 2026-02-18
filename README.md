# rfpintelligence

RFP Intelligence - A Python library for RFP (Request for Proposal) processing and analysis.

## Features

### Source Weighting

The `apply_source_weighting` function provides flexible source URL weighting based on configuration rules.

#### Usage

```python
from rfpintelligence import apply_source_weighting

# Define source weights configuration
config = {
    "https://example.com/page": 0.9,  # Exact URL match
    "github.com": 0.8,                 # Domain match
    "default": 0.5                     # Default fallback
}

# Apply weighting
weight = apply_source_weighting("https://github.com/user/repo", config)
print(weight)  # Output: 0.8
```

#### How it works

The function evaluates source URLs and returns a numeric weight based on these rules:

1. **Exact URL Match**: If the URL exactly matches a key in the config, returns that weight
2. **Domain Match**: If the domain from the URL matches (or is contained in) a config key, returns that weight
3. **Default Fallback**: If no match is found, returns the `default` value from config (or 0.5 if not specified)
4. **Empty Config**: If no config is provided, returns 0.5

## Installation

```bash
pip install -e .
```

## Development

### Running Tests

```bash
python -m unittest discover tests
```

### Example

```bash
python examples/example_usage.py
```

## Requirements

- Python >= 3.6

