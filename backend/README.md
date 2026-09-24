# Study Tracker Backend

This backend exposes a read-only FastAPI API over the repo's roadmap data.

## Create a virtual environment

```bash
cd backend
python3 -m venv .venv
source .venv/bin/activate
```

## Install dependencies

```bash
pip install -r requirements.txt
```

## Run the server

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at:
- http://localhost:8000/health
- http://localhost:8000/tracks
- http://localhost:8000/tracks/mlops
- http://localhost:8000/tracks/mlops/stats
