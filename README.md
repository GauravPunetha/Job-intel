# Job Intelligence Platform

A Python-based job market intelligence application with skill mapping and filtering capabilities.

## Features

- 🔍 **Smart Job Search** - Search and filter jobs by title, location, skills, and source
- ⭐ **Skill Filtering** - Click on skills to discover related jobs
- 📊 **Job Details Modal** - View complete job descriptions, requirements, and apply directly
- 📈 **Analytics Dashboard** - See top locations, skills, and data sources
- ✨ **Real-time Filtering** - Instant results as you select filters

## Project Structure

```
job-intel/
├── app.py                    # Flask backend
├── templates/
│   └── index.html           # Frontend UI
├── collectors/              # Job data collectors
├── pipelines/               # Data processing
├── data/
│   └── silver/             # Processed job data (JSONL)
├── taxonomy/
│   └── skills_seed.json    # Skills taxonomy
└── requirements.txt
```

## Setup

```bash
# Clone the repository
git clone <repo-url>
cd job-intel

# Create virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt
```

## Usage

```bash
# Run the application
python app.py

# Visit http://localhost:5000 in your browser
```

## Features

- Search jobs by title, location, skill, and source
- View complete job details including description, requirements, and skills
- Click skills to filter jobs by that skill
- Direct apply button to job posting
- Real-time filtering with instant results

## License

MIT

### 2. Collect Data (Greenhouse Example)
```bash
# Pull Databricks jobs from Greenhouse (free, public API)
python scripts/run_collectors.py --greenhouse databricks

# You can add more boards:
python scripts/run_collectors.py --greenhouse cloudflare stripe

# Or use Lever:
python scripts/run_collectors.py --lever databricks
```

**Output:** `data/bronze/greenhouse_databricks.jsonl` (raw JSON, one per line)

### 3. Transform to Silver (Normalized)
```bash
# Clean HTML, extract skills, parse salaries
python scripts/transform_greenhouse_databricks.py
```

**Output:** `data/silver/databricks_silver.jsonl` (clean records with skills & salary)

### 4. Analyze & Visualize
Load silver/gold JSONL into:
- **Power BI** / Tableau for dashboards
- **Python** (pandas/Plotly) for analysis
- **SQL** database for querying

**Insights:**
- Top 20 skills by role/location
- Salary bands (min/median/max)
- Posting volume trends
- Emerging skills (YoY growth)

## 🔗 Free Data Sources

| Source | Type | Auth | Coverage |
|--------|------|------|----------|
| **Greenhouse** | Public JSON API | None | 1000s of company boards |
| **Lever** | Public JSON API | None | 1000s of company postings |
| **Workday** | Public JSON | None | Enterprise careers sites |
| **Ashby** | GraphQL API | None | Startup job boards |
| **Recruitee** | Public JSON API | None | Company postings |

## 🕷️ Web Crawling & Scraping Demo

To show real HTML scraping (ethically):

```bash
# Run Scrapy spider on a permissioned career page
# Only works if robots.txt allows!
scrapy runspider collectors/company_site/scrapy_spider.py \
  -a seeds="https://careers.example.com/jobs"
```

**Spider features:**
- ✅ Checks robots.txt before crawling (fail-closed)
- ✅ Throttles requests (1s delay, autothrottle enabled)
- ✅ Clear User-Agent: `JobIntelBot/1.0`
- ✅ Extracts job title, URL, description
- ✅ Deduplication via content hash

## 📋 Taxonomy & Skills Extraction

The project uses a **skills dictionary** (`taxonomy/skills_seed.json`) to map raw job text to canonical skills & JSC IDs:

```json
{
  "pyspark": {
    "aliases": ["spark sql", "apache spark", "databricks"],
    "jsc_id": "DE_PYSPARK"
  },
  "python": {
    "aliases": ["py"],
    "jsc_id": "CORE_PYTHON"
  }
}
```

**To use your internal taxonomy:**
1. Export your Skills 3.0 / JSC master
2. Update `taxonomy/skills_seed.json`
3. Re-run transform scripts

## 🛡️ Compliance & Ethics

✅ **No forbidden platforms:**
- ❌ LinkedIn scraping (banned by ToS)
- ❌ Indeed scraping (banned by ToS)
- ❌ Internshala without permission

✅ **Only use:**
- ✅ Public job board APIs (Greenhouse, Lever, etc.)
- ✅ Pages that allow crawling in robots.txt
- ✅ With polite throttling (1–2s delays)
- ✅ Clear User-Agent

✅ **Data governance:**
- Store job content only (no PII)
- Document data sources & retention
- Align to company privacy policy

## 📊 Sample Output (Silver/Gold)

```json
{
  "source": "greenhouse",
  "employer": "databricks",
  "title": "Senior Data Engineer",
  "location": "San Francisco, CA",
  "url": "https://boards.greenhouse.io/databricks/...",
  "description_text": "We are hiring a senior data engineer...",
  "skills": [
    {"skill_canonical": "pyspark", "jsc_id": "DE_PYSPARK", "freq": 3},
    {"skill_canonical": "python", "jsc_id": "CORE_PYTHON", "freq": 2},
    {"skill_canonical": "sql", "jsc_id": "CORE_SQL", "freq": 1}
  ],
  "salary": {
    "currency": "USD",
    "pay_type": "year",
    "min": 150000,
    "max": 200000
  }
}
```

## 🔧 Customization

### Add a New Greenhouse Board
```bash
python scripts/run_collectors.py --greenhouse your_board_token
```

### Add a Custom Transformation
Create `scripts/transform_your_source.py` with:
1. Read from `data/bronze/`
2. Call `extract_skills()` and `parse_salary()`
3. Write to `data/silver/`

### Scale with Orchestration
The `orchestration/dags/job_intel.py` skeleton shows how to use Apache Airflow:
- Schedule collectors hourly/daily
- Add quality gates (null checks, outlier flags)
- Publish to gold tables automatically

## 📚 References

- [Greenhouse Job Board API](https://developers.greenhouse.io/harvest.html#get-list-jobs)
- [Lever Postings API](https://github.com/lever/postings-api)
- [Scrapy Documentation](https://docs.scrapy.org)
- [robots.txt Standard](https://en.wikipedia.org/wiki/Robots_exclusion_standard)

## 📝 License & Usage

Use responsibly. Respect robots.txt, rate limits, and Terms of Service of all data sources.
