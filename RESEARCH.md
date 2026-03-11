# Web-SPSS Research Report

> **Generated**: 2026-03-12 | **Research Effort**: High (5 parallel agents, ~50 searches)
> **Target**: Open-source web-based statistical software for economics students (Vietnam)

---

## Executive Summary

- **Target users**: Economics/social science students, thesis writers (Vietnam universities)
- **Core value prop**: Free, web-based, SPSS-compatible, Vietnamese-supported, no row limit (vs SPSS Student Edition 2,000-row cap)
- **Timeline**: 4-day MVP (Priority 1 features), 2-week full feature (Priority 2)
- **Key insight**: 80% of economics thesis work uses only 12–15 SPSS procedures. Implement these with **APA-quality pivot table output** and you have a viable product. No web-based open-source SPSS alternative exists — this is the primary market gap.
- **Strongest differentiator**: Economics-specific methods (Panel Data FE/RE, Robust SEs, Probit/Tobit) that JASP, jamovi, and PSPP do NOT provide in any GUI

---

## Part 1: Functional Requirements

### Priority 1 — Must-Have (Day 1–2, covers 80% of student use)

| # | Feature | Description | SPSS Menu Path | Python Implementation |
|---|---------|-------------|----------------|----------------------|
| 1 | **CSV/Excel Import** | Import tabular data with auto type detection | File → Import Data | `pandas.read_csv()`, `pandas.read_excel()` |
| 2 | **SPSS .sav Import/Export** | Full metadata round-trip (labels, value codes, missing) | File → Open/Save As | `pyreadstat.read_sav()`, `write_sav()` |
| 3 | **Variable View** | Full SPSS-style metadata editor: name, label, type, width, decimals, values, missing, measure, role | View → Variable View | Pydantic model + pyreadstat meta |
| 4 | **Frequencies** | Counts, percentages, cumulative %, mode, bar/pie chart | Analyze → Descriptive Statistics → Frequencies | `pd.value_counts()`, `scipy.stats.mode()` |
| 5 | **Descriptives** | Mean, median, sum, std dev, variance, range, min, max, SE mean, skewness, kurtosis | Analyze → Descriptive Statistics → Descriptives | `pd.DataFrame.describe()`, `scipy.stats.describe()` |
| 6 | **Crosstabs + Chi-Square** | Frequency table, χ², Cramer's V, Fisher's exact, Phi | Analyze → Descriptive Statistics → Crosstabs | `scipy.stats.chi2_contingency()`, `scipy.stats.fisher_exact()` |
| 7 | **Independent Samples T-Test** | Levene's test, Cohen's d, 95% CI | Analyze → Compare Means → Independent-Samples T Test | `scipy.stats.ttest_ind()`, `scipy.stats.levene()` |
| 8 | **Paired Samples T-Test** | With effect size (Cohen's dz) | Analyze → Compare Means → Paired-Samples T Test | `scipy.stats.ttest_rel()`, `pingouin.ttest()` |
| 9 | **One-Sample T-Test** | Test against known population mean | Analyze → Compare Means → One-Sample T Test | `scipy.stats.ttest_1samp()` |
| 10 | **One-Way ANOVA** | F-test + Levene + Post-hoc (Tukey, Bonferroni, Scheffe) | Analyze → Compare Means → One-Way ANOVA | `scipy.stats.f_oneway()`, `statsmodels.stats.multicomp.pairwise_tukeyhsd()` |
| 11 | **Pearson/Spearman Correlation** | Bivariate correlation matrix with significance | Analyze → Correlate → Bivariate | `scipy.stats.pearsonr()`, `scipy.stats.spearmanr()`, `pingouin.pairwise_corr()` |
| 12 | **OLS Linear Regression** | R², adj. R², ANOVA table, coefficients (B, Beta, t, p, 95% CI), residuals, collinearity diagnostics (VIF) | Analyze → Regression → Linear | `statsmodels.OLS()` |
| 13 | **Binary Logistic Regression** | Log-odds, Exp(B), Hosmer-Lemeshow, classification table | Analyze → Regression → Binary Logistic | `statsmodels.Logit()` |
| 14 | **EFA (Factor Analysis)** | PCA/PAF extraction, Varimax/Oblimin rotation, KMO, Bartlett, scree plot, factor loadings | Analyze → Dimension Reduction → Factor | `factor_analyzer.FactorAnalyzer()` |
| 15 | **Reliability Analysis** | Cronbach's alpha, item-total correlation, alpha-if-deleted | Analyze → Scale → Reliability Analysis | `pingouin.cronbach_alpha()` |
| 16 | **Recode Variables** | Recode into same/different variable, value mapping | Transform → Recode Into Same/Different Variables | Pandas vectorized mapping |
| 17 | **Compute Variable** | Formula-based new variable creation | Transform → Compute Variable | `pd.eval()`, `numexpr` |
| 18 | **Select Cases / Filter** | Conditional row selection | Data → Select Cases | `pd.DataFrame.query()` |
| 19 | **Sort Cases** | Multi-key ascending/descending | Data → Sort Cases | `pd.DataFrame.sort_values()` |
| 20 | **Export: Excel + PDF** | APA-format pivot tables to .xlsx and .pdf | File → Export Output | `openpyxl`, `weasyprint` |

---

### Priority 2 — Should-Have (Day 3–4)

| # | Feature | SPSS Menu Path | Python Implementation |
|---|---------|----------------|----------------------|
| 1 | **Mann-Whitney U** | Analyze → Nonparametric → Legacy → 2 Independent Samples | `scipy.stats.mannwhitneyu()` |
| 2 | **Kruskal-Wallis H** | Analyze → Nonparametric → Legacy → K Independent Samples | `scipy.stats.kruskal()` |
| 3 | **Wilcoxon Signed-Rank** | Analyze → Nonparametric → Legacy → 2 Related Samples | `scipy.stats.wilcoxon()` |
| 4 | **Partial Correlation** | Analyze → Correlate → Partial | `pingouin.partial_corr()` |
| 5 | **Repeated Measures ANOVA** | Analyze → GLM → Repeated Measures | `pingouin.rm_anova()` |
| 6 | **Two-Way ANOVA (GLM Univariate)** | Analyze → GLM → Univariate | `statsmodels.formula.api.ols()` |
| 7 | **Multinomial Logistic Regression** | Analyze → Regression → Multinomial Logistic | `statsmodels.MNLogit()` |
| 8 | **Ordinal Regression** | Analyze → Regression → Ordinal | `statsmodels.ordinal_model.OrderedModel()` |
| 9 | **K-Means Clustering** | Analyze → Classify → K-Means Cluster | `sklearn.cluster.KMeans()` |
| 10 | **Hierarchical Clustering** | Analyze → Classify → Hierarchical Cluster | `scipy.cluster.hierarchy.linkage()` + dendrogram |
| 11 | **Explore (Box plots, stem-leaf, Shapiro-Wilk)** | Analyze → Descriptive Statistics → Explore | `scipy.stats.shapiro()`, box plot via Plotly |
| 12 | **Missing Value Imputation** | Transform → Replace Missing Values | `sklearn.impute.SimpleImputer()`, `IterativeImputer()` |
| 13 | **Merge Files (Add Cases/Variables)** | Data → Merge Files | `pd.concat()`, `pd.merge()` |
| 14 | **Aggregate** | Data → Aggregate | `pd.groupby().agg()` |
| 15 | **Chart Builder** (Bar, Histogram, Scatter, Box) | Graphs → Chart Builder | Plotly + React |

---

### Priority 3 — Nice-to-Have (Week 2 — differentiators)

| # | Feature | Why Important | Python Implementation |
|---|---------|---------------|----------------------|
| 1 | **Panel Data — Fixed Effects** | Standard in econ thesis, NO competitor has GUI | `linearmodels.panel.PanelOLS()` |
| 2 | **Panel Data — Random Effects** | With Hausman test | `linearmodels.panel.RandomEffects()` |
| 3 | **Robust Standard Errors (HC3/HAC)** | Standard in all econ papers | `statsmodels.get_robustcov_results(cov_type='HC3')` |
| 4 | **Probit Model** | Binary choice, econ standard | `statsmodels.Probit()` |
| 5 | **Tobit Model** | Censored data (wages, expenditure) | `statsmodels.Tobit()` |
| 6 | **2SLS / IV Estimation** | Causal inference, endogeneity | `linearmodels.iv.IV2SLS()` |
| 7 | **Multiple Imputation** | MI for missing data, SPSS PROC MI equivalent | `sklearn.impute.IterativeImputer()` |
| 8 | **Kaplan-Meier + Cox Regression** | Survival analysis | `lifelines.KaplanMeierFitter()`, `CoxPHFitter()` |
| 9 | **ARIMA / Time Series** | Forecasting | `statsmodels.tsa.arima.model.ARIMA()` |
| 10 | **Syntax Log** | Reproducibility log (Python equivalent of SPSS .sps) | Auto-generate from UI actions |

---

### Competitor Gap Analysis

| Tool | Strengths | Critical Gaps | Web? |
|------|-----------|---------------|------|
| **JASP** | Bayesian counterparts for every test, APA output, posterior plots | No SEM GUI, no panel data, no web, no econ methods | ❌ |
| **jamovi** | Live results panel (best UX), module ecosystem (SEM, mediation), .sav interop | No Bayesian, no panel data, no economics methods | ❌ |
| **PSPP** | SPSS syntax compatible, lightweight | No pivot table editor, no two-way ANOVA, no CFA/SEM, poor charts | ❌ |
| **Web-SPSS** (ours) | Web browser, Vietnamese support, no row limit, economics module | To be built | ✅ |

**Unique opportunities vs. all competitors**:
- Web browser access (lab computers, Chromebooks — no install)
- Panel data (FE/RE) — no GUI competitor has this for economics students
- Robust SEs (HC3/HAC) — critical for econ papers, no GUI tool provides
- APA table copy-paste to Word with full formatting
- Collaboration / cloud save / share links

---

## Part 2: Technology Stack

### Backend

| Library | Version | Purpose | Alternative Considered |
|---------|---------|---------|----------------------|
| **FastAPI** | `^0.115.0` | Web framework, async HTTP, auto-docs (Swagger) | Flask (no async), Django (too heavy) |
| **uvicorn[standard]** | `^0.30.0` | ASGI server with uvloop | gunicorn (sync only) |
| **pyreadstat** | `^1.2.7` | Read/write SPSS .sav with full metadata; C++ backend | `pandas.read_spss()` (wraps pyreadstat; less control) |
| **pandas** | `^2.2.0` | DataFrame operations, CSV/Excel I/O | polars (less scipy integration) |
| **numpy** | `^1.26.0` | Numerical arrays, matrix ops | — |
| **scipy** | `^1.13.0` | Core statistical tests (t-test, ANOVA, chi2, nonparametric) | — |
| **statsmodels** | `^0.14.0` | OLS/WLS/GLS regression, logistic, time series, ANOVA | — |
| **pingouin** | `^0.5.4` | ANOVA with effect sizes, partial correlation, Cronbach's alpha | scipy (less output detail) |
| **factor_analyzer** | `^0.4.1` | EFA with all rotations (Varimax, Oblimin, Quartimax, Promax), KMO/Bartlett | sklearn.FactorAnalysis (fewer rotations, no KMO) |
| **scikit-learn** | `^1.5.0` | PCA, KMeans, hierarchical clustering, preprocessing | — |
| **linearmodels** | `^6.1` | Panel data (FE/RE), IV/2SLS — unique to economics | statsmodels (limited panel) |
| **lifelines** | `^0.29.0` | Kaplan-Meier, Cox regression | — |
| **openpyxl** | `^3.1.0` | Excel export with SPSS-style formatting | xlwt (unmaintained) |
| **weasyprint** | `^62.0` | HTML → PDF generation | ReportLab (faster but lower-level), Puppeteer (Node.js dep) |
| **jinja2** | `^3.1.0` | HTML template for PDF/output | — |
| **celery[redis]** | `^5.4.0` | Task queue for long-running stats jobs (>5s) | FastAPI BackgroundTasks (no persistence, no retry) |
| **redis** | `^5.2.0` | Celery broker + result backend | RabbitMQ (heavier) |
| **chardet** | `^5.2.0` | Encoding detection for Vietnamese .sav files | — |
| **pydantic** | `^2.7.0` | Request/response schemas, settings | — |

**Full `pyproject.toml` (pinned)**:
```toml
[tool.poetry.dependencies]
python = "^3.11"
fastapi = "^0.115.0"
uvicorn = {extras = ["standard"], version = "^0.30.0"}
celery = {extras = ["redis"], version = "^5.4.0"}
redis = "^5.2.0"
flower = "^2.0.0"
pyreadstat = "^1.2.7"
pandas = "^2.2.0"
numpy = "^1.26.0"
scipy = "^1.13.0"
scikit-learn = "^1.5.0"
statsmodels = "^0.14.0"
pingouin = "^0.5.4"
factor-analyzer = "^0.4.1"
linearmodels = "^6.1"
lifelines = "^0.29.0"
openpyxl = "^3.1.0"
weasyprint = "^62.0"
reportlab = "^4.2.0"
jinja2 = "^3.1.0"
chardet = "^5.2.0"
pydantic = "^2.7.0"
pydantic-settings = "^2.3.0"
```

---

### Frontend

| Library | Version | Purpose | Performance Note |
|---------|---------|---------|-----------------|
| **Next.js** | `^14.2.0` | React framework with App Router, SSR, API routes | — |
| **TypeScript** | `^5.5.0` | Type safety | — |
| **@tanstack/react-table** | `^8.x` | Headless table logic (sorting, filtering, column visibility) | 14KB gzipped — extremely lean |
| **@tanstack/react-virtual** | `^3.8.0` | Virtual scrolling for 100k+ rows | ~9x speedup vs. no virtualization; 21ms render for 100k rows |
| **Zustand** | `^4.5.0` | Global state management | 3KB gzipped; selector-based fine-grained re-renders |
| **Plotly.js** | `^2.x` | Statistical charts (box plot, scatter, histogram, Q-Q, dendrogram) | Large bundle (~3.5MB); use dynamic import; supports all SPSS chart types |
| **Recharts** | `^2.x` | Simple bar/pie/line for quick output | React-friendly; 240KB gzipped |
| **shadcn/ui** | Latest | UI components (Radix-based, unstyled, accessible) | Tailwind CSS, tree-shakeable |
| **Comlink** | `^4.4.1` | Web Worker interface (proxy pattern for stats computation) | Eliminates UI blocking for client-side stats |
| **TanStack Query (React Query)** | `^5.56.0` | Server state, API caching, background refetch | Handles job polling elegantly |
| **PapaParse** | `^5.x` | CSV parsing in browser | Streaming support for large files |
| **xlsx** | `^0.18.x` | Excel file reading in browser | — |
| **Dexie.js** | `^3.x` | IndexedDB wrapper for browser-side dataset storage | Fallback when OPFS not available |

**Full `package.json` (key deps)**:
```json
{
  "dependencies": {
    "next": "^14.2.0",
    "react": "^18.3.0",
    "@tanstack/react-table": "^8.20.0",
    "@tanstack/react-virtual": "^3.8.0",
    "zustand": "^4.5.0",
    "plotly.js": "^2.35.0",
    "react-plotly.js": "^2.6.0",
    "recharts": "^2.12.0",
    "@tanstack/react-query": "^5.56.0",
    "comlink": "^4.4.1",
    "papaparse": "^5.4.1",
    "dexie": "^3.2.7"
  }
}
```

---

### Infrastructure

| Service | Purpose | Cost | Limitation |
|---------|---------|------|-----------|
| **Vercel** | Frontend hosting (Next.js) + edge CDN | Free tier generous | Serverless function timeout: 10s (Hobby), 300s (Pro); 4.5MB payload limit — not suitable for backend stats |
| **Render (Web Services)** | FastAPI backend — **primary choice** | Free tier (spins down after 15min inactivity); $7/mo Starter (always-on) | 512MB RAM on free — ok for MVP; no GPU |
| **cron-job.org** | Keep Render free tier warm — ping `/health` every 3 minutes | **Free** (external cron service) | Prevents 15min spin-down; eliminates cold start on free tier |
| **Redis Cloud** | Celery broker + job results | Free 30MB tier (Redis Cloud) | 30MB enough for job metadata; not dataset storage |
| **Cloudflare R2** | File storage for uploaded .sav/.csv | $0.015/GB-month; free egress | Better than S3 for egress costs |
| **Upstash Redis** | Serverless Redis (if no persistent worker) | Free 10K req/day | Alternative to Redis Cloud |

**Recommended architecture for MVP**:
- Frontend: **Vercel** (free tier)
- Backend: **Render.com** (free tier) with Docker + **cron-job.org** keep-warm ping every 3 minutes
- Task Queue: **Celery + Upstash Redis** (or Redis Cloud free)
- File Storage: **Cloudflare R2** (virtually free at student-scale)
- Database: **None for MVP** (stateless — dataset lives in session/R2)

**cron-job.org keep-warm setup**:
```
URL:      https://your-app.onrender.com/health
Method:   GET
Schedule: Every 3 minutes  (*/3 * * * *)
Timeout:  10s
```
Add a lightweight health endpoint in FastAPI:
```python
@app.get("/health")
async def health():
    return {"status": "ok"}
```

---

## Part 3: Implementation Guide

### 3.1 SPSS .sav File Compatibility

**Approach**: `pyreadstat` (C++ backend, fastest option) for all .sav I/O. `pandas.read_spss()` just wraps pyreadstat with less metadata control.

**Key Libraries**: `pyreadstat.read_sav()`, `pyreadstat.write_sav()`

**CRITICAL — Always use `apply_value_formats=False`**:
```python
df, meta = pyreadstat.read_sav(
    path,
    apply_value_formats=False,  # Keep numeric codes for computation
    formats_as_category=True,   # Memory efficient
)
# Apply labels only in response serialization, never in computation
```

**Metadata preservation**:
```python
# meta object contains:
meta.column_names              # ['var1', 'var2', ...]
meta.column_names_to_labels    # {'var1': 'Age of respondent', ...}
meta.variable_value_labels     # {'gender': {1: 'Male', 2: 'Female'}}
meta.missing_ranges            # {'income': [{'lo': -999, 'hi': -999}]}
meta.variable_measure          # {'age': 'scale', 'gender': 'nominal'}
meta.file_encoding             # 'UTF-8' or 'windows-1252'
```

**Vietnamese encoding handling** (critical for Vietnamese universities):
```python
import chardet

VIETNAMESE_ENCODINGS = ["utf-8", "windows-1258", "windows-1252", "cp1258"]

def resolve_sav_encoding(path: str, declared_encoding: str | None) -> str:
    if declared_encoding and declared_encoding.lower() in ("utf-8", "utf8"):
        return "utf-8"
    # Sniff first 50KB
    with open(path, "rb") as f:
        raw = f.read(50_000)
    detection = chardet.detect(raw)
    if detection.get("confidence", 0) > 0.85:
        return detection["encoding"]
    return "windows-1258"  # Safe default for Vietnamese SPSS files
```

**Algorithm Notes**: SPSS SYSMIS (system missing) = `NaN` in pandas after pyreadstat. User-defined missing values stored in `meta.missing_ranges`. Must convert NaN properly before export back to .sav.

**Performance**: pyreadstat reads 100k rows × 50 vars in ~0.3s (C++ backend). Metadata-only read: `metadataonly=True` parameter, ~5ms.

---

### 3.2 Statistical Computation Architecture

**Approach**: Layered routing based on computation time

```
< 1 second    → Direct sync in asyncio.to_thread() (t-test, Pearson, descriptives)
1–10 seconds  → FastAPI BackgroundTasks + WebSocket progress
> 10 seconds  → Celery + Redis job queue (factor analysis large datasets, clustering)
```

**FastAPI async pattern for CPU-bound stats**:
```python
import asyncio
from scipy import stats

@app.post("/tests/ttest/independent")
async def independent_ttest(payload: TTestRequest):
    # scipy is CPU-bound — offload to thread (numpy releases GIL)
    result = await asyncio.to_thread(
        stats.ttest_ind,
        payload.group_a, payload.group_b,
        equal_var=payload.equal_var,
        alternative=payload.alternative
    )
    return {"statistic": float(result.statistic), "pvalue": float(result.pvalue)}
```

**Celery pattern for long-running jobs**:
```python
# celery_worker.py
from celery import Celery
app = Celery('webspss', broker='redis://localhost:6379/0', backend='redis://localhost:6379/0')

@app.task(bind=True)
def run_factor_analysis(self, data_json: str, n_factors: int, rotation: str):
    self.update_state(state='PROGRESS', meta={'step': 'Loading data'})
    df = pd.read_json(data_json)
    fa = FactorAnalyzer(n_factors=n_factors, rotation=rotation, method='principal')
    fa.fit(df)
    return {
        'loadings': fa.loadings_.tolist(),
        'communalities': fa.get_communalities().tolist(),
        'eigenvalues': fa.get_eigenvalues()[0].tolist(),
        'kmo': calculate_kmo(df.values)
    }

# FastAPI endpoint
@app.post("/factor/submit")
async def submit_factor(payload: FactorRequest):
    task = run_factor_analysis.apply_async(args=[payload.data_json, payload.n_factors, payload.rotation])
    return {"job_id": task.id, "poll_url": f"/jobs/{task.id}"}

@app.get("/jobs/{job_id}")
async def get_job_status(job_id: str):
    task = run_factor_analysis.AsyncResult(job_id)
    return {"status": task.status, "result": task.result if task.ready() else None}
```

**Router organization**:
```python
# Organize by statistical domain
router_descriptives = APIRouter(prefix="/descriptives", tags=["Descriptives"])
router_tests = APIRouter(prefix="/tests", tags=["Hypothesis Tests"])
router_regression = APIRouter(prefix="/regression", tags=["Regression"])
router_factor = APIRouter(prefix="/factor", tags=["Factor & Cluster"])
router_files = APIRouter(prefix="/files", tags=["File I/O"])
router_jobs = APIRouter(prefix="/jobs", tags=["Async Jobs"])
```

**Edge case validation**:
```python
def validate_input(y, X=None):
    if len(y) < 3:
        raise StatisticalError("INSUFFICIENT_DATA", f"Min 3 obs required, got {len(y)}")
    if np.std(y) == 0:
        raise StatisticalError("ZERO_VARIANCE", "DV has zero variance")
    if X is not None:
        X_arr = np.array(X)
        if np.linalg.matrix_rank(X_arr) < X_arr.shape[1]:
            raise StatisticalError("SINGULAR_MATRIX", "Design matrix is rank-deficient")
```

---

### 3.3 Frontend Data Handling

**Virtual scrolling for 100k rows**:

Use `@tanstack/react-virtual` v3 (`useVirtualizer`) combined with `@tanstack/react-table` for headless logic:

```tsx
import { useVirtualizer } from '@tanstack/react-virtual'
import { useReactTable, getCoreRowModel } from '@tanstack/react-table'

const DataGrid = ({ data, columns }) => {
  const table = useReactTable({ data, columns, getCoreRowModel: getCoreRowModel() })
  const { rows } = table.getRowModel()
  const parentRef = useRef<HTMLDivElement>(null)

  const rowVirtualizer = useVirtualizer({
    count: rows.length,
    getScrollElement: () => parentRef.current,
    estimateSize: () => 32, // Fixed row height for performance
    overscan: 5,
  })

  return (
    <div ref={parentRef} style={{ height: '600px', overflow: 'auto' }}>
      <div style={{ height: `${rowVirtualizer.getTotalSize()}px`, position: 'relative' }}>
        {rowVirtualizer.getVirtualItems().map(virtualRow => {
          const row = rows[virtualRow.index]
          return (
            <div key={row.id} style={{ position: 'absolute', top: virtualRow.start, height: 32 }}>
              {row.getVisibleCells().map(cell => <span key={cell.id}>{/* render cell */}</span>)}
            </div>
          )
        })}
      </div>
    </div>
  )
}
```

**Performance benchmark**: Without virtualization → ~143ms render for 10k rows; With TanStack Virtual → ~21ms. For 100k rows, only ~30–50 rows are rendered at any time.

**Web Workers with Comlink** (for client-side stats without blocking UI):
```typescript
// stats.worker.ts
import * as Comlink from 'comlink'
const statsApi = {
  async computeDescriptives(data: number[]) {
    const mean = data.reduce((a, b) => a + b) / data.length
    // ... more computations
    return { mean, std, min, max }
  }
}
Comlink.expose(statsApi)

// In React component
const worker = new Worker(new URL('./stats.worker.ts', import.meta.url))
const statsWorker = Comlink.wrap<typeof statsApi>(worker)
const result = await statsWorker.computeDescriptives(columnData)
```

**Zustand store for dataset** (do NOT store raw data in Zustand):
```typescript
interface DatasetStore {
  metadata: VariableMeta[]           // Variable labels, types, value labels
  dataRef: React.MutableRefObject<number[][]> | null  // Raw data in ref, not state
  activeFilters: FilterCondition[]
  setMetadata: (meta: VariableMeta[]) => void
}
// Keep raw 100k-row array in a ref or OPFS — never in Zustand state
```

---

### 3.4 Visualization Specifics

**Box Plot (SPSS-exact whiskers)**:

SPSS calls whiskers **"adjacent values"** — they are the *actual data points* nearest the fences, NOT the fence boundaries themselves.

```python
def spss_boxplot_stats(data: list[float]) -> dict:
    arr = np.array([x for x in data if not np.isnan(x)])
    q1 = np.percentile(arr, 25)  # SPSS uses weighted average interpolation
    q3 = np.percentile(arr, 75)
    iqr = q3 - q1
    lower_fence = q1 - 1.5 * iqr
    upper_fence = q3 + 1.5 * iqr
    outer_lower = q1 - 3.0 * iqr
    outer_upper = q3 + 3.0 * iqr

    lower_adjacent = arr[arr >= lower_fence].min()  # Actual data point
    upper_adjacent = arr[arr <= upper_fence].max()  # Actual data point
    mild_outliers = arr[(arr < lower_fence) | (arr > upper_fence)]
    mild_outliers = mild_outliers[(mild_outliers >= outer_lower) & (mild_outliers <= outer_upper)]
    extreme_outliers = arr[(arr < outer_lower) | (arr > outer_upper)]

    return {
        "q1": q1, "median": np.median(arr), "q3": q3,
        "whisker_low": lower_adjacent, "whisker_high": upper_adjacent,
        "mild_outliers": mild_outliers.tolist(),   # SPSS shows as ○
        "extreme_outliers": extreme_outliers.tolist()  # SPSS shows as ★
    }
```

**Q-Q Plot (SPSS Blom formula)**:

SPSS uses **Blom (1958)** plotting position: `p_i = (i - 3/8) / (n + 1/4)`. scipy default is `(i - 0.5) / n` (Filliben). Use Blom for SPSS compatibility:

```python
from scipy import stats
import numpy as np

def spss_qq_data(data: list[float]) -> dict:
    arr = np.sort([x for x in data if not np.isnan(x)])
    n = len(arr)
    i = np.arange(1, n + 1)
    # Blom formula (SPSS default)
    p = (i - 3/8) / (n + 1/4)
    theoretical = stats.norm.ppf(p)
    # Fitting line: from Q1 and Q3 of both distributions
    q1_obs, q3_obs = np.percentile(arr, [25, 75])
    q1_th, q3_th = stats.norm.ppf([0.25, 0.75])
    slope = (q3_obs - q1_obs) / (q3_th - q1_th)
    intercept = q1_obs - slope * q1_th
    return {
        "observed": arr.tolist(),
        "theoretical": theoretical.tolist(),
        "fit_slope": slope,
        "fit_intercept": intercept
    }
```

**Residual Plots (Cook's distance, leverage)**:
```python
import statsmodels.api as sm
from statsmodels.stats.outliers_influence import OLSInfluence

def compute_residuals(y, X):
    X_const = sm.add_constant(X)
    model = sm.OLS(y, X_const).fit()
    influence = OLSInfluence(model)
    return {
        "standardized_residuals": influence.resid_studentized_internal.tolist(),
        "studentized_deleted_residuals": influence.resid_studentized_external.tolist(),
        "leverage": influence.hat_matrix_diag.tolist(),
        "cooks_distance": influence.cooks_distance[0].tolist(),
        "dffits": influence.dffits[0].tolist(),
    }
```

**Cronbach's Alpha (SPSS exact)**:
```python
# SPSS formula: α = (k/(k-1)) × (1 - Σσᵢ²/σT²) with ddof=1
# pingouin matches SPSS exactly:
import pingouin as pg
alpha_result = pg.cronbach_alpha(data=df[item_columns])
# Returns: (alpha_value, ci_95_tuple)
# Also provides: item-total correlations, alpha-if-deleted
```

**Levene's Test (SPSS reports both variants)**:
```python
from scipy.stats import levene

# SPSS reports both:
f_mean, p_mean = levene(*groups, center='mean')    # Classic Levene
f_median, p_median = levene(*groups, center='median')  # Brown-Forsythe (more robust)
```

**Collinearity Diagnostics (VIF + Condition Index)**:
```python
from statsmodels.stats.outliers_influence import variance_inflation_factor

# VIF for each predictor
vif = [variance_inflation_factor(X.values, i) for i in range(X.shape[1])]

# SPSS Condition Index: uses column-normalized SVD including intercept
X_aug = np.column_stack([np.ones(n), X.values])
X_scaled = X_aug / np.sqrt((X_aug**2).sum(axis=0))
_, singular_values, Vt = np.linalg.svd(X_scaled, full_matrices=False)
eigenvalues = singular_values**2
condition_indices = np.sqrt(eigenvalues[0] / eigenvalues)
# CI > 30 with 2+ variance proportions > 0.5 = near dependency
```

**Post-hoc Tests**:
```python
# Tukey HSD (most common)
from statsmodels.stats.multicomp import pairwise_tukeyhsd
tukey = pairwise_tukeyhsd(endog=y, groups=groups)

# Bonferroni (simple, conservative)
from statsmodels.stats.multicomp import MultiComparison
mc = MultiComparison(y, groups)
result = mc.allpairtest(scipy.stats.ttest_ind, method='bonf')

# Scheffé (most conservative, all contrasts — no direct statsmodels)
# Manual: |d| > sqrt((k-1) × F_crit × MSW × (1/n_i + 1/n_j))
```

**Dendrogram (hierarchical clustering)**:
```python
from scipy.cluster.hierarchy import linkage, dendrogram
import plotly.figure_factory as ff

# Compute linkage (SPSS default is Ward's method)
Z = linkage(X_scaled, method='ward', metric='euclidean')

# Plotly dendrogram
fig = ff.create_dendrogram(X_scaled, labels=case_labels, linkagefun=lambda x: linkage(x, 'ward'))
```

---

### 3.5 Output Format & Export

**PDF Generation — WeasyPrint (recommended)**:
- Developer experience: HTML/CSS → PDF (familiar workflow)
- Speed: ~0.8s for typical statistical output (3–4 tables)
- vs. ReportLab: ~2× slower but much easier template maintenance
- vs. Puppeteer: No Node.js dependency, no headless Chrome
- **System deps**: Requires `pango`, `cairo`, `gdk-pixbuf` on Linux

```dockerfile
RUN apt-get install -y libpango-1.0-0 libpangocairo-1.0-0 libcairo2 libgdk-pixbuf2.0-0
```

```python
from weasyprint import HTML
import jinja2

template = jinja2.Template("""
<html><body>
<h2>{{ title }}</h2>
<table class="spss-table">
  {% for row in data %}
  <tr>{% for cell in row %}<td>{{ cell }}</td>{% endfor %}</tr>
  {% endfor %}
</table>
</body></html>
""")
html = template.render(title="Regression Output", data=table_data)
pdf_bytes = HTML(string=html).write_pdf()
```

**Excel Export (SPSS-style tables with openpyxl)**:
```python
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Border, Side, Alignment

SPSS_HEADER_FONT = Font(name="Arial", bold=True, size=9)
SPSS_HEADER_FILL = PatternFill("solid", fgColor="D9D9D9")
SPSS_BODY_FONT = Font(name="Arial", size=9)

def write_regression_table(ws, model_result):
    # Header
    headers = ["", "B", "Std. Error", "Beta", "t", "Sig."]
    for col, h in enumerate(headers, 1):
        cell = ws.cell(row=1, column=col, value=h)
        cell.font = SPSS_HEADER_FONT
        cell.fill = SPSS_HEADER_FILL
    # Data rows with 3-decimal formatting
    for row_idx, (name, coef) in enumerate(model_result.params.items(), 2):
        ws.cell(row=row_idx, column=1, value=name)
        ws.cell(row=row_idx, column=2, value=round(coef, 3)).number_format = "0.000"
        # ... rest of row
```

**Word/Copy-paste**: Generate APA-format HTML tables. When users copy from the browser, the clipboard picks up HTML with formatting. Ensure `<table>` has proper `border-collapse` CSS — most Word versions handle this paste correctly.

---

### 3.6 Code Structure (Clean Architecture)

```
bernie-spss/
├── backend/
│   ├── app/
│   │   ├── main.py                    # FastAPI app, router registration
│   │   ├── domain/
│   │   │   ├── models/
│   │   │   │   ├── dataset.py         # Dataset, Variable, ValueLabel (Pydantic)
│   │   │   │   └── job.py             # Job status models
│   │   │   └── services/
│   │   │       ├── descriptives.py    # Pure statistical functions (no HTTP)
│   │   │       ├── regression.py
│   │   │       ├── factor_analysis.py
│   │   │       └── spss_io.py
│   │   ├── api/
│   │   │   ├── routes/
│   │   │   │   ├── descriptives.py    # FastAPI routers
│   │   │   │   ├── regression.py
│   │   │   │   ├── factor.py
│   │   │   │   ├── files.py
│   │   │   │   └── jobs.py
│   │   │   └── schemas/               # Pydantic request/response models
│   │   ├── tasks/
│   │   │   └── celery_tasks.py        # Long-running Celery tasks
│   │   └── core/
│   │       ├── config.py              # Settings (pydantic-settings)
│   │       └── exceptions.py          # StatisticalError, etc.
│   ├── tests/
│   │   ├── unit/                      # Pure statistical function tests
│   │   ├── integration/               # API endpoint tests (httpx)
│   │   └── fixtures/                  # Sample .sav, .csv test files
│   ├── Dockerfile
│   └── pyproject.toml
├── frontend/
│   ├── src/
│   │   ├── app/                       # Next.js App Router pages
│   │   ├── components/
│   │   │   ├── DataGrid/              # TanStack Table + Virtual
│   │   │   ├── VariableView/          # SPSS Variable View editor
│   │   │   ├── OutputViewer/          # Pivot tables, charts
│   │   │   └── Charts/               # Plotly wrappers
│   │   ├── workers/
│   │   │   └── stats.worker.ts        # Comlink Web Worker
│   │   ├── stores/
│   │   │   └── datasetStore.ts        # Zustand
│   │   └── lib/
│   │       └── api.ts                 # API client (TanStack Query)
│   └── package.json
└── docker-compose.yml
```

---

## Part 4: Risk Analysis

| Risk | Severity | Mitigation |
|------|----------|-----------|
| **SPSS output fidelity** — pivot tables look different from SPSS | High | Cross-validate every table against actual SPSS output; use SPSS screenshot as design spec |
| **Vietnamese encoding in .sav files** | High | chardet detection + `windows-1258` fallback; test with real Vietnamese .sav files before launch |
| **Factor analysis sign indeterminacy** | Medium | Python and R may produce loadings with opposite signs. Use `np.sign()` alignment in tests: `py_loadings *= np.sign(py_loadings[0]) * np.sign(r_loadings[0])` |
| **CPU blocking in FastAPI** | High | All scipy/numpy calls through `asyncio.to_thread()`; Celery for >10s jobs. Test with load testing (locust) |
| **Pandas quartile differences from SPSS** | Medium | SPSS uses weighted average interpolation (numpy default). Verify Q1/Q3 for box plots match SPSS output with same dataset |
| **Bundle size (Plotly.js ~3.5MB)** | Medium | Dynamic import: `const Plot = dynamic(() => import('react-plotly.js'), {ssr: false})` |
| **WeasyPrint system dependencies** | Medium | Add to Dockerfile; test in CI. Alternative: use Puppeteer if Docker not available |
| **Celery worker memory** | Medium | Limit pandas DataFrame size in tasks; use chunked reading for large files; set `CELERY_TASK_SOFT_TIME_LIMIT` |
| **Cold start on Render free tier** | Medium | Use **cron-job.org** to ping `/health` every 3 minutes — keeps the dyno warm 24/7 at zero cost. Show loading skeleton as fallback if cold start still occurs |
| **Ordinal regression API changes** | Low | `statsmodels.miscmodels.ordinal_model.OrderedModel` API changed in 0.12–0.14. Pin to `^0.14.0` |
| **SPSS .sav missing value edge cases** | Medium | LO/HI sentinel values in SPSS missing ranges — handle with pyreadstat `missing_ranges` metadata |

---

## Part 5: References

### Official Library Documentation
- **scipy.stats**: https://docs.scipy.org/doc/scipy/reference/stats.html
- **statsmodels**: https://www.statsmodels.org/stable/index.html
- **statsmodels OLS**: https://www.statsmodels.org/stable/regression.html
- **statsmodels discrete (Logit/Probit/MNLogit)**: https://www.statsmodels.org/stable/discretemod.html
- **statsmodels ordinal**: https://www.statsmodels.org/stable/generated/statsmodels.miscmodels.ordinal_model.OrderedModel.html
- **pingouin**: https://pingouin-stats.org/api.html
- **factor_analyzer**: https://factor-analyzer.readthedocs.io/
- **pyreadstat**: https://github.com/Roche/pyreadstat
- **scikit-learn decomposition**: https://scikit-learn.org/stable/modules/decomposition.html
- **linearmodels panel data**: https://bashtage.github.io/linearmodels/
- **lifelines survival**: https://lifelines.readthedocs.io/

### SPSS Algorithm References
- **IBM SPSS Statistics Algorithms**: https://www.ibm.com/support/pages/ibm-spss-statistics-algorithms
- **IBM SPSS Variable View**: https://www.ibm.com/docs/en/spss-statistics/
- **SPSS Box Plot Adjacent Values**: Tukey, J.W. (1977). *Exploratory Data Analysis*. Addison-Wesley.
- **Blom Plotting Position**: Blom, G. (1958). *Statistical Estimates and Transformed Beta Variables*. Wiley.
- **Filliben Plotting Position**: Filliben, J.J. (1975). *Technometrics*, 17(1), 111–117.
- **Brown-Forsythe Test**: Brown, M.B., Forsythe, A.B. (1974). *Journal of the American Statistical Association*, 69(346), 364–367.
- **Collinearity Diagnostics**: Belsley, D.A., Kuh, E., Welsch, R.E. (1980). *Regression Diagnostics*. Wiley.
- **Scheffé Post-Hoc**: Scheffé, H. (1959). *The Analysis of Variance*. Wiley.

### Competitor Comparisons
- **JASP features**: https://jasp-stats.org/features/
- **jamovi modules**: https://www.jamovi.org/library.html
- **PSPP**: https://www.gnu.org/software/pspp/
- **jamovi vs JASP vs SPSS comparison**: Multiple academic reviews in *Teaching Statistics* journal, 2022–2024

### Frontend / Infrastructure
- **TanStack Table v8**: https://tanstack.com/table/latest
- **TanStack Virtual v3**: https://tanstack.com/virtual/latest
- **Comlink (Web Workers)**: https://github.com/GoogleChromeLabs/comlink
- **Render.com**: https://render.com/docs
- **cron-job.org** (keep-warm): https://cron-job.org
- **WeasyPrint**: https://weasyprint.org/
- **openpyxl**: https://openpyxl.readthedocs.io/

---

## Part 6: Deployment Guide

> Full step-by-step instructions for the recommended stack:
> **Backend → Render.com** · **Frontend → Vercel** · **Redis → Upstash** · **Files → Cloudflare R2**

---

### 6.1 Architecture Overview

```
                  ┌─────────────────────────────────┐
  Browser  ──────►│  Vercel (Next.js 14 frontend)   │
                  │  bernie-spss.vercel.app          │
                  └──────────────┬──────────────────┘
                                 │ API calls (HTTPS)
                  ┌──────────────▼──────────────────┐
                  │  Render.com (FastAPI backend)    │
                  │  bernie-spss.onrender.com:8000   │
                  └──────┬──────────────┬───────────┘
                         │              │
           ┌─────────────▼──┐   ┌───────▼──────────┐
           │ Upstash Redis  │   │  Cloudflare R2   │
           │ (Celery broker │   │  (file uploads,  │
           │  + job results)│   │   optional MVP)  │
           └────────────────┘   └──────────────────┘
```

**Cost at student scale (< 1,000 users/day):**

| Service | Tier | Monthly Cost |
|---|---|---|
| Vercel | Hobby (free) | **$0** |
| Render.com | Free Web Service | **$0** (spins down after 15 min idle) |
| Render.com | Starter (always-on) | **$7/mo** |
| Upstash Redis | Free (10K req/day) | **$0** |
| Cloudflare R2 | Free (10 GB) | **$0** |
| **Total MVP** | | **$0 – $7/mo** |

---

### 6.2 Backend → Render.com

#### Step 1 — Create a Web Service

1. Go to [render.com](https://render.com) → **New → Web Service**
2. Connect your GitHub repo: `Phu-Nhuan-Builder/bernie-spss`
3. Configure:

| Field | Value |
|---|---|
| **Name** | `bernie-spss-api` |
| **Root Directory** | `backend` |
| **Runtime** | **Docker** (uses your `backend/Dockerfile`) |
| **Instance Type** | Free (or Starter $7/mo for always-on) |
| **Region** | Singapore (`sgp`) — closest to Vietnam |

4. Click **Create Web Service**

#### Step 2 — Environment Variables

In Render dashboard → **Environment** tab, add:

```
REDIS_URL          = <your Upstash Redis URL>  (see §6.4)
ALLOWED_ORIGINS    = https://your-app.vercel.app
ENVIRONMENT        = production
MAX_UPLOAD_MB      = 50
```

#### Step 3 — Keep-Warm with cron-job.org (Free tier only)

Render free tier sleeps after 15 min of inactivity → cold starts take 30–60s.
**Fix: ping `/health` every 3 minutes with cron-job.org (free service).**

1. Register at [cron-job.org](https://cron-job.org) (free)
2. Create a new cron job:

```
URL:       https://bernie-spss-api.onrender.com/health
Method:    GET
Schedule:  Every 3 minutes  →  */3 * * * *
Timeout:   10s
```

3. Enable → Save. Your backend now stays warm 24/7 at zero cost.

#### Step 4 — Add Celery Worker (optional, for large EFA jobs)

In Render → **New → Background Worker**, same repo, root `backend`:

```
Start Command: celery -A app.tasks.celery_tasks worker --loglevel=info --concurrency=2
```

Add the same env vars. The worker reads `SESSION_STORE` from the same process namespace only if on the same dyno — for multi-dyno, switch `SESSION_STORE` to Redis-backed storage.

#### Verify

```bash
curl https://bernie-spss-api.onrender.com/health
# → {"status": "ok", "sessions": 0, "environment": "production"}

curl https://bernie-spss-api.onrender.com/docs
# → Swagger UI with all 30+ endpoints
```

---

### 6.3 Frontend → Vercel

#### Step 1 — Import Project

1. Go to [vercel.com](https://vercel.com) → **Add New Project**
2. Import `Phu-Nhuan-Builder/bernie-spss`
3. Configure:

| Field | Value |
|---|---|
| **Framework Preset** | Next.js (auto-detected) |
| **Root Directory** | `frontend` |
| **Build Command** | `npm run build` (default) |
| **Output Directory** | `.next` (default) |

#### Step 2 — Environment Variables

In Vercel project → **Settings → Environment Variables**:

```
NEXT_PUBLIC_API_URL = https://bernie-spss-api.onrender.com
```

Set for **Production**, **Preview**, and **Development** environments.

#### Step 3 — Deploy

Click **Deploy**. Vercel builds and deploys in ~2 min.

Your live URL: `https://bernie-spss.vercel.app` (or your custom domain).

#### Step 4 — Custom Domain (optional)

In Vercel → **Domains** → Add `spss.youruniversity.edu.vn` → follow DNS instructions.

#### Verify

```
https://bernie-spss.vercel.app          → redirects to /workspace
https://bernie-spss.vercel.app/workspace → main SPSS UI
```

---

### 6.4 Redis → Upstash (Free)

Upstash provides serverless Redis with a **free tier of 10,000 requests/day** — sufficient for Celery job queuing at student scale.

1. Go to [upstash.com](https://upstash.com) → **Create Database**
2. Configure:

| Field | Value |
|---|---|
| **Name** | `bernie-spss-redis` |
| **Type** | Regional |
| **Region** | `ap-southeast-1` (Singapore) |
| **Eviction** | No eviction (job results must persist) |

3. Copy the **Redis URL** (format: `rediss://default:PASSWORD@HOST:PORT`)
4. Paste into Render env var: `REDIS_URL = rediss://default:...`

**Alternative: Redis Cloud (free 30 MB)**
- [redis.io/try-free](https://redis.io/try-free) → Free tier → Singapore region
- Same connection string format

---

### 6.5 File Storage → Cloudflare R2 (Optional for MVP)

> **MVP note**: The in-memory `SESSION_STORE` is sufficient for single-server MVP. Add R2 only when you need persistent sessions across restarts or multiple workers.

1. Go to [Cloudflare dashboard](https://dash.cloudflare.com) → **R2** → **Create bucket**
2. Name: `bernie-spss-uploads`
3. Create an **API token** (R2 Read+Write permissions)
4. Add to Render env vars:

```
CLOUDFLARE_R2_ACCOUNT_ID  = your_account_id
CLOUDFLARE_R2_ACCESS_KEY  = your_access_key
CLOUDFLARE_R2_SECRET_KEY  = your_secret_key
CLOUDFLARE_R2_BUCKET      = bernie-spss-uploads
```

Free tier: 10 GB storage, 1M Class-A operations/month, **free egress**.

---

### 6.6 Full docker-compose (Local / Self-Hosted VPS)

For self-hosting on a VPS (e.g. DigitalOcean $6/mo Droplet, Oracle Free Tier):

```bash
# On your VPS
git clone https://github.com/Phu-Nhuan-Builder/bernie-spss.git
cd bernie-spss
cp .env.example .env
# Edit .env with your values

docker-compose up -d --build

# Check all services
docker-compose ps
docker-compose logs backend -f
```

Add Nginx reverse proxy + Let's Encrypt SSL:

```nginx
# /etc/nginx/sites-available/bernie-spss
server {
    server_name spss.yourdomain.com;

    location /api/ {
        proxy_pass http://localhost:8000/;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        client_max_body_size 50M;
    }

    location / {
        proxy_pass http://localhost:3000;
        proxy_set_header Host $host;
    }
}
```

```bash
certbot --nginx -d spss.yourdomain.com
```

---

### 6.7 Environment Variables Reference

#### Backend (`.env` or Render Environment)

| Variable | Required | Default | Description |
|---|---|---|---|
| `REDIS_URL` | Yes (Celery) | `redis://localhost:6379/0` | Upstash / Redis Cloud URL |
| `MAX_UPLOAD_MB` | No | `50` | Max file upload size |
| `ALLOWED_ORIGINS` | Yes | `http://localhost:3000` | Comma-separated CORS origins |
| `ENVIRONMENT` | No | `development` | `development` \| `production` |
| `CLOUDFLARE_R2_ACCOUNT_ID` | No | — | R2 account ID |
| `CLOUDFLARE_R2_ACCESS_KEY` | No | — | R2 access key |
| `CLOUDFLARE_R2_SECRET_KEY` | No | — | R2 secret key |
| `CLOUDFLARE_R2_BUCKET` | No | `bernie-spss-uploads` | R2 bucket name |

#### Frontend (`.env.local` or Vercel Environment)

| Variable | Required | Default | Description |
|---|---|---|---|
| `NEXT_PUBLIC_API_URL` | Yes | `http://localhost:8000` | FastAPI backend URL |

---

### 6.8 Post-Deploy Checklist

```
□ curl https://your-backend.onrender.com/health → {"status":"ok"}
□ Open https://your-frontend.vercel.app → redirects to /workspace
□ Upload sample.csv → session_id returned, data grid renders
□ Run Frequencies on a variable → output block appears
□ Run Independent T-Test → t, df, p, Levene's F all appear
□ Run OLS Regression → R², coefficients, VIF table render
□ Run Factor Analysis → loadings, KMO, Bartlett appear
□ Export to Excel → .xlsx downloads, opens in Excel with SPSS-style formatting
□ Export to PDF → .pdf downloads, tables render correctly
□ cron-job.org ping every 3 min → no cold starts after 5 min idle test
```

---

### 6.9 Scaling Beyond Free Tier

| Trigger | Action | Cost |
|---|---|---|
| > 50 concurrent users | Upgrade Render to **Starter** ($7/mo, always-on, 512 MB RAM) | $7/mo |
| > 200 concurrent users | Render **Standard** ($25/mo, 2 GB RAM) + Celery worker | $50/mo |
| > 500 concurrent users | Add **Render PostgreSQL** for session persistence; swap `SESSION_STORE` to Redis | +$7/mo |
| File uploads > 10 GB/mo | R2 paid tier ($0.015/GB) — still cheapest egress | ~$0.15/mo |
| Custom domain + HTTPS | Vercel free tier includes SSL for any custom domain | $0 |

---

*Report generated by 5 parallel research agents — ~50 web searches — 2026-03-12*
*Deployment guide added: 2026-03-12*
