# Bernie-SPSS

> Open-source, web-based statistical software for Vietnamese economics students.
> A modern SPSS alternative built with FastAPI + Next.js 14 + shadcn/ui.

---

## Features (Priority 1 — MVP)

| Category | Features |
|---|---|
| **File I/O** | Upload `.sav`, `.csv`, `.xlsx`; export `.sav`; Vietnamese encoding detection |
| **Data View** | Virtualized spreadsheet (10,000+ rows), SPSS Variable View |
| **Descriptives** | Frequencies, Descriptives, Crosstabs, Explore (Shapiro-Wilk, box plots) |
| **Tests** | Independent/Paired/One-Sample T-Test, One-Way ANOVA, Means |
| **Regression** | Pearson/Spearman Correlations, OLS Linear Regression, Binary Logistic |
| **Advanced** | Factor Analysis (EFA), Reliability (Cronbach's α) |
| **Transform** | Recode, Compute Variable, Select Cases, Sort Cases |
| **Charts** | Box plots, Histograms, Scatter plots, Scree plots, Q-Q plots |
| **Export** | PDF (WeasyPrint, SPSS-style tables), Excel (.xlsx, 3-decimal formatting) |

---

## Quick Start with Docker

```bash
# 1. Clone
git clone https://github.com/your-org/bernie-spss.git
cd bernie-spss

# 2. Configure environment
cp .env.example .env
# Edit .env if needed (defaults work for local dev)

# 3. Start all services
docker-compose up --build

# 4. Open browser
open http://localhost:3000

# 5. Verify backend
curl http://localhost:8000/health
# → {"status": "ok", "sessions": 0, "environment": "development"}
```

---

## Local Development (without Docker)

### Backend

```bash
cd backend

# Create virtual environment
python3.11 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure environment
cp .env.example .env

# Start Redis (required for Celery)
docker run -d -p 6379:6379 redis:7-alpine

# Run API server
uvicorn app.main:app --reload --port 8000

# Run Celery worker (in separate terminal)
celery -A app.tasks.celery_tasks worker --loglevel=info --concurrency=2

# API docs: http://localhost:8000/docs
```

### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Configure environment
cp .env.local.example .env.local
# NEXT_PUBLIC_API_URL=http://localhost:8000

# Run development server
npm run dev

# Open: http://localhost:3000
```

### Run Tests

```bash
cd backend
pytest tests/ -v

# With coverage
pytest tests/ --cov=app --cov-report=html
```

---

## Project Structure

```
bernie-spss/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app entry point
│   │   ├── core/
│   │   │   ├── config.py              # pydantic-settings
│   │   │   └── exceptions.py          # Custom exception handlers
│   │   ├── domain/
│   │   │   ├── models/
│   │   │   │   ├── dataset.py         # VariableMeta, DatasetMeta
│   │   │   │   └── job.py             # JobStatus, JobResult
│   │   │   └── services/
│   │   │       ├── spss_io.py         # File I/O + SESSION_STORE
│   │   │       ├── descriptives.py    # Frequencies, Descriptives, Crosstabs
│   │   │       ├── tests.py           # T-tests, ANOVA
│   │   │       ├── regression.py      # OLS, Logistic, Correlation
│   │   │       ├── factor_analysis.py # EFA, Reliability
│   │   │       ├── transforms.py      # Recode, Compute, Filter, Sort
│   │   │       └── export.py          # PDF + Excel export
│   │   ├── api/
│   │   │   ├── routes/                # FastAPI routers
│   │   │   └── schemas/               # Pydantic request/response schemas
│   │   └── tasks/
│   │       └── celery_tasks.py        # Async EFA for large datasets
│   ├── tests/
│   │   ├── unit/                      # Unit tests
│   │   ├── integration/               # API integration tests
│   │   └── fixtures/                  # sample.csv, sample.sav
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/
│   ├── src/
│   │   ├── app/                       # Next.js App Router
│   │   ├── components/
│   │   │   ├── DataGrid/              # TanStack Table + Virtualizer
│   │   │   ├── Dialogs/               # Statistical procedure dialogs
│   │   │   ├── OutputViewer/          # SPSS-style pivot tables
│   │   │   ├── Charts/                # Plotly charts
│   │   │   ├── MenuBar/               # SPSS-style menu
│   │   │   └── Sidebar/               # File import
│   │   ├── stores/                    # Zustand state
│   │   ├── lib/                       # API client, utilities
│   │   ├── types/                     # TypeScript interfaces
│   │   └── workers/                   # Comlink Web Workers
│   └── package.json
├── docker-compose.yml
└── README.md
```

---

## Environment Variables

### Backend (`.env`)

| Variable | Default | Description |
|---|---|---|
| `REDIS_URL` | `redis://localhost:6379/0` | Redis connection for Celery |
| `MAX_UPLOAD_MB` | `50` | Maximum file upload size |
| `ALLOWED_ORIGINS` | `http://localhost:3000` | CORS allowed origins (comma-separated) |
| `ENVIRONMENT` | `development` | `development` or `production` |
| `CLOUDFLARE_R2_*` | (empty) | Optional R2 storage (not used in MVP) |

### Frontend (`.env.local`)

| Variable | Default | Description |
|---|---|---|
| `NEXT_PUBLIC_API_URL` | `http://localhost:8000` | Backend API URL |

---

## Deploy to Render + Vercel

### Backend → Render (Free tier)

1. Create a new **Web Service** on Render
2. Connect your GitHub repo, root directory: `backend`
3. Build command: `pip install -r requirements.txt`
4. Start command: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
5. Add environment variables from `.env.example`
6. Add a **Redis** add-on (or use Render's managed Redis)

### Frontend → Vercel

```bash
cd frontend
npx vercel --prod

# Set environment variable in Vercel dashboard:
# NEXT_PUBLIC_API_URL=https://your-backend.onrender.com
```

---

## SPSS Compatibility Notes

- **Box plot whiskers**: Uses Tukey (1977) adjacent values — actual data points, not fence boundaries
- **Q-Q plots**: Uses Blom (1958) plotting position formula `p = (i - 3/8) / (n + 1/4)`
- **Cronbach's alpha**: Uses `pingouin.cronbach_alpha()` with `ddof=1` — matches SPSS exactly
- **VIF**: `variance_inflation_factor()` from statsmodels
- **SAV encoding**: Auto-detects with `chardet`, falls back to `windows-1258` for Vietnamese files

---

## License

MIT — Free for educational use.
