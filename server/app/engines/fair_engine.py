"""FAIR (Factor Analysis of Information Risk) Monte Carlo Engine"""
import numpy as np
from typing import Dict, List, Tuple
from app.models.schemas import RiskScenario, RiskScenarioConfig
from app.core.logging import logger


class FAIREngine:
    """
    FAIR Risk Quantification Engine
    Uses Monte Carlo simulation for probabilistic risk analysis
    """

    def __init__(self, n_simulations: int = 50000):
        self.n_simulations = n_simulations
        logger.info(f"FAIR Engine initialized with {n_simulations:,} simulations")

    def _calibrate_distribution(self, low: float, most_likely: float, high: float) -> np.ndarray:
        """Create PERT distribution from expert estimates"""
        mean = (low + 4 * most_likely + high) / 6
        alpha = 1 + 4 * (most_likely - low) / (high - low)
        beta = 1 + 4 * (high - most_likely) / (high - low)
        return np.random.beta(alpha, beta, self.n_simulations) * (high - low) + low

    def _lognormal_loss(self, min_loss: float, most_likely: float, max_loss: float) -> np.ndarray:
        """Generate loss magnitude using log-normal distribution"""
        mu = np.log(most_likely)
        sigma = (np.log(max_loss) - np.log(min_loss)) / 4
        return np.random.lognormal(mu, sigma, self.n_simulations)

    def calculate_risk(self, scenario_config: RiskScenarioConfig) -> Dict:
        """Run FAIR Monte Carlo simulation for a single scenario"""
        # Threat Event Frequency (TEF)
        tef = self._calibrate_distribution(*scenario_config.threat_event_freq)

        # Threat Capability (TC) vs Control Strength (CS)
        tc = self._calibrate_distribution(*scenario_config.threat_capability)
        cs = self._calibrate_distribution(*scenario_config.control_strength)

        # Vulnerability
        vulnerability = np.clip((tc - cs + 1) / 2, 0, 1)

        # Loss Event Frequency (LEF)
        lef = tef * vulnerability

        # Loss Magnitude (LM)
        lm = self._lognormal_loss(*scenario_config.loss_magnitude)

        # Annualized Loss Expectancy (ALE)
        ale = lef * lm

        return {
            'tef': tef,
            'vulnerability': vulnerability,
            'lef': lef,
            'lm': lm,
            'ale': ale,
            'ale_mean': float(np.mean(ale)),
            'ale_median': float(np.median(ale)),
            'ale_std': float(np.std(ale)),
            'ale_var_95': float(np.percentile(ale, 95)),
            'ale_var_99': float(np.percentile(ale, 99)),
            'ale_cvar_95': float(np.mean(ale[ale >= np.percentile(ale, 95)])),
            'prob_any_loss': float(np.mean(lef > 0)),
            'simulations': self.n_simulations
        }

    def calculate_portfolio_risk(self, scenarios: Dict[str, RiskScenarioConfig]) -> List[RiskScenario]:
        """Calculate risk across multiple scenarios"""
        results = []
        for name, config in scenarios.items():
            result = self.calculate_risk(config)
            results.append(RiskScenario(
                scenario_name=name,
                ale_mean=result['ale_mean'],
                ale_median=result['ale_median'],
                ale_std=result['ale_std'],
                ale_var_95=result['ale_var_95'],
                ale_var_99=result['ale_var_99'],
                ale_cvar_95=result['ale_cvar_95'],
                prob_any_loss=result['prob_any_loss'],
                simulations=result['simulations']
            ))
        logger.info(f"Portfolio risk calculated for {len(results)} scenarios")
        return results

    def get_default_scenarios(self) -> Dict[str, RiskScenarioConfig]:
        """Return default enterprise risk scenarios"""
        return {
            'Ransomware Attack': RiskScenarioConfig(
                threat_event_freq=(0.5, 2.0, 5.0),
                threat_capability=(0.6, 0.8, 0.95),
                control_strength=(0.4, 0.6, 0.8),
                loss_magnitude=(500000, 2000000, 15000000)
            ),
            'Data Breach (Customer PII)': RiskScenarioConfig(
                threat_event_freq=(0.2, 1.0, 3.0),
                threat_capability=(0.5, 0.7, 0.9),
                control_strength=(0.5, 0.65, 0.85),
                loss_magnitude=(1000000, 5000000, 50000000)
            ),
            'Insider Threat': RiskScenarioConfig(
                threat_event_freq=(0.1, 0.5, 2.0),
                threat_capability=(0.7, 0.9, 1.0),
                control_strength=(0.3, 0.5, 0.7),
                loss_magnitude=(200000, 1000000, 10000000)
            ),
            'Supply Chain Attack': RiskScenarioConfig(
                threat_event_freq=(0.1, 0.3, 1.0),
                threat_capability=(0.6, 0.85, 0.98),
                control_strength=(0.2, 0.4, 0.6),
                loss_magnitude=(1000000, 8000000, 100000000)
            ),
            'Cloud Misconfiguration': RiskScenarioConfig(
                threat_event_freq=(1.0, 3.0, 8.0),
                threat_capability=(0.3, 0.5, 0.8),
                control_strength=(0.4, 0.55, 0.75),
                loss_magnitude=(50000, 500000, 5000000)
            ),
            'DDoS Attack': RiskScenarioConfig(
                threat_event_freq=(2.0, 5.0, 15.0),
                threat_capability=(0.4, 0.6, 0.85),
                control_strength=(0.5, 0.7, 0.9),
                loss_magnitude=(10000, 100000, 1000000)
            )
        }
