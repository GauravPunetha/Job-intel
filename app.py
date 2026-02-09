from flask import Flask, render_template, jsonify, request
import json
from pathlib import Path
from collections import Counter
import os

app = Flask(__name__, template_folder=os.path.abspath('templates'))
print(f"📂 Template folder: {app.template_folder}")
print(f"📂 Working directory: {os.getcwd()}")

# Load data
def load_silver_data():
    """Load all silver layer job data"""
    jobs = []
    silver_path = Path("data/silver")
    if silver_path.exists():
        for file in silver_path.glob("*.jsonl"):
            with open(file, 'r', encoding='utf-8') as f:
                for line in f:
                    if line.strip():
                        jobs.append(json.loads(line))
    return jobs

def load_skills():
    """Load skill taxonomy"""
    try:
        with open("taxonomy/skills_seed.json", 'r', encoding='utf-8') as f:
            return json.load(f)
    except:
        return {}

# Cache data
JOBS = load_silver_data()
SKILLS = load_skills()

print(f"✅ Loaded {len(JOBS)} jobs")
print(f"✅ Loaded {len(SKILLS)} skills")
print(f"✅ Data path: {Path('data/silver').absolute()}")

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/stats')
def get_stats():
    """Get overall statistics"""
    if not JOBS:
        return jsonify({"error": "No data available"}), 404
    
    total_jobs = len(JOBS)
    
    # Count locations
    locations = Counter()
    for job in JOBS:
        loc = job.get('location', 'Unknown')
        if loc:
            locations[loc] += 1
    
    # Count skills
    skills = Counter()
    for job in JOBS:
        job_skills = job.get('skills', [])
        for s in job_skills:
            skills[s.get('skill_canonical', 'unknown')] += 1
    
    return jsonify({
        "total_jobs": total_jobs,
        "total_locations": len(locations),
        "total_skills": len(skills),
        "top_locations": dict(locations.most_common(10)),
        "top_skills": dict(skills.most_common(10)),
        "data_sources": list(set(j.get('source', 'unknown') for j in JOBS))
    })

@app.route('/api/jobs')
def get_jobs():
    """Get jobs with filtering"""
    page = request.args.get('page', 1, type=int)
    limit = request.args.get('limit', 20, type=int)
    search = request.args.get('search', '', type=str).lower()
    location = request.args.get('location', '', type=str)
    skill = request.args.get('skill', '', type=str)
    source = request.args.get('source', '', type=str)
    
    filtered = JOBS
    
    # Filter by search term
    if search:
        filtered = [j for j in filtered if 
                   search in j.get('title', '').lower() or
                   search in j.get('location', '').lower()]
    
    # Filter by location
    if location:
        filtered = [j for j in filtered if location.lower() in j.get('location', '').lower()]
    
    # Filter by source
    if source:
        filtered = [j for j in filtered if j.get('source', '') == source]
    
    # Filter by skill
    if skill:
        filtered = [j for j in filtered if any(
            skill.lower() in s.get('skill_canonical', '').lower() 
            for s in j.get('skills', [])
        )]
    
    # Pagination
    total = len(filtered)
    start = (page - 1) * limit
    end = start + limit
    jobs_page = filtered[start:end]
    
    # Add absolute_url field if url exists (for backward compatibility)
    for job in jobs_page:
        if 'url' in job and 'absolute_url' not in job:
            job['absolute_url'] = job['url']
    
    return jsonify({
        "jobs": jobs_page,
        "total": total,
        "page": page,
        "limit": limit,
        "pages": (total + limit - 1) // limit
    })

@app.route('/api/locations')
def get_locations():
    """Get all unique locations"""
    locations = sorted(set(j.get('location', 'Unknown') for j in JOBS if j.get('location')))
    return jsonify({"locations": locations})

@app.route('/api/skills')
def get_all_skills():
    """Get all skills from taxonomy"""
    skills = sorted(SKILLS.keys())
    return jsonify({"skills": skills})

@app.route('/api/sources')
def get_sources():
    """Get all data sources"""
    sources = sorted(set(j.get('source', 'unknown') for j in JOBS))
    return jsonify({"sources": sources})

@app.route('/api/jobs/<int:job_id>')
def get_job_detail(job_id):
    """Get detailed information about a specific job"""
    if job_id < 0 or job_id >= len(JOBS):
        return jsonify({"error": "Job not found"}), 404
    
    job = JOBS[job_id]
    return jsonify({
        "id": job_id,
        "job": job
    })

if __name__ == '__main__':
    print("\n" + "="*70)
    print("🚀 STARTING FLASK SERVER")
    print("="*70)
    print(f"📍 Visit: http://localhost:5000")
    print(f"📊 Jobs loaded: {len(JOBS)}")
    print(f"⭐ Skills loaded: {len(SKILLS)}")
    print("="*70 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000, use_reloader=False)
