**Phase 0: Foundation & Project Setup**

This monorepo contains:
- `backend/` – FastAPI service for resume/JD parsing, LLM integration
- `notion-worker/` – (optional) Node.js service for pushing results into Notion
- `shared/` – shared models/types
- `infra/` – CI/CD configs, Dockerfiles, infra-as-code