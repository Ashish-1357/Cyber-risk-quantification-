#!/usr/bin/env python3
"""
Cyber Risk Quantification Platform - FastAPI Server
Open Source Edition | Zero Licensing Costs

Usage:
    uvicorn main:app --reload --host 0.0.0.0 --port 8000

    Or:
    python main.py
"""
import time
from datetime import datetime
from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

from app.core.config import settings
from app.core.logging import logger
from app.api.routes import router


# Track startup time
_start_time = time.time()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Application lifespan events"""
    logger.info(f"🚀 Starting {settings.app_name} v{settings.app_version}")
    logger.info(f"📊 FAIR Simulations: {settings.default_simulations:,}")
    logger.info(f"💰 Default Budget: ${settings.default_budget:,.0f}")
    yield
    logger.info("👋 Shutting down server")


# Create FastAPI app
app = FastAPI(
    title=settings.app_name,
    version=settings.app_version,
    description="""
    AI-Powered Continuous Cyber Risk Quantification & Investment Optimization Platform.

    ## Features

    * **FAIR Risk Quantification** - Monte Carlo simulation for probabilistic risk analysis
    * **Asset Discovery** - Enterprise asset inventory with business context
    * **Vulnerability Scoring** - Contextual risk scoring with CVSS + EPSS
    * **Control Catalog** - 20 security controls with TCO models
    * **Investment Optimization** - Constrained portfolio optimization

    ## Zero Cost

    All technologies used are open-source and free:
    - FastAPI (MIT)
    - NumPy (BSD)
    - Pandas (BSD)
    - SciPy (BSD)
    - Plotly (MIT)
    """,
    docs_url="/api/docs",
    redoc_url="/api/redoc",
    openapi_url="/api/openapi.json",
    lifespan=lifespan
)

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(router, prefix="/api/v1", tags=["cyber-risk"])

# Serve static files (client)
try:
    app.mount("/static", StaticFiles(directory="../client"), name="static")
except RuntimeError:
    logger.warning("Client directory not found, static files not served")


@app.get("/", response_class=HTMLResponse)
async def root():
    """Root endpoint - serves dashboard or API info"""
    return """
    <!DOCTYPE html>
    <html>
    <head>
        <title>Cyber Risk Platform</title>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <style>
            body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif; 
                   max-width: 800px; margin: 50px auto; padding: 20px; line-height: 1.6; }
            h1 { color: #2c3e50; }
            .card { background: #f8f9fa; border-radius: 8px; padding: 20px; margin: 15px 0; }
            .endpoint { background: #e9ecef; padding: 8px 12px; border-radius: 4px; 
                       font-family: monospace; margin: 5px 0; display: inline-block; }
            a { color: #3498db; text-decoration: none; }
            a:hover { text-decoration: underline; }
            .badge { background: #28a745; color: white; padding: 4px 8px; border-radius: 4px; 
                    font-size: 12px; }
        </style>
    </head>
    <body>
        <h1>🔒 Cyber Risk Quantification Platform</h1>
        <p><span class="badge">Open Source</span> <span class="badge">Zero Cost</span></p>

        <div class="card">
            <h2>📊 Dashboard</h2>
            <p><a href="/static/index.html">Open Interactive Dashboard</a></p>
        </div>

        <div class="card">
            <h2>📚 API Documentation</h2>
            <p><a href="/api/docs">Swagger UI</a> | <a href="/api/redoc">ReDoc</a></p>
        </div>

        <div class="card">
            <h2>🔌 Key Endpoints</h2>
            <div><span class="endpoint">GET /api/v1/health</span> - Health check</div>
            <div><span class="endpoint">GET /api/v1/dashboard/summary</span> - Dashboard summary</div>
            <div><span class="endpoint">GET /api/v1/risk/scenarios</span> - Risk scenarios</div>
            <div><span class="endpoint">POST /api/v1/optimize</span> - Run optimization</div>
            <div><span class="endpoint">GET /api/v1/assets</span> - Asset inventory</div>
            <div><span class="endpoint">GET /api/v1/vulnerabilities</span> - Vulnerabilities</div>
        </div>

        <div class="card">
            <h2>⚙️ Configuration</h2>
            <p>Environment: <strong>""" + settings.environment + """</strong></p>
            <p>Version: <strong>""" + settings.app_version + """</strong></p>
            <p>Simulations: <strong>""" + f"{settings.default_simulations:,}" + """</strong></p>
        </div>
    </body>
    </html>
    """


@app.get("/api")
async def api_root():
    """API root"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "documentation": "/api/docs",
        "endpoints": {
            "health": "/api/v1/health",
            "assets": "/api/v1/assets",
            "vulnerabilities": "/api/v1/vulnerabilities",
            "risk": "/api/v1/risk/scenarios",
            "optimize": "/api/v1/optimize",
            "dashboard": "/api/v1/dashboard/summary"
        }
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main:app",
        host=settings.host,
        port=settings.port,
        workers=1 if settings.debug else settings.workers,
        reload=settings.debug
    )
