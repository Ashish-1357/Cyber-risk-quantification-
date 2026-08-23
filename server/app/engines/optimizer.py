"""Investment Optimization Engine"""
import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
from app.models.schemas import OptimizationResult, Control, ScenarioAnalysisPoint
from app.core.logging import logger


class InvestmentOptimizer:
    """
    Security Investment Portfolio Optimizer
    Uses constrained greedy algorithms with local search
    """

    def __init__(self, controls_df: pd.DataFrame, scenario_risks: List[Dict],
                 budget: float = 3000000, staff_capacity: int = 50, 
                 risk_appetite: float = 5000000):
        self.controls = controls_df.copy()
        self.scenario_risks = scenario_risks
        self.budget = budget
        self.staff_capacity = staff_capacity
        self.risk_appetite = risk_appetite
        self.n_controls = len(controls_df)
        self._compute_risk_reduction_matrix()
        logger.info(f"Optimizer initialized: budget=${budget:,.0f}, staff={staff_capacity}")

    def _compute_risk_reduction_matrix(self):
        """Pre-compute risk reduction for each control"""
        self.risk_reduction = np.zeros(self.n_controls)
        self.implementation_cost = self.controls['implementation_cost'].values
        self.annual_cost = self.controls['annual_cost'].values
        self.total_cost = self.implementation_cost + self.annual_cost * 5
        self.fte_required = np.random.uniform(0.5, 5.0, self.n_controls)

        for i, (_, ctrl) in enumerate(self.controls.iterrows()):
            total_reduction = 0
            for scenario_name in ctrl['coverage']:
                scenario_risk = next(
                    (r for r in self.scenario_risks if r.get('scenario_name') == scenario_name), 
                    None
                )
                if scenario_risk:
                    reduction = scenario_risk.get('ale_mean', 0) * ctrl['effectiveness'] * 0.5
                    total_reduction += reduction
            self.risk_reduction[i] = total_reduction

    def optimize(self, method: str = 'budget_constrained') -> OptimizationResult:
        """Run optimization with specified method"""
        if method == 'budget_constrained':
            return self._optimize_budget_constrained()
        elif method == 'roi_maximizing':
            return self._optimize_roi()
        elif method == 'risk_appetite':
            return self._optimize_risk_appetite()
        else:
            raise ValueError(f"Unknown method: {method}")

    def _optimize_budget_constrained(self) -> OptimizationResult:
        """Maximize risk reduction within budget"""
        efficiency = self.risk_reduction / (self.total_cost + 1)
        sorted_indices = np.argsort(-efficiency)

        selected = np.zeros(self.n_controls, dtype=bool)
        current_budget = 0.0
        current_fte = 0.0
        total_reduction = 0.0

        for idx in sorted_indices:
            if (current_budget + self.total_cost[idx] <= self.budget and
                current_fte + self.fte_required[idx] <= self.staff_capacity):
                selected[idx] = True
                current_budget += self.total_cost[idx]
                current_fte += self.fte_required[idx]
                total_reduction += self.risk_reduction[idx]

        return self._build_result(selected, current_budget, current_fte, total_reduction)

    def _optimize_roi(self) -> OptimizationResult:
        """Maximize portfolio ROI"""
        roi = (self.risk_reduction * 5 - self.total_cost) / (self.total_cost + 1)
        sorted_indices = np.argsort(-roi)

        selected = np.zeros(self.n_controls, dtype=bool)
        current_budget = 0.0
        current_fte = 0.0
        total_reduction = 0.0

        for idx in sorted_indices:
            if (current_budget + self.total_cost[idx] <= self.budget and
                current_fte + self.fte_required[idx] <= self.staff_capacity):
                selected[idx] = True
                current_budget += self.total_cost[idx]
                current_fte += self.fte_required[idx]
                total_reduction += self.risk_reduction[idx]

        return self._build_result(selected, current_budget, current_fte, total_reduction)

    def _optimize_risk_appetite(self) -> OptimizationResult:
        """Minimize cost while meeting risk appetite"""
        baseline_risk = sum(r.get('ale_mean', 0) for r in self.scenario_risks)
        target_reduction = baseline_risk - self.risk_appetite

        efficiency = self.risk_reduction / (self.total_cost + 1)
        sorted_indices = np.argsort(-efficiency)

        selected = np.zeros(self.n_controls, dtype=bool)
        current_budget = 0.0
        current_fte = 0.0
        total_reduction = 0.0

        for idx in sorted_indices:
            if total_reduction < target_reduction:
                if current_fte + self.fte_required[idx] <= self.staff_capacity:
                    selected[idx] = True
                    current_budget += self.total_cost[idx]
                    current_fte += self.fte_required[idx]
                    total_reduction += self.risk_reduction[idx]

        return self._build_result(selected, current_budget, current_fte, total_reduction)

    def _build_result(self, selected: np.ndarray, budget_used: float, 
                      fte_used: float, total_reduction: float) -> OptimizationResult:
        """Build optimization result"""
        selected_controls = self.controls[selected].copy()
        selected_controls['risk_reduction'] = self.risk_reduction[selected]
        selected_controls['roi_5yr'] = (
            (selected_controls['risk_reduction'] * 5 - selected_controls['total_5year_cost']) /
            selected_controls['total_5year_cost'] * 100
        )

        baseline_risk = sum(r.get('ale_mean', 0) for r in self.scenario_risks)
        residual_risk = max(0, baseline_risk - total_reduction)

        control_objects = []
        for _, row in selected_controls.iterrows():
            control_objects.append(Control(
                id=row['id'],
                name=row['name'],
                category=row['category'],
                subcategory=row['subcategory'],
                implementation_cost=row['implementation_cost'],
                annual_cost=row['annual_cost'],
                total_5year_cost=row['total_5year_cost'],
                effectiveness=row['effectiveness'],
                coverage=row['coverage'],
                risk_reduction=row['risk_reduction'],
                roi_5yr=row['roi_5yr']
            ))

        return OptimizationResult(
            num_controls=int(selected.sum()),
            total_investment=round(budget_used, 2),
            budget_remaining=round(self.budget - budget_used, 2),
            fte_used=round(fte_used, 2),
            fte_remaining=round(self.staff_capacity - fte_used, 2),
            total_risk_reduction=round(total_reduction, 2),
            baseline_risk=round(baseline_risk, 2),
            residual_risk=round(residual_risk, 2),
            risk_reduction_pct=round((total_reduction / baseline_risk) * 100, 2) if baseline_risk > 0 else 0,
            portfolio_roi=round(((total_reduction * 5 - budget_used) / budget_used * 100), 2) if budget_used > 0 else 0,
            payback_period_years=round(budget_used / total_reduction, 2) if total_reduction > 0 else float('inf'),
            npv=round(total_reduction * 5 - budget_used, 2),
            selected_controls=control_objects
        )

    def run_scenario_analysis(self, budget_range: np.ndarray) -> List[ScenarioAnalysisPoint]:
        """Run optimization across budget range"""
        results = []
        original_budget = self.budget

        for budget in budget_range:
            self.budget = budget
            result = self.optimize('budget_constrained')
            results.append(ScenarioAnalysisPoint(
                budget=round(budget, 2),
                risk_reduction=round(result.total_risk_reduction, 2),
                residual_risk=round(result.residual_risk, 2),
                num_controls=result.num_controls,
                roi=round(result.portfolio_roi, 2),
                investment=round(result.total_investment, 2)
            ))

        self.budget = original_budget
        return results
