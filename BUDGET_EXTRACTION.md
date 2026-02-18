# Budget Extraction Module

This module provides functionality to extract budget information from text using heuristic pattern matching.

## Installation

No external dependencies are required. This module uses only Python standard library.

## Usage

```python
from src.budget_extraction import extract_budget

# Example 1: Basic dollar amount
result = extract_budget("The budget is $1,000,000", min_budget_config=0)
print(result)
# {'budget_value': 1000000.0, 'budget_currency': 'USD', 'budget_text': '$1000000'}

# Example 2: With k suffix
result = extract_budget("Budget: $50k", min_budget_config=0)
print(result)
# {'budget_value': 50000.0, 'budget_currency': 'USD', 'budget_text': '$50k'}

# Example 3: Range (returns largest value)
result = extract_budget("Budget range: $50k-$200k", min_budget_config=0)
print(result)
# {'budget_value': 200000.0, 'budget_currency': 'USD', 'budget_text': '$200k'}

# Example 4: Small purchase phrase
result = extract_budget("This is a small purchase", min_budget_config=0)
print(result)
# {'budget_value': None, 'budget_currency': 'USD', 'budget_text': 'indicated small/under threshold'}

# Example 5: No budget found
result = extract_budget("No budget information here", min_budget_config=0)
print(result)
# {'budget_value': None, 'budget_currency': None, 'budget_text': None}
```

## Supported Patterns

The function recognizes the following budget patterns:

- **Dollar signs**: `$1,000,000`, `$ 500000`, `$50k`, `$1.5m`
- **USD prefix**: `USD 2000000`, `USD 500k`
- **USD suffix**: `3000000 USD`, `2.5m USD`
- **Ranges**: `$50k-$200k`, `50k-200k`
- **Phrases**: "small purchase", "under $50k", "not to exceed"

## Features

1. **Comma Removal**: Automatically removes commas from numbers (e.g., `$1,000,000` → `1000000`)
2. **Suffix Normalization**: Converts `k` to `× 1,000` and `m` to `× 1,000,000`
3. **Multiple Matches**: Returns the largest value when multiple budget amounts are found
4. **Phrase Detection**: Recognizes phrases indicating no specific budget
5. **Decimal Support**: Handles decimal values (e.g., `$1500.50`, `$1.5m`)

## Return Value

The function returns a dictionary with three keys:

- `budget_value`: The extracted budget as a float, or `None` if no budget found
- `budget_currency`: The currency code (`"USD"`), or `None` if no budget found
- `budget_text`: The matched text from the input, or a description if a phrase was matched

## Testing

Run the test suite:

```bash
python -m unittest tests.test_budget_extraction
```

All 17 tests should pass successfully.

## Parameters

- `text`: The input text to extract budget from
- `min_budget_config`: Minimum budget threshold (reserved for future use to filter low values)

## License

This is part of the RFP Intelligence project.
