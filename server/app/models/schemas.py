"""Pydantic models for API request/response validation"""
from pydantic import BaseModel, Field, field_validator
from typing import List, Dict, Optional, Tuple
from datetime import datetime
from enum import Enum


class AssetType(str, Enum):
    WEB_SERVER = "web_server"
    DATABASE = "database"
    WORKSTATION = "workstation"
    CLOUD_INSTANCE = "cloud_instance"
    CONTAINER = "container"
    NETWORK_DEVICE = "network_device"
    API_GATEWAY = "api_gateway"
    STORAGE = "storage"


class CriticalityLevel(str, Enum):
    CRITICAL = "critical"
    HIGH = "high"
    MEDIUM = "medium"
    LOW = "low"


class Asset(BaseModel):
    """Asset model"""
    id: str
    name: str
    type: AssetType
    criticality: CriticalityLevel
    business_unit: str
    annual_revenue_impact: float = Field(..., ge=0)
    data_classification: str
    compliance_scope: List[str]
    owner: str
    location: str
    cloud_provider: str
    created_at: datetime


class Vulnerability(BaseModel):
    """Vulnerability model"""
    id: str
    cve_id: str
    asset_id: str
    asset_name: str
    asset_criticality: CriticalityLevel
    cvss_score: float = Field(..., ge=0, le=10)
    epss_score: float = Field(..., ge=0, le=1)
    exploit_available: bool
    patch_available: bool
    patch_lag_days: float
    contextual_risk_score: float = Field(..., ge=0, le=10)
    discovered_date: datetime
    remediation_cost: float = Field(..., ge=0)


class RiskScenarioConfig(BaseModel):
    """FAIR scenario configuration"""
    threat_event_freq: Tuple[float, float, float] = Field(..., description="(low, most_likely, high)")
    threat_capability: Tuple[float, float, float] = Field(..., description="(low, most_likely, high)")
    control_strength: Tuple[float, float, float] = Field(..., description="(low, most_likely, high)")
    loss_magnitude: Tuple[float, float, float] = Field(..., description="(min, most_likely, max)")


class RiskScenario(BaseModel):
    """Risk scenario with calculated metrics"""
    scenario_name: str
    ale_mean: float
    ale_median: float
    ale_std: float
    ale_var_95: float
    ale_var_99: float
    ale_cvar_95: float
    prob_any_loss: float
    simulations: int


class Control(BaseModel):
    """Security control model"""
    id: str
    name: str
    category: str
    subcategory: str
    implementation_cost: float = Field(..., ge=0)
    annual_cost: float = Field(..., ge=0)
    total_5year_cost: float = Field(..., ge=0)
    effectiveness: float = Field(..., ge=0, le=1)
    coverage: List[str]
    risk_reduction: Optional[float] = None
    roi_5yr: Optional[float] = None


class OptimizationRequest(BaseModel):
    """Investment optimization request"""
    budget: float = Field(default=3000000, ge=0, description="Total security budget")
    staff_capacity: int = Field(default=50, ge=1, description="Available FTE")
    risk_appetite: float = Field(default=5000000, ge=0, description="Maximum acceptable residual risk")
    method: str = Field(default="budget_constrained", pattern="^(budget_constrained|roi_maximizing|risk_appetite)$")

    @field_validator("method")
    @classmethod
    def validate_method(cls, v):
        if v not in ["budget_constrained", "roi_maximizing", "risk_appetite"]:
            raise ValueError("Invalid optimization method")
        return v


class OptimizationResult(BaseModel):
    """Optimization result"""
    num_controls: int
    total_investment: float
    budget_remaining: float
    fte_used: float
    fte_remaining: float
    total_risk_reduction: float
    baseline_risk: float
    residual_risk: float
    risk_reduction_pct: float
    portfolio_roi: float
    payback_period_years: float
    npv: float
    selected_controls: List[Control]


class ScenarioAnalysisPoint(BaseModel):
    """Single point in scenario analysis"""
    budget: float
    risk_reduction: float
    residual_risk: float
    num_controls: int
    roi: float
    investment: float


class DashboardSummary(BaseModel):
    """Dashboard summary response"""
    total_assets: int
    total_vulnerabilities: int
    critical_vulnerabilities: int
    total_revenue_at_risk: float
    baseline_ale: float
    residual_risk: float
    risk_score: float
    total_investment: float
    portfolio_roi: float
    last_updated: datetime


class HealthCheck(BaseModel):
    """Health check response"""
    status: str
    version: str
    timestamp: datetime
    uptime_seconds: float
