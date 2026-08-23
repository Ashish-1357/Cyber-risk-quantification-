# Architecture Documentation

## System Architecture

```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│     Client      │────▶│   Nginx (80)    │────▶│  FastAPI (8000) │
│  (HTML/JS)      │     │  Reverse Proxy  │     │   REST API      │
└─────────────────┘     └─────────────────┘     └─────────────────┘
                                                        │
                        ┌─────────────────┐            │
                        │   Plotly.js     │◀───────────┘
                        │  (CDN/Local)    │   JSON Response
                        └─────────────────┘
```

## Backend Architecture

```
main.py
  ├── API Router (/api/v1)
  │     ├── /health
  │     ├── /assets
  │     ├── /vulnerabilities
  │     ├── /risk/scenarios
  │     ├── /controls
  │     ├── /optimize
  │     └── /dashboard
  ├── Engines (Business Logic)
  │     ├── AssetEngine
  │     ├── VulnerabilityEngine
  │     ├── FAIREngine
  │     ├── ControlCatalog
  │     └── InvestmentOptimizer
  └── Models (Pydantic Schemas)
```

## Data Flow

1. **Asset Simulation** → Generates synthetic enterprise asset inventory
2. **Vulnerability Discovery** → Creates vulnerability findings per asset
3. **FAIR Quantification** → Runs Monte Carlo on 6 risk scenarios
4. **Control Catalog** → Loads 20 controls with cost models
5. **Optimization** → Selects optimal control portfolio
6. **Dashboard** → Aggregates all data for visualization

## Technology Decisions

| Decision | Rationale |
|----------|-----------|
| FastAPI over Flask/Django | Async support, auto-docs, Pydantic integration |
| Vanilla JS over React/Vue | Zero build step, faster load, simpler deployment |
| Plotly.js over D3 | Higher-level API, faster development, interactive |
| FAIR over custom model | Industry standard, defensible, well-documented |
| Greedy over MILP | Sufficient for demo, no external solver dependency |
