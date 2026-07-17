# Profile Automation Tool — Phase 1

Modular FastAPI backend with SQLite persistence and simulated Octo, browser, and Verisoul integrations.

## Run

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
Copy-Item .env.example .env
uvicorn app.main:app --app-dir backend --reload
```

Open `http://127.0.0.1:8000/docs`.

`POST /job/start` starts a background job. Phase 1 uses deterministic dummy scores; profiles scoring 0–30 are retained and marked running, while the rest are stopped and deleted until the target is reached.
