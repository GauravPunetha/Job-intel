# Deployment Guide

This guide covers deploying the Job Intelligence Platform to production.

## Quick Start - Render.com (Recommended)

### Step 1: Connect Your Repository
1. Go to [render.com](https://render.com)
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Select the Job-intel repository
5. Set these values:
   - **Name:** job-intel (or your choice)
   - **Environment:** Python 3
   - **Build Command:** `pip install -r requirements_frontend.txt`
   - **Start Command:** `gunicorn wsgi:app`
   - **Instance Type:** Free

### Step 2: Environment Variables (Optional)
Click "Advanced" and add if needed:
- `FLASK_ENV`: `production`
- `PORT`: (Render sets automatically)

### Step 3: Deploy
Click "Create Web Service" and Render will automatically deploy!

---

## Alternative Platforms

### Railway.app
1. Login with GitHub at [railway.app](https://railway.app)
2. Click "New Project"
3. Select "GitHub Repo"
4. Choose job-intel repository
5. Add Variables:
   - `FLASK_ENV=production`
   - `PORT=5000`
6. Deploy!

### Heroku (Legacy)
```bash
heroku login
heroku create your-app-name
heroku buildpacks:set heroku/python
git push heroku main
```

---

## Local Testing Before Deployment

### Start in Production Mode
```bash
set FLASK_ENV=production
gunicorn wsgi:app
```

Or on Linux/Mac:
```bash
export FLASK_ENV=production
gunicorn wsgi:app --bind 0.0.0.0:8000
```

Visit: http://localhost:8000

---

## Data Persistence

The app loads data from local JSONL files in `data/silver/`. Two options:

### Option 1: Commit Data to Repository (Recommended for Small Datasets)
Already done! Your data files are in the repo.

### Option 2: Use Cloud Storage (For Large Datasets)
Modify `app.py` to load from S3/Cloud Storage:
```python
import boto3
s3 = boto3.client('s3')
response = s3.get_object(Bucket='your-bucket', Key='data/silver/combined_all_companies.jsonl')
```

---

## Troubleshooting

### "ModuleNotFoundError: No module named 'flask'"
Make sure `requirements_frontend.txt` is used (has gunicorn):
```bash
pip install -r requirements_frontend.txt
```

### App displays but shows no jobs
Verify data files are in `data/silver/` directory. Check the app logs for errors.

### Slow startup on free tier
Cold starts on free instances take 30-60 seconds. This is normal.

---

## Monitoring

### View Logs
- **Render:** Dashboard → Logs tab
- **Railway:** Project → Deployments → View Logs
- **Local:** Check terminal output

### Health Check
Visit your deployed URL to verify it's working:
```
https://your-app-name.onrender.com
```

Should show the Job Intelligence Dashboard with loaded jobs.

---

## Custom Domain

All platforms support custom domains. Check their documentation for setup (usually adds CNAME to DNS).

---

## Next Steps

1. Choose a platform above
2. Connect your GitHub repository
3. Deploy and test
4. Share your live link! 🚀
