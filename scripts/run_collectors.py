
import argparse, json, sys
from pathlib import Path

# Add parent directory to path so we can import collectors & pipelines
sys.path.insert(0, str(Path(__file__).parent.parent))

BRONZE = Path("data/bronze")
BRONZE.mkdir(parents=True, exist_ok=True)


def write_jsonl(path: Path, records: list[dict]):
    with open(path, 'a', encoding='utf-8') as f:
        for r in records:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--indeed', action='store_true')
    parser.add_argument('--greenhouse', nargs='*', help='Board tokens, e.g., acme contoso')
    parser.add_argument('--lever', nargs='*', help='Company shortnames, e.g., contoso fabrikam')
    args = parser.parse_args()

    if args.indeed:
        from collectors.indeed_api.client import IndeedClient
        client = IndeedClient()
        data = client.search_jobs("Data Engineer", "Pune, IN", 50)
        # Writes raw graph edges for now; adapt to your bronze schema
        edges = data.get('data', {}).get('jobSearch', {}).get('edges', []) if isinstance(data, dict) else []
        write_jsonl(BRONZE / 'indeed_jobs.jsonl', edges)

    if args.greenhouse:
        from collectors.greenhouse_jobboard.collect import fetch_greenhouse_jobs
        for token in args.greenhouse:
            rows = fetch_greenhouse_jobs(token, include_content=True)
            write_jsonl(BRONZE / f'greenhouse_{token}.jsonl', rows)

    if args.lever:
        from collectors.lever_postings.collect import fetch_lever_jobs
        for company in args.lever:
            rows = fetch_lever_jobs(company)
            write_jsonl(BRONZE / f'lever_{company}.jsonl', rows)

if __name__ == '__main__':
    main()
