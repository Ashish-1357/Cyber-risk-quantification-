"""FastAPI Routes for Cyber Risk Platform"""
from fastapi import APIRouter, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict
import numpy as np
from datetime import datetime

from app.core.config import settings
from app.core.logging import logger
from app.models.schemas import (
    Asset, Vulnerability, RiskScenario, Control, 
    OptimizationRequest, OptimizationResult, ScenarioAnalysisPoint,
    DashboardSummary, HealthCheck, RiskScenarioConfig
)
from app.engines.asset_engine import AssetEngine
from app.engines.vulnerability_engine import VulnerabilityEngine
from app.engines.fair_engine import FAIREngine
from app.engines.control_catalog import ControlCatalog
from app.engines.optimizer import InvestmentOptimizer

router = APIRouter()

# Initialize engines (singleton pattern for demo)
asset_engine = AssetEngine(num_assets=settings.num_assets)
vuln_engine = VulnerabilityEngine(asset_engine.assets_df)
fair_engine = FAIREngine(n_simulations=settings.default_simulations)
control_catalog = ControlCatalog()

# Store scenario risks for optimization
_scenario_risks = None
_optimizer = None


def _get_scenario_risks():
    """Lazy load scenario risks"""
    global _scenario_risks
    if _scenario_risks is None:
        scenarios = fair_engine.get_default_scenarios()
        _scenario_risks = fair_engine.calculate_portfolio_risk(scenarios)
    return _scenario_risks


def _get_optimizer():
    """Lazy load optimizer"""
    global _optimizer
    if _optimizer is None:
        risks = _get_scenario_risks()
        risks_dict = [r.model_dump() for r in risks]
        _optimizer = InvestmentOptimizer(
            control_catalog.controls_df,
            risks_dict,
            budget=settings.default_budget,
            staff_capacity=settings.default_staff_capacity,
            risk_appetite=settings.default_risk_appetite
        )
    return _optimizer


# =============================================================================
# HEALTH & INFO
# =============================================================================

@router.get("/health", response_model=HealthCheck)
async def health_check():
    """Health check endpoint"""
    return HealthCheck(
        status="healthy",
        version=settings.app_version,
        timestamp=datetime.now(),
        uptime_seconds=0.0  # Would track actual uptime in production
    )


@router.get("/info")
async def app_info():
    """Application information"""
    return {
        "name": settings.app_name,
        "version": settings.app_version,
        "environment": settings.environment,
        "features": [
            "FAIR Risk Quantification",
            "Monte Carlo Simulation",
            "Investment Optimization",
            "Asset Discovery",
            "Vulnerability Scoring",
            "Control Catalog"
        ]
    }


# =============================================================================
# ASSET ENDPOINTS
# =============================================================================

@router.get("/assets", response_model=List[Asset])
async def get_assets(
    criticality: Optional[str] = None,
    business_unit: Optional[str] = None,
    limit: int = Query(default=100, le=500)
):
    """Get assets with optional filtering"""
    assets = asset_engine.assets

    if criticality:
        assets = [a for a in assets if a.criticality == criticality]
    if business_unit:
        assets = [a for a in assets if a.business_unit == business_unit]

    return assets[:limit]


@router.get("/assets/summary")
async def get_asset_summary():
    """Get asset inventory summary"""
    return asset_engine.get_summary()


@router.get("/assets/{asset_id}")
async def get_asset(asset_id: str):
    """Get specific asset by ID"""
    asset = asset_engine.get_asset_by_id(asset_id)
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


# =============================================================================
# VULNERABILITY ENDPOINTS
# =============================================================================

@router.get("/vulnerabilities", response_model=List[Vulnerability])
async def get_vulnerabilities(
    critical_only: bool = False,
    exploit_available: Optional[bool] = None,
    limit: int = Query(default=100, le=500)
):
    """Get vulnerabilities with optional filtering"""
    vulns = vuln_engine.vulnerabilities

    if critical_only:
        vulns = [v for v in vulns if v.contextual_risk_score >= 7.0]
    if exploit_available is not None:
        vulns = [v for v in vulns if v.exploit_available == exploit_available]

    return vulns[:limit]


@router.get("/vulnerabilities/summary")
async def get_vulnerability_summary():
    """Get vulnerability summary statistics"""
    return vuln_engine.get_summary()


@router.get("/vulnerabilities/by-asset/{asset_id}")
async def get_vulnerabilities_by_asset(asset_id: str):
    """Get vulnerabilities for a specific asset"""
    return vuln_engine.get_vulnerabilities_by_asset(asset_id)


# =============================================================================
# RISK QUANTIFICATION ENDPOINTS
# =============================================================================

@router.get("/risk/scenarios", response_model=List[RiskScenario])
async def get_risk_scenarios():
    """Get all risk scenarios with FAIR calculations"""
    return _get_scenario_risks()


@router.post("/risk/calculate")
async def calculate_risk(scenario_config: RiskScenarioConfig, name: str = "Custom Scenario"):
    """Calculate risk for a custom scenario"""
    result = fair_engine.calculate_risk(scenario_config)
    return RiskScenario(
        scenario_name=name,
        ale_mean=result['ale_mean'],
        ale_median=result['ale_median'],
        ale_std=result['ale_std'],
        ale_var_95=result['ale_var_95'],
        ale_var_99=result['ale_var_99'],
        ale_cvar_95=result['ale_cvar_95'],
        prob_any_loss=result['prob_any_loss'],
        simulations=result['simulations']
    )


@router.get("/risk/summary")
async def get_risk_summary():
    """Get enterprise risk summary"""
    risks = _get_scenario_risks()
    total_ale = sum(r.ale_mean for r in risks)
    total_var95 = sum(r.ale_var_95 for r in risks)

    return {
        "total_scenarios": len(risks),
        "total_ale": round(total_ale, 2),
        "total_var_95": round(total_var95, 2),
        "highest_risk_scenario": max(risks, key=lambda x: x.ale_mean).scenario_name,
        "lowest_risk_scenario": min(risks, key=lambda x: x.ale_mean).scenario_name,
        "scenarios": [r.model_dump() for r in risks]
    }


# =============================================================================
# CONTROL CATALOG ENDPOINTS
# =============================================================================

@router.get("/controls", response_model=List[Control])
async def get_controls(category: Optional[str] = None):
    """Get security controls"""
    if category:
        return control_catalog.get_by_category(category)
    return control_catalog.get_controls()


@router.get("/controls/categories")
async def get_control_categories():
    """Get control categories"""
    return control_catalog.get_categories()


@router.get("/controls/{control_id}")
async def get_control(control_id: str):
    """Get specific control"""
    control = control_catalog.get_control_by_id(control_id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control


# =============================================================================
# OPTIMIZATION ENDPOINTS
# =============================================================================

@router.post("/optimize", response_model=OptimizationResult)
async def optimize_portfolio(request: OptimizationRequest):
    """Run investment optimization"""
    risks = _get_scenario_risks()
    risks_dict = [r.model_dump() for r in risks]

    optimizer = InvestmentOptimizer(
        control_catalog.controls_df,
        risks_dict,
        budget=request.budget,
        staff_capacity=request.staff_capacity,
        risk_appetite=request.risk_appetite
    )

    result = optimizer.optimize(request.method)
    logger.info(f"Optimization completed: {result.num_controls} controls selected")
    return result


@router.get("/optimize/scenario-analysis")
async def scenario_analysis(
    min_budget: float = Query(default=500000, ge=0),
    max_budget: float = Query(default=5000000, ge=0),
    steps: int = Query(default=20, ge=5, le=50)
):
    """Run scenario analysis across budget range"""
    risks = _get_scenario_risks()
    risks_dict = [r.model_dump() for r in risks]

    optimizer = InvestmentOptimizer(
        control_catalog.controls_df,
        risks_dict,
        budget=max_budget,
        staff_capacity=settings.default_staff_capacity,
        risk_appetite=settings.default_risk_appetite
    )

    budget_range = np.linspace(min_budget, max_budget, steps)
    results = optimizer.run_scenario_analysis(budget_range)
    return results


# =============================================================================
# DASHBOARD ENDPOINTS
# =============================================================================

@router.get("/dashboard/summary", response_model=DashboardSummary)
async def get_dashboard_summary():
    """Get consolidated dashboard summary"""
    asset_summary = asset_engine.get_summary()
    vuln_summary = vuln_engine.get_summary()
    risks = _get_scenario_risks()
    baseline_ale = sum(r.ale_mean for r in risks)

    # Get optimized result
    optimizer = _get_optimizer()
    opt_result = optimizer.optimize('budget_constrained')

    risk_score = min(100, (opt_result.residual_risk / baseline_ale) * 100) if baseline_ale > 0 else 0

    return DashboardSummary(
        total_assets=asset_summary['total_assets'],
        total_vulnerabilities=vuln_summary['total_vulnerabilities'],
        critical_vulnerabilities=vuln_summary['critical_vulnerabilities'],
        total_revenue_at_risk=asset_summary['total_revenue_at_risk'],
        baseline_ale=round(baseline_ale, 2),
        residual_risk=round(opt_result.residual_risk, 2),
        risk_score=round(risk_score, 2),
        total_investment=round(opt_result.total_investment, 2),
        portfolio_roi=round(opt_result.portfolio_roi, 2),
        last_updated=datetime.now()
    )


@router.get("/dashboard/data")
async def get_dashboard_data():
    """Get all data needed for dashboard rendering"""
    risks = _get_scenario_risks()
    optimizer = _get_optimizer()
    opt_result = optimizer.optimize('budget_constrained')

    return {
        "assets": asset_engine.get_summary(),
        "vulnerabilities": vuln_engine.get_summary(),
        "risk_scenarios": [r.model_dump() for r in risks],
        "optimization": opt_result.model_dump(),
        "controls": [c.model_dump() for c in control_catalog.get_controls()]
    }
