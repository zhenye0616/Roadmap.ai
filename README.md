**Phase 0: Foundation & Project Setup**

- `backend/` – FastAPI service for resume/JD parsing, LLM integration
- `notion-worker/` – (optional) Node.js service for pushing results into Notion
- `shared/` – shared models/types
- `infra/` – CI/CD configs, Dockerfiles, infra-as-code

**Phase 1: Resume & JD Ingestion MVP**

- Resume parsing endpoint (POST /api/resume)
Input: PDF/DOCX upload (plus optional plain-text)
Pipeline: PDFMiner + spaCy → extract skills list, job titles
Output: JSON { skills: [...], experience: [...] }
- JD parsing endpoint (POST /api/jd)
URL path:
Fetch HTML → strip to main content via Readability → spaCy → extract required skills
Fallback: plain text paste upload using same NLP pipeline

goal: Can reliably turn any resume or JD into a standardized skills array.