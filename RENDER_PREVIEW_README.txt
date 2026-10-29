RENDER PREVIEW DEPLOYMENT — TEST DATA ONLY

This package is configured to start as a hosted preview on Render.
It is NOT approved or prepared for collecting real participant data.
The current app uses SQLite in the app filesystem; on Render's free web service,
files are ephemeral and may be lost on redeploy/restart. Do not use it for real
research responses until persistent storage/database, access controls, privacy,
consent, and ethics requirements are addressed.

Render settings:
- New + > Web Service
- Connect the GitHub repository containing the CONTENTS of this folder
- Runtime: Python 3
- Build command: pip install -r requirements.txt
- Start command: gunicorn wsgi:app --bind 0.0.0.0:$PORT --workers 1 --threads 4 --timeout 120
- Environment variable: FLASK_SECRET_KEY = a long random secret string

Do not commit passwords or real participant data to GitHub.
The researcher account is not automatically created by this package; the hosted
preview is intended to inspect the participant-facing demo flow only until a
secure production setup is completed.
