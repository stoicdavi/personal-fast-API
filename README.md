# Personal Fast API
# DevOps Stage 1 API

This is a simple FastAPI backend deployed behind an Nginx reverse proxy.

## How to run locally
1. Clone the repository.
2. Create a virtual environment: `python3 -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Run the server: `uvicorn main:app --reload`

## Endpoints
* `GET /` : Returns `{"message": "API is running"}`
* `GET /health` : Returns `{"message": "healthy"}`
* `GET /me` : Returns personal details.
