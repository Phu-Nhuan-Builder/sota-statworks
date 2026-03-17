# SOTA StatWorks

**AI-powered, open-source statistical analysis platform — the next generation of SPSS.**

> 🧠 AI-first architecture: Natural language → statistical analysis → charts + tables + insights
> 🌐 Runs in any browser, no installation required.
> ⚡ Built with FastAPI + Next.js 14 + NVIDIA NIM LLM

[![Live Demo](https://img.shields.io/badge/Live-stat.sotaworks.co-blue)](https://stat.sotaworks.co)
[![GitHub](https://img.shields.io/badge/GitHub-Phu--Nhuan--Builder-black)](https://github.com/Phu-Nhuan-Builder/sota-statworks)

---

## ✨ What Makes SOTA StatWorks Different

| Traditional SPSS | SOTA StatWorks |
|-----------------|----------------|
| Click through menus manually | **Ask in natural language** — AI selects the method |
| Fixed output format | **Multi-modal output** — charts + tables + insights |
| Desktop-only, expensive license | **Free, web-based**, runs anywhere |
| Rule-based only | **AI-first with graceful degradation** |

### 🧠 AI Analysis Pipeline

```
User prompt → LLM Intent Parser → Variable Mapping (fuzzy)
→ Constraint Evaluation (advisory only) → Execute AI method
→ Graceful Degradation (regression → correlation → descriptives)
→ Chart Builder + Table Builder + Constraint-aware Insight
```

---

## Features

### 📊 Statistical Methods (20+)

| # | Feature | Status |
|---|---------|--------|
| 1 | CSV / Excel Import | ✅ |
| 2 | SPSS .sav Import/Export | ✅ |
| 3 | Variable View Editor | ✅ |
| 4 | Frequencies | ✅ |
| 5 | Descriptive Statistics | ✅ |
| 6 | Crosstabs + Chi-Square | ✅ |
| 7 | Independent Samples T-Test | ✅ |
| 8 | Paired Samples T-Test | ✅ |
| 9 | One-Sample T-Test | ✅ |
| 10 | One-Way ANOVA + Post-hoc (Tukey/Bonferroni/Scheffé) | ✅ |
| 11 | Pearson / Spearman Correlation | ✅ |
| 12 | OLS Linear Regression | ✅ |
| 13 | Binary Logistic Regression | ✅ |
| 14 | EFA (Exploratory Factor Analysis) | ✅ |
| 15 | Reliability Analysis (Cronbach's α) | ✅ |
| 16 | Recode Variables | ✅ |
| 17 | Compute Variable | ✅ |
| 18 | Select Cases / Filter | ✅ |
| 19 | Sort Cases | ✅ |
| 20 | Export: Excel + PDF | ✅ |

### 🧠 AI-Powered Features

| Feature | Description |
|---------|-------------|
| **Natural Language Analysis** | "What affects GDP of Vietnam?" → auto regression |
| **Smart Variable Mapping** | Fuzzy matching — "GDP" finds "GDP per capita" |
| **Entity Filtering** | "Compare Vietnam vs China" → auto-filter dataset |
| **Graceful Degradation** | If regression fails → correlation → descriptives |
| **Constraint-Aware Insights** | LLM knows data limitations, won't hallucinate |
| **Multi-Modal Output** | Charts + tables + text insights in one response |

---

## Quick Start

### Docker (Recommended)

```bash
# 1. Clone
git clone https://github.com/Phu-Nhuan-Builder/sota-statworks
cd sota-statworks
cp .env.example .env
cp frontend/.env.local.example frontend/.env.local

# 2. Start all services
docker-compose up --build

# 3. Open browser
open http://localhost:3000

# 4. Verify backend
curl http://localhost:8000/health
# → {"status":"ok","sessions":0,"environment":"development"}
```

### Local Development

#### Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt

# Start FastAPI
python -m uvicorn app.main:app --reload --port 8000
```

#### Frontend

```bash
cd frontend
npm install --legacy-peer-deps
cp .env.local.example .env.local
npm run dev
# Open http://localhost:3000
```

---

## Environment Variables

### Backend (`.env` / `.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NVIDIA_NIM_API_KEY` | — | **Required.** NVIDIA NIM API key for AI features |
| `NVIDIA_NIM_BASE_URL` | `https://integrate.api.nvidia.com/v1` | LLM endpoint |
| `NVIDIA_NIM_MODEL` | `meta/llama-3.1-70b-instruct` | LLM model |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | CORS origins (comma-separated) |
| `MAX_UPLOAD_MB` | `50` | Max file upload size |
| `ENVIRONMENT` | `development` | `development` or `production` |
| `SESSION_TTL_SECONDS` | `3600` | Session expiry time |
| `REDIS_URL` | `redis://localhost:6379/0` | Celery broker (optional) |

### Frontend (`.env.local`)

| Variable | Default | Description |
|----------|---------|-------------|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API base URL |

---

## Deployment

### Backend → Render.com

1. Create **Web Service** → connect GitHub repo
2. Set **Root Directory**: `backend`
3. Set **Runtime**: `Docker`
4. Add environment variables (see table above)
5. Deploy → URL: `https://your-app.onrender.com`

### Frontend → Vercel

1. Import GitHub repo → set **Root Directory**: `frontend`
2. Set `NEXT_PUBLIC_API_URL` to your Render backend URL
3. Deploy → URL: `https://your-app.vercel.app`

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| **Backend** | FastAPI + uvicorn + Pydantic v2 |
| **AI / LLM** | NVIDIA NIM (Llama 3.1 70B) |
| **Statistics** | scipy + statsmodels + pingouin + factor_analyzer |
| **File I/O** | pyreadstat (SPSS .sav), pandas (CSV/Excel) |
| **Task Queue** | Celery + Redis |
| **Export** | openpyxl (Excel), WeasyPrint (PDF) |
| **Frontend** | Next.js 14 + TypeScript + Tailwind CSS |
| **UI Components** | shadcn/ui + Radix UI |
| **Tables** | TanStack Table v8 + TanStack Virtual v3 |
| **State** | Zustand |
| **Charts** | Plotly.js + SVG renderer |
| **HTTP Client** | Axios + TanStack Query |

---

## Architecture

```
sota-statworks/
├── backend/
│   ├── app/
│   │   ├── main.py                  # FastAPI entry point
│   │   ├── core/                    # Config, exceptions
│   │   ├── domain/
│   │   │   ├── models/              # Pydantic domain models
│   │   │   └── services/            # Pure statistical functions
│   │   ├── api/
│   │   │   ├── routes/              # HTTP route handlers
│   │   │   └── schemas/             # Request/Response schemas
│   │   ├── services/                # AI pipeline
│   │   │   ├── orchestrator.py      # Main analysis pipeline
│   │   │   ├── intent_parser.py     # LLM → structured intent
│   │   │   ├── method_router.py     # Intent → statistical method
│   │   │   ├── chart_builder.py     # Results → chart specs
│   │   │   ├── table_builder.py     # Results → table specs
│   │   │   ├── insight_generator.py # Results → LLM explanation
│   │   │   └── llm_client.py        # NVIDIA NIM client
│   │   └── tasks/                   # Celery async tasks
│   ├── Dockerfile
│   └── tests/
├── frontend/
│   └── src/
│       ├── app/                     # Next.js App Router pages
│       ├── components/              # UI components
│       ├── stores/                  # Zustand state
│       ├── lib/                     # API client, utilities
│       └── types/                   # TypeScript interfaces
├── docker-compose.yml
└── README.md
```

---

## Running Tests

```bash
cd backend
pytest tests/ -v

# Run specific test
pytest tests/unit/test_descriptives.py -v
pytest tests/integration/test_api.py -v
```

---

## License

MIT License — Free for academic and commercial use.

Built with ❤️ by **Phu Nhuan Builder** 🇻🇳
