# RFP Intelligence

A weekly RFP (Request for Proposal) aggregator that collects, filters, scores, and ranks RFPs from multiple RSS/Atom feeds using GitHub Actions and Python.

## Features

- 🔄 Automated weekly RFP collection via GitHub Actions
- 🎯 Configurable keyword, budget, and region filtering
- 📊 Intelligent scoring and ranking system
- 🔍 Deduplication to avoid redundant RFPs
- 📝 Automatic markdown report generation
- 🌐 GitHub Pages integration for easy viewing

## Quick Start

### 1. Setup Repository

1. Clone this repository or open in GitHub Codespaces
2. Configure your RFP sources and preferences (see Configuration below)

### 2. Configuration

#### Add Feed URLs (`feeds.txt`)

Edit `feeds.txt` and add your RSS/Atom feed URLs (one per line):

```
https://example.com/rfp-feed.xml
https://procurement.example.gov/feed.atom
# Lines starting with # are comments
```

#### Configure Settings (`config.yml`)

Edit `config.yml` to set your preferences:

```yaml
keywords:
  - "software development"
  - "cloud services"
  - "IT consulting"

min_budget: 50000  # Minimum budget in USD

regions:
  - "North America"
  - "Europe"

source_weights:
  trusted-source.gov: 2.0  # Higher weight for trusted sources
  example.com: 1.5

weights:
  keyword_match: 2.0  # Importance of keyword matches
  recency: 1.5        # Importance of how recent the RFP is
  budget: 1.0         # Importance of budget size
  source: 1.0         # Importance of source reputation

top_n: 10           # Number of top RFPs to display
days_window: 7      # Only include RFPs from last N days
```

### 3. Enable GitHub Pages

1. Go to your repository Settings
2. Navigate to "Pages" in the left sidebar
3. Under "Source", select "Deploy from a branch"
4. Select the branch (e.g., `main`) and folder `/docs`
5. Click "Save"
6. Your RFP reports will be available at `https://<username>.github.io/<repository>/`

### 4. Run the Workflow

#### Manual Run (Testing)

1. Go to the "Actions" tab in your repository
2. Select "Weekly RFP Collection" workflow
3. Click "Run workflow" button
4. Wait for the workflow to complete
5. Check `docs/index.md` for the generated report

#### Automatic Weekly Runs

The workflow is configured to run automatically every Monday at 9:00 AM UTC. You can modify the schedule in `.github/workflows/weekly-rfps.yml`:

```yaml
schedule:
  - cron: '0 9 * * 1'  # Every Monday at 9:00 AM UTC
```

### 5. Local Development

To run the script locally:

```bash
# Install dependencies
pip install -r requirements.txt

# Run the collection script
python scripts/collect_rfps.py

# View the generated report
cat docs/index.md
```

## File Structure

```
.
├── feeds.txt                          # RSS/Atom feed URLs
├── config.yml                         # Configuration settings
├── requirements.txt                   # Python dependencies
├── LICENSE                            # MIT License
├── README.md                          # This file
├── scripts/
│   └── collect_rfps.py               # Main RFP collection script
├── .github/
│   └── workflows/
│       └── weekly-rfps.yml           # GitHub Actions workflow
└── docs/
    ├── .gitkeep                      # Ensures docs/ is tracked
    └── index.md                      # Generated RFP report (auto-created)
```

## How It Works

The RFP aggregation pipeline follows these steps:

1. **Fetch Feeds**: Retrieves RSS/Atom feeds from URLs in `feeds.txt`
2. **Parse Entries**: Extracts structured data from each feed entry
3. **Filter**: Applies keyword, budget, region, and time window filters
4. **Deduplicate**: Removes duplicate RFPs based on URL and content similarity
5. **Score**: Calculates relevance scores based on configured weights
6. **Rank**: Sorts RFPs by score (highest first)
7. **Output**: Generates markdown report with top N RFPs in `docs/index.md`

## Customization

### Extending the Script

The `scripts/collect_rfps.py` file is well-commented and modular. You can extend it by:

- Adding custom parsers for specific feed formats
- Implementing budget extraction from descriptions
- Adding region detection logic
- Enhancing the deduplication algorithm
- Customizing the scoring function
- Changing the output format

### Workflow Customization

Modify `.github/workflows/weekly-rfps.yml` to:

- Change the schedule (cron expression)
- Add notifications (email, Slack, etc.)
- Deploy to different platforms
- Add testing steps before committing

## Troubleshooting

### Workflow Fails

- Check the Actions tab for error logs
- Ensure `feeds.txt` contains valid URLs
- Verify `config.yml` syntax is correct
- Check that feeds are accessible and return valid RSS/Atom

### No RFPs Collected

- Verify feed URLs are active and returning content
- Check if filters are too restrictive (keywords, budget, time window)
- Review workflow logs for fetch errors

### GitHub Pages Not Updating

- Ensure workflow has `contents: write` permission
- Check that `docs/index.md` was committed
- Verify GitHub Pages is enabled and pointed to `/docs`

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
