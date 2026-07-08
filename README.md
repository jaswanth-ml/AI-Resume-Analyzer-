# AI Resume Analyzer

An intelligent **Applicant Tracking System (ATS)–style resume analyzer** that compares a candidate's resume against a job description, computes an ATS match score, and returns AI-powered improvement suggestions — all via a simple REST API.

Built with **FastAPI** and **Ollama** (local LLM), so your resume data stays on your machine.

![Python](https://img.shields.io/badge/Python-3.10+-blue?logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-009688?logo=fastapi&logoColor=white)
![Ollama](https://img.shields.io/badge/Ollama-Local%20LLM-black)
![License](https://img.shields.io/badge/License-MIT-green)

---

## Features

- **PDF resume parsing** — Extract text from uploaded PDF resumes
- **AI skill extraction** — Pull professional skills from resume and job description text using a local LLM
- **ATS scoring** — Compare resume skills vs. JD skills and compute a match percentage
- **Skill breakdown** — Matched, missing, and bonus (extra) skills
- **Actionable suggestions** — AI-generated resume improvements, project ideas, and ATS tips tailored to the role

---

## Tech Stack

| Layer | Technology |
|-------|------------|
| API | [FastAPI](https://fastapi.tiangolo.com/) |
| PDF parsing | [pypdf](https://pypdf.readthedocs.io/) |
| AI / LLM | [Ollama](https://ollama.com/) — `llama3.2:3b` |
| HTTP client | `requests` |
| Validation | Pydantic |

---

## How It Works

```
┌─────────────┐     ┌──────────────┐     ┌─────────────────┐
│  PDF Resume │────▶│ PDF Service  │────▶│  Resume Text    │
└─────────────┘     └──────────────┘     └────────┬────────┘
                                                  │
┌─────────────┐                                   ▼
│  Job Desc   │──────────────────────────▶┌───────────────┐
│  (text)     │                           │  AI Service   │
└─────────────┘                           │ (Ollama LLM)  │
                                          └───────┬───────┘
                                                  │
                    ┌─────────────────────────────┼─────────────────────────────┐
                    ▼                             ▼                             ▼
            Resume Skills                   JD Skills                    Suggestions
                    │                             │                             │
                    └──────────────┬──────────────┘                             │
                                   ▼                                            │
                          ┌─────────────────┐                                   │
                          │ Resume Analyzer │                                   │
                          │  (ATS scoring)  │                                   │
                          └────────┬────────┘                                   │
                                   ▼                                            │
                          JSON Response ◀───────────────────────────────────────┘
```

1. User uploads a **PDF resume** and provides **job description text**
2. PDF text is extracted via `pypdf`
3. Ollama extracts skills from both resume and JD
4. `analyze_resume()` computes ATS score and skill lists
5. Ollama generates personalized improvement suggestions
6. Full analysis is returned as JSON

---

## Prerequisites

- **Python 3.10+**
- **[Ollama](https://ollama.com/)** installed and running locally
- **llama3.2:3b** model pulled in Ollama

### Install Ollama & model

```bash
# Install Ollama from https://ollama.com/download

# Pull the required model
ollama pull llama3.2:3b

# Verify Ollama is running (default: http://localhost:11434)
ollama list
```

---

## Installation

```bash
# Clone the repository
git clone https://github.com/YOUR_USERNAME/Ai_Resume_Analyzer_Project.git
cd Ai_Resume_Analyzer_Project

# Create and activate virtual environment
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

---

## Running the Server

```bash
# From the project root
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

- **API:** http://localhost:8000
- **Swagger UI:** http://localhost:8000/docs
- **ReDoc:** http://localhost:8000/redoc

Ensure **Ollama is running** before calling the analyze endpoint.

---

## API Reference

### `POST /analyze`

Analyze a resume against a job description.

**Content-Type:** `multipart/form-data`

| Field | Type | Required | Description |
|-------|------|----------|-------------|
| `resume` | file (PDF) | Yes | Candidate resume PDF |
| `jd_text` | string | Yes | Full job description text |

#### Example (cURL)

```bash
curl -X POST "http://localhost:8000/analyze" \
  -F "resume=@/path/to/resume.pdf" \
  -F "jd_text=We are looking for a Python developer with FastAPI, Docker, AWS, and PostgreSQL experience..."
```

#### Example (Python)

```python
import requests

url = "http://localhost:8000/analyze"
files = {"resume": open("resume.pdf", "rb")}
data = {"jd_text": "Python, FastAPI, Docker, AWS, PostgreSQL..."}

response = requests.post(url, files=files, data=data)
print(response.json())
```

#### Example Response

```json
{
  "ats_score": 72.5,
  "matched_skills": ["python", "fastapi", "docker"],
  "missing_skills": ["postgresql", "kubernetes"],
  "bonus_skills": ["n8n", "openai"],
  "suggestions": {
    "candidate_summary": "Strong backend profile with Python and FastAPI...",
    "top_missing_skills": ["postgresql", "kubernetes"],
    "project_suggestions": [
      "Build a REST API with FastAPI and PostgreSQL to demonstrate database skills..."
    ],
    "resume_improvements": [
      "Add a bullet quantifying API performance improvements under your FastAPI project..."
    ],
    "ats_improvement_tips": [
      "Mirror JD keywords like 'PostgreSQL' and 'Kubernetes' in your skills section..."
    ]
  }
}
```

---

## ATS Score Calculation

The ATS score is computed as:

```
ATS Score = (Matched Skills / Total JD Skills) × 100
```

| Category | Definition |
|----------|------------|
| **Matched skills** | Skills present in both resume and JD |
| **Missing skills** | Skills in JD but not in resume |
| **Bonus skills** | Skills in resume but not required by JD |

Skills are normalized to lowercase and deduplicated before comparison.

---

## Project Structure

```
Ai_Resume_Analyzer_Project/
├── app/
│   ├── main.py                 # FastAPI app & /analyze endpoint
│   ├── test_ai.py              # Local test script for AI skill extraction
│   ├── schemes/
│   │   └── resume.py           # Pydantic models
│   └── services/
│       ├── ai_service.py       # Ollama integration (skills + suggestions)
│       ├── pdf_service.py      # PDF text extraction
│       └── resume_analyzer.py  # ATS scoring logic
├── requirements.txt
├── .gitignore
└── README.md
```

---

## Testing AI Skill Extraction

A standalone script is included to test Ollama skill extraction:

```bash
cd app
python test_ai.py
```

Make sure Ollama is running with `llama3.2:3b` before executing.

---

## Configuration

| Setting | Default | Location |
|---------|---------|----------|
| Ollama API URL | `http://localhost:11434/api/generate` | `app/services/ai_service.py` |
| LLM model | `llama3.2:3b` | `app/services/ai_service.py` |
| API host/port | `0.0.0.0:8000` | uvicorn CLI |

To use a different model, update the `"model"` field in `ai_service.py` and pull it via `ollama pull <model-name>`.

---

## Limitations

- **PDF only** — Resume upload accepts PDF format (via `pypdf`)
- **Local LLM required** — Ollama must be running; no cloud API fallback
- **Skill-based matching** — Scoring is keyword/skill overlap, not semantic similarity
- **Model output parsing** — Skill extraction expects a valid Python list; suggestions expect valid JSON from the LLM
- **No authentication** — API is open; add auth before production use
- **No persistence** — Results are not stored in a database

---

## Roadmap

- [ ] Support DOCX resume uploads
- [ ] Environment variables for Ollama URL and model name
- [ ] Frontend UI for resume upload and results
- [ ] Semantic skill matching (embeddings)
- [ ] User accounts and analysis history
- [ ] Docker Compose setup (FastAPI + Ollama)

---

## Contributing

Contributions are welcome.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## License

This project is licensed under the MIT License.

---

## Acknowledgments

- [FastAPI](https://fastapi.tiangolo.com/) for the web framework
- [Ollama](https://ollama.com/) for local LLM inference
- [pypdf](https://pypdf.readthedocs.io/) for PDF text extraction
