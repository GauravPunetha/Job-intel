# Contributing

## Development Setup

1. Clone the repository
2. Create virtual environment: `python -m venv .venv`
3. Activate: `.venv\Scripts\activate` (Windows) or `source .venv/bin/activate` (Unix)
4. Install dependencies: `pip install -r requirements.txt`

## Running the Application

```bash
python app.py
```

Visit `http://localhost:5000` in your browser.

## Project Structure

- `app.py` - Flask backend API
- `templates/index.html` - Frontend UI
- `data/silver/` - Processed job data (JSONL format)
- `taxonomy/skills_seed.json` - Skills taxonomy mapping
- `collectors/` - Job data collection modules
- `pipelines/` - Data processing pipelines

## API Endpoints

- `GET /` - Frontend
- `GET /api/stats` - Overall statistics
- `GET /api/jobs` - Get filtered jobs (pagination)
- `GET /api/locations` - Get all unique locations
- `GET /api/skills` - Get all skills
- `GET /api/sources` - Get all job sources
