# comparator.py
from fastapi import FastAPI

app = FastAPI()


@app.get("/", include_in_schema=False)
async def read_root():
    return {"status": "ok", "message": "ML Service is up and running"}
