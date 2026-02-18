# RFP Intelligence

An automated system for collecting, filtering, scoring, and ranking Request for Proposals (RFPs) from RSS feeds based on configurable criteria.

## Features

- 🔍 **Automated Collection**: Fetches RFPs from multiple RSS feeds
- 🎯 **Smart Filtering**: Filters by recency and annotates region matches for scoring
- 📊 **Intelligent Scoring**: Ranks opportunities based on keyword matches, budget size, recency, and source priority
- 🔄 **Deduplication**: Automatically removes duplicate entries
- 📅 **Weekly Automation**: GitHub Actions workflow runs weekly and commits updates
- 📄 **Clean Output**: Generates formatted Markdown documentation

## Setup

### 1. Configure RSS Feeds

Edit `feeds.txt` and add your RSS feed URLs (one per line):

```txt
ReliefWeb Humanitarian Updates - https://reliefweb.int/updates/rss.xml
Asian Development Bank (ADB) Business Opportunities - https://feeds.feedburner.com/procurement-notices
World Bank Procurement & Project Tenders - https://projects.worldbank.org/en/projects-operations/procurement/rss
UN News - Economic Development - https://news.un.org/feed/subscribe/en/news/topic/economic-development/feed/rss.xml
UN News - Humanitarian Aid - https://news.un.org/feed/subscribe/en/news/topic/humanitarian-aid/feed/rss.xml
UN OCHA (Humanitarian Affairs) - https://www.unocha.org/rss.xml
UNHCR (Refugees) - https://www.unhcr.org/rss.xml
EU Tenders (TED) - https://ted.europa.eu/TED/rss/en/RSS.xml
EU International Partnerships - https://international-partnerships.ec.europa.eu/newsroom/feed_en
USAID Press Releases - https://www.usaid.gov/news-information/press-releases/rss.xml
OECD Development Matters - https://oecd-development-matters.org/feed/
African Development Bank (AfDB) Procurement - https://www.afdb.org/en/projects-and-operations/procurement/rss
Inter-American Development Bank (IDB) - https://www.iadb.org/en/rss
Green Climate Fund (GCF) - https://www.greenclimate.fund/rss.xml
Global Environment Facility (GEF) - https://www.thegef.org/rss.xml
United Nations Global Marketplace - https://www.ungm.org/Public/Notice
```

Lines starting with `#` are treated as comments.

### Feeds

Current RSS feeds used by this project:

```txt
https://reliefweb.int/updates/rss.xml
https://feeds.feedburner.com/procurement-notices
https://projects.worldbank.org/en/projects-operations/procurement/rss
https://news.un.org/feed/subscribe/en/news/topic/economic-development/feed/rss.xml
https://news.un.org/feed/subscribe/en/news/topic/humanitarian-aid/feed/rss.xml
https://www.unocha.org/rss.xml
https://www.unhcr.org/rss.xml
https://ted.europa.eu/TED/rss/en/RSS.xml
https://international-partnerships.ec.europa.eu/newsroom/feed_en
https://www.usaid.gov/news-information/press-releases/rss.xml
https://oecd-development-matters.org/feed/
https://www.afdb.org/en/projects-and-operations/procurement/rss
https://www.iadb.org/en/rss
https://www.greenclimate.fund/rss.xml
https://www.thegef.org/rss.xml
https://www.ungm.org/Public/Notice
```

### 2. Configure Criteria

Edit `config.yml` and replace placeholder values with your actual criteria:

```yaml
# Keywords to match in RFP titles and descriptions
keywords:
  - climate adaptation
  - climate resilience
  - WASH
  - water supply
  - sanitation
  - food security
  - nutrition
  - renewable energy
  - energy access
  - public health
  - health systems
  - education
  - vocational training
  - governance
  - capacity building
  - infrastructure
  - urban development

# Regions of interest
regions:
  - East Asia and Pacific (EAP): Includes China, Indonesia, Pacific Island States, and Philippines.
  - Latin America and Caribbean (LAC): Covers South America, Central America, and Caribbean islands.
  - Middle East, North Africa, Afghanistan, & Pakistan (MENAP): Often grouped due to regional stability and development similarities.
  - South Asia (SAR): Includes India, Pakistan, Bangladesh, and Afghanistan.
  - Sub-Saharan Africa (SSA): Focuses on countries south of the Sahara Desert.

# Minimum budget threshold in USD
min_budget: 50000

# Maximum age of RFPs to consider (in days)
max_age_days: 30

# Optional: enforce configured regions as a hard filter
# true = drop entries with no region match, false = keep and only use region in scoring
strict_region_filter: false

# Optional: UNGM fallback ingestion when UNGM RSS parsing is empty
ungm_fallback_enabled: true

# Optional: specific UNGM notice IDs/URLs to always include
ungm_notice_ids:
  - 289708

# Optional: UNGM search fallback paging controls
ungm_search_pages: 1
ungm_search_page_size: 15
ungm_max_fallback_notices: 30

# Maximum number of results to output
max_results: 20

# Optional: Source weights (prioritize certain feeds)
source_weights:
  'trusted-source.gov': 1.5
  'medium-source.com': 1.0
```

**Important**: All null values must be replaced with actual values before running the script.

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Run Locally

Execute the collection script:

```bash
python scripts/collect_rfps.py
```

The script will:
1. Fetch entries from all configured RSS feeds
2. Filter entries by recency and annotate region matches
3. Score and rank the entries
4. Output analysis-only metrics to `docs/index.md`
5. Save run metadata to `data/last_run.json`

## GitHub Actions Automation

### Enable GitHub Pages

1. Go to your repository **Settings** → **Pages**
2. Under "Source", select **Deploy from a branch**
3. Select branch: **main** (or your default branch)
4. Select folder: **/ (root)** or **/docs** (recommended)
5. Click **Save**

Your RFP intelligence analysis page will be available at:
```
https://marketedgeglobal.github.io/rfpintelligence/
```

### What's on the Live Page

The published `docs/index.md` page includes analysis-only data:
- **Pipeline Metrics**: fetched, filtered, deduplicated, selected top results, and filter diagnostics
- **Scoring Summary**: entries scored, average score, highest score, lowest score
- **Run Metadata**: output file path, metadata file path, timezone

### Workflow Schedule

The GitHub Actions workflow (`.github/workflows/weekly-rfps.yml`) automatically:
- ✅ Runs every Monday at 9:00 AM UTC
- ✅ Checks out the repository
- ✅ Sets up Python 3.11
- ✅ Installs dependencies
- ✅ Runs the collection script
- ✅ Verifies the `docs/index.md` live page contains the required analysis sections
- ✅ Commits `docs/index.md` and `data/last_run.json` only if they changed
- ✅ Uses `github-actions[bot]` as the commit author

### Trigger Workflow Manually

To run the workflow on-demand:

1. Go to your repository on GitHub
2. Click the **Actions** tab
3. Select **Weekly RFP Collection** workflow
4. Click **Run workflow** button
5. Select the branch (usually `main`)
6. Click **Run workflow**

The workflow will execute immediately, and results will be committed automatically if there are changes.

## Architecture

### Pipeline Flow

```
1. Fetch feeds → 2. Parse entries → 3. Filter → 4. Deduplicate → 5. Score → 6. Rank → 7. Output
```

### Scoring System

Entries are scored based on four components:

1. **Keyword Match (40%)**: How many configured keywords appear in the title/description
2. **Budget (30%)**: Higher budgets score higher (minimum threshold configurable)
3. **Recency (20%)**: Newer entries score higher (linear decay over max_age_days)
4. **Source Weight (10%)**: Priority multiplier for trusted sources

### Idempotency

Running the script multiple times without new feed items will NOT change `docs/index.md`. The script only updates the file if content has changed, ensuring clean Git history.

## Testing

Run the test suite:

```bash
# Run all tests
pytest tests/

# Run with verbose output
pytest tests/ -v

# Run specific test file
pytest tests/test_collect_rfps.py -v
```

Tests cover:
- Link validation with mocking
- Budget extraction patterns
- Source weighting logic
- Scoring functions
- Integration scenarios

## File Structure

```
rfpintelligence/
├── .github/
│   └── workflows/
│       └── weekly-rfps.yml    # GitHub Actions workflow
├── data/
│   └── last_run.json          # Metadata from last run
├── docs/
│   └── index.md               # Generated analysis output (published via GitHub Pages)
├── scripts/
│   └── collect_rfps.py        # Main collection script
├── tests/
│   └── test_collect_rfps.py   # Test suite
├── config.yml                 # Configuration criteria
├── feeds.txt                  # RSS feed URLs
├── requirements.txt           # Python dependencies
├── LICENSE                    # MIT License
└── README.md                  # This file
```

## Timestamps

All timestamps are in UTC and use ISO 8601 format:
```
2026-02-18T14:30:00+00:00
```

## Security

- ❌ No API keys or secrets required
- ❌ No external authentication needed
- ✅ Uses only public RSS feeds
- ✅ All credentials handled by GitHub Actions automatically

## License

MIT License - see [LICENSE](LICENSE) file for details.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Ensure all tests pass
6. Submit a pull request

## Troubleshooting

### Script exits with "null value" error

Make sure all required fields in `config.yml` have actual values (not `null`).

### No entries found

- Verify RSS feed URLs are accessible and valid
- Check that feeds contain recent entries
- Adjust `max_age_days` to include older entries
- Review keyword matching criteria

### GitHub Actions workflow not triggering

- Ensure the workflow file is on your default branch (usually `main`)
- Check that GitHub Actions are enabled in repository settings
- Verify the cron schedule syntax is correct

### GitHub Pages not updating

- Ensure GitHub Pages is enabled in repository settings
- Verify the workflow is committing to the correct branch
- Check that `docs/index.md` exists and has valid content
- Allow a few minutes for GitHub Pages to rebuild after commits
