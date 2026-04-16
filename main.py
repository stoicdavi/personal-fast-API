from fastapi import FastAPI
from fastapi.responses import JSONResponse

app = FastAPI()

@app.get("/", response_class=JSONResponse)
async def root():
    return {"message": "API is running"}

@app.get("/health", response_class=JSONResponse)
async def health():
    return {"message": "healthy"}

@app.get("/me", response_class=JSONResponse)
async def me():
    return {"name": "David Nanjila", "email": "nanjiladavid2@gmail.com", "github": "https://github.com/stoicdavi"}