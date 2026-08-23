# 🔒 AI-Powered Cyber Risk Quantification & Investment Optimization Platform

**Open Source Edition | Zero Licensing Costs | Production-Ready**

A complete, full-stack enterprise cybersecurity platform that continuously quantifies cyber risk in financial terms and optimizes security investment decisions using AI/ML — built entirely with free and open-source technologies.

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python](https://img.shields.io/badge/python-3.12-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.111.0-009688.svg)

---

## 🚀 Features

- **FAIR Risk Quantification** — Monte Carlo simulation (50,000 iterations) for probabilistic risk analysis
- **Asset Discovery** — Enterprise asset inventory with business context and revenue impact
- **Vulnerability Scoring** — Contextual risk scoring combining CVSS, EPSS, and asset criticality
- **Control Catalog** — 20 security controls with full TCO models and effectiveness scores
- **Investment Optimization** — Constrained portfolio optimization maximizing risk reduction per dollar
- **Interactive Dashboard** — Real-time visualizations with Plotly.js
- **REST API** — Full FastAPI backend with auto-generated OpenAPI docs
- **Scenario Analysis** — What-if analysis across budget ranges
- **Pareto Frontier** — Risk vs investment trade-off visualization

---

## 📁 Project Structure

```
cyber-risk-platform/
├── client/                     # Frontend (Vanilla JS + Plotly)
│   ├── index.html             # Main dashboard
│   ├── src/
│   │   ├── app.js             # Application logic
│   │   └── styles.css         # Styles
│   └── public/                # Static assets
├── server/                     # Backend (FastAPI + Python)
│   ├── app/
│   │   ├── core/              # Config, logging
│   │   ├── models/            # Pydantic schemas
│   │   ├── engines/           # Risk engines
│   │   │   ├── asset_engine.py
│   │   │   ├── vulnerability_engine.py
│   │   │   ├── fair_engine.py
│   │   │   ├── control_catalog.py
│   │   │   └── optimizer.py
│   │   ├── api/               # API routes
│   │   └── utils/             # Utilities
│   ├── tests/                 # Pytest test suite
│   ├── main.py                # FastAPI application
│   ├── requirements.txt       # Python dependencies
│   ├── Dockerfile             # Container image
│   └── .env                   # Environment variables
├── docker-compose.yml         # Docker orchestration
├── nginx.conf                 # Nginx reverse proxy config
├── scripts/                   # Helper scripts
├── docs/                      # Documentation
├── .gitignore
└── README.md
```

---

## 🛠️ Quick Start

### Option 1: Local Development (Python)

```bash
# Clone the repository
git clone <repo-url>
cd cyber-risk-platform

# Start backend
cd server
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload --host 0.0.0.0 --port 8000

# Open client (in new terminal)
cd ../client
# Serve with any static server, e.g.:
python -m http.server 5500
# Or open index.html directly in browser
```

### Option 2: Docker (Recommended for Production)

```bash
# Start all services
docker-compose up -d

# Access the platform
# Dashboard: http://localhost
# API: http://localhost/api/v1
# API Docs: http://localhost/api/docs
```

### Option 3: Docker (Development)

```bash
# Server only
cd server
docker build -t cyber-risk-server .
docker run -p 8000:8000 cyber-risk-server

# Client (any static file server)
cd client
python -m http.server 5500
```

---

## 📊 API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/v1/health` | Health check |
| GET | `/api/v1/assets` | List assets |
| GET | `/api/v1/assets/summary` | Asset summary |
| GET | `/api/v1/vulnerabilities` | List vulnerabilities |
| GET | `/api/v1/vulnerabilities/summary` | Vulnerability stats |
| GET | `/api/v1/risk/scenarios` | Risk scenarios (FAIR) |
| GET | `/api/v1/risk/summary` | Enterprise risk summary |
| POST | `/api/v1/risk/calculate` | Custom scenario calculation |
| GET | `/api/v1/controls` | Security controls catalog |
| POST | `/api/v1/optimize` | Run investment optimization |
| GET | `/api/v1/optimize/scenario-analysis` | Budget scenario analysis |
| GET | `/api/v1/dashboard/summary` | Dashboard KPIs |
| GET | `/api/v1/dashboard/data` | Full dashboard data |

**Interactive API Documentation:**
- Swagger UI: `http://localhost:8000/api/docs`
- ReDoc: `http://localhost:8000/api/redoc`

---

## 🧪 Testing

```bash
cd server
pytest -v
```

---

## ⚙️ Configuration

All configuration is managed through environment variables. Copy `.env.example` to `.env` and customize:

```bash
cp server/.env.example server/.env
```

| Variable | Default | Description |
|----------|---------|-------------|
| `DEFAULT_SIMULATIONS` | 50000 | Monte Carlo iterations |
| `DEFAULT_BUDGET` | 3000000 | Security budget ($) |
| `DEFAULT_STAFF_CAPACITY` | 50 | Available FTE |
| `DEFAULT_RISK_APPETITE` | 5000000 | Max acceptable risk ($) |
| `NUM_ASSETS` | 500 | Simulated asset count |
| `CORS_ORIGINS` | * | Allowed frontend origins |

---

## 💰 Cost Breakdown

| Component | Technology | Annual Cost |
|-----------|-----------|-------------|
| Backend Framework | FastAPI | $0 |
| Numerical Computing | NumPy | $0 |
| Data Analysis | Pandas | $0 |
| Statistics | SciPy | $0 |
| Visualization | Plotly.js | $0 |
| Containerization | Docker | $0 |
| Web Server | Nginx | $0 |
| **Total** | | **$0** |

The only costs are infrastructure (cloud VM, electricity) if you choose to deploy remotely.

---

## 🔧 Technology Stack

### Backend
- **FastAPI** — High-performance async web framework
- **Pydantic** — Data validation and settings management
- **NumPy** — Numerical computing
- **Pandas** — Data manipulation
- **SciPy** — Scientific computing and optimization

### Frontend
- **Vanilla JavaScript (ES6+)** — No build step required
- **Plotly.js** — Interactive visualizations
- **CSS Grid/Flexbox** — Modern responsive layout

### DevOps
- **Docker** — Containerization
- **Docker Compose** — Multi-service orchestration
- **Nginx** — Reverse proxy and static file serving

---

## 📖 Methodology

### FAIR Model
The platform implements the FAIR (Factor Analysis of Information Risk) methodology:

```
Threat Event Frequency (TEF)
    × Vulnerability (Vuln) = Loss Event Frequency (LEF)

LEF × Loss Magnagnitude (LM) = Annualized Loss Expectancy (ALE)
```

### Monte Carlo Simulation
- 50,000 iterations per scenario
- PERT distributions for expert estimates
- Log-normal distributions for loss magnitude
- Output: VaR 95%, VaR 99%, CVaR, confidence intervals

### Optimization Algorithm
- Greedy heuristic with efficiency sorting
- Local search refinement
- Constraints: Budget, staff capacity, risk appetite
- Objective: Maximize risk reduction or ROI

---

## 📝 License

MIT License — free for commercial and personal use.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit changes (`git commit -m 'Add amazing feature'`)
4. Push to branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🙏 Acknowledgments

- FAIR Institute for the risk quantification framework
- Open-source community for the amazing tools
- Plotly for interactive visualization library

---

**Built with ❤️ and zero licensing costs.**
