"""API Tests for Cyber Risk Platform"""
import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


class TestHealth:
    def test_health_check(self):
        response = client.get("/api/v1/health")
        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "version" in data


class TestAssets:
    def test_get_assets(self):
        response = client.get("/api/v1/assets")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0

    def test_get_asset_summary(self):
        response = client.get("/api/v1/assets/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_assets" in data
        assert data["total_assets"] > 0

    def test_filter_by_criticality(self):
        response = client.get("/api/v1/assets?criticality=critical")
        assert response.status_code == 200
        data = response.json()
        for asset in data:
            assert asset["criticality"] == "critical"


class TestVulnerabilities:
    def test_get_vulnerabilities(self):
        response = client.get("/api/v1/vulnerabilities")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)

    def test_critical_only(self):
        response = client.get("/api/v1/vulnerabilities?critical_only=true")
        assert response.status_code == 200
        data = response.json()
        for vuln in data:
            assert vuln["contextual_risk_score"] >= 7.0


class TestRisk:
    def test_get_scenarios(self):
        response = client.get("/api/v1/risk/scenarios")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 6
        assert all("ale_mean" in s for s in data)

    def test_risk_summary(self):
        response = client.get("/api/v1/risk/summary")
        assert response.status_code == 200
        data = response.json()
        assert "total_ale" in data
        assert data["total_ale"] > 0


class TestControls:
    def test_get_controls(self):
        response = client.get("/api/v1/controls")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 20

    def test_get_categories(self):
        response = client.get("/api/v1/controls/categories")
        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) > 0


class TestOptimization:
    def test_optimize_default(self):
        response = client.post("/api/v1/optimize", json={})
        assert response.status_code == 200
        data = response.json()
        assert "selected_controls" in data
        assert "total_investment" in data
        assert data["total_investment"] <= 3000000

    def test_optimize_custom_budget(self):
        response = client.post("/api/v1/optimize", json={
            "budget": 1000000,
            "staff_capacity": 10,
            "method": "budget_constrained"
        })
        assert response.status_code == 200
        data = response.json()
        assert data["total_investment"] <= 1000000

    def test_scenario_analysis(self):
        response = client.get("/api/v1/optimize/scenario-analysis?min_budget=100000&max_budget=1000000&steps=5")
        assert response.status_code == 200
        data = response.json()
        assert len(data) == 5


class TestDashboard:
    def test_dashboard_summary(self):
        response = client.get("/api/v1/dashboard/summary")
        assert response.status_code == 200
        data = response.json()
        assert "risk_score" in data
        assert "baseline_ale" in data

    def test_dashboard_data(self):
        response = client.get("/api/v1/dashboard/data")
        assert response.status_code == 200
        data = response.json()
        assert "assets" in data
        assert "risk_scenarios" in data
        assert "optimization" in data
