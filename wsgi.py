"""
Production WSGI entry point for the Flask application.
Used by gunicorn and other production servers.
"""
import os
from app import app

# Ensure environment is set to production
if 'FLASK_ENV' not in os.environ:
    os.environ['FLASK_ENV'] = 'production'

if __name__ == '__main__':
    app.run()
