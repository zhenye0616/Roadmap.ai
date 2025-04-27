import os
import sys
project_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(project_root)
from fastapi import FastAPI, File, UploadFile, HTTPException, Body, Form
from .parse_resume import parse_resume_file_upload, parse_resume_text
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .parseJD import extract_linkedin_job_async, split_job_description
from .llm import suggest_skill_gap
from pydantic import BaseModel
import asyncio

# =========================
app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # or ["http://localhost:3000"]
    allow_methods=["*"],
    allow_headers=["*"],
)


class JDIn(BaseModel):
    text: str


@app.get("/", include_in_schema=False)
async def read_root():
    return {"status": "ok", "message": "Service is up and running"}


@app.get("/health")
async def health():
    return {"status": "ok"}


# =========================
# Resume Parsing Endpoints
# =========================
@app.post("/api/resume")
async def resume_endpoint(file: UploadFile = File(None), plain_text: str = Form(None)):
    """
    Parse resume from uploaded file OR from pasted plain text.
    """
    if not file and not plain_text:
        raise HTTPException(status_code=400, detail="Must upload a file or provide plain text.")
    if file:
        contents = await file.read()
        parsed_data = parse_resume_file_upload(contents, filename=file.filename)
    else:
        parsed_data = parse_resume_text(plain_text)

    return parsed_data


# =========================
# JD Parsing Endpoints
# =========================

@app.post("/api/jd")
async def jd_endpoint(url: str = Form(None), plain_text: str = Form(None)):
    if not url and not plain_text:
        raise HTTPException(status_code=400, detail="Must provide a JD URL or JD text")
    try:
        if url:
            result = await extract_linkedin_job_async(url)
            #print(result)
            #result = split_job_description(plain_text)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Parsing failed: {e}")
    return result


# =========================
# Resume vs JD Comparison
# =========================

@app.post("/compare")
async def compare(
    resume: dict = Body(..., examples={"skills": ["Python", "SQL"]}),
    jd: JDIn = Body(...),
):
    """
    Expects:
      - resume: output from /parse or /api/resume (JSON with 'skills', etc.)
      - jd: { "text": "<full job description text>" }
    Returns:
      - { "roadmap": "<LLM output>" }
    """
    roadmap = suggest_skill_gap(resume, jd.text)
    return {"roadmap": roadmap}
