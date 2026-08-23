"""Security Control Catalog with Cost Models"""
import pandas as pd
from typing import List, Dict, Optional
from app.models.schemas import Control


class ControlCatalog:
    """Security control catalog with TCO models and effectiveness scores"""

    CONTROLS_DATA = [
        {'id': 'CTRL-001', 'name': 'Multi-Factor Authentication (MFA)', 
         'category': 'IAM', 'subcategory': 'Authentication',
         'implementation_cost': 150000, 'annual_cost': 50000,
         'effectiveness': 0.85, 'coverage': ['Ransomware Attack', 'Insider Threat', 'Data Breach (Customer PII)']},
        {'id': 'CTRL-002', 'name': 'Privileged Access Management (PAM)',
         'category': 'IAM', 'subcategory': 'Authorization',
         'implementation_cost': 300000, 'annual_cost': 100000,
         'effectiveness': 0.80, 'coverage': ['Insider Threat', 'Ransomware Attack', 'Supply Chain Attack']},
        {'id': 'CTRL-003', 'name': 'Zero Trust Network Architecture',
         'category': 'Network', 'subcategory': 'Segmentation',
         'implementation_cost': 800000, 'annual_cost': 200000,
         'effectiveness': 0.75, 'coverage': ['Ransomware Attack', 'Insider Threat', 'Data Breach (Customer PII)', 'Supply Chain Attack']},
        {'id': 'CTRL-004', 'name': 'Endpoint Detection & Response (EDR)',
         'category': 'Endpoint', 'subcategory': 'Detection',
         'implementation_cost': 400000, 'annual_cost': 150000,
         'effectiveness': 0.70, 'coverage': ['Ransomware Attack', 'Insider Threat', 'Supply Chain Attack']},
        {'id': 'CTRL-005', 'name': 'Extended Detection & Response (XDR)',
         'category': 'Endpoint', 'subcategory': 'Detection',
         'implementation_cost': 600000, 'annual_cost': 250000,
         'effectiveness': 0.78, 'coverage': ['Ransomware Attack', 'Insider Threat', 'Data Breach (Customer PII)', 'Supply Chain Attack']},
        {'id': 'CTRL-006', 'name': 'Data Loss Prevention (DLP)',
         'category': 'Data', 'subcategory': 'Protection',
         'implementation_cost': 350000, 'annual_cost': 120000,
         'effectiveness': 0.65, 'coverage': ['Data Breach (Customer PII)', 'Insider Threat']},
        {'id': 'CTRL-007', 'name': 'Encryption at Rest & Transit',
         'category': 'Data', 'subcategory': 'Encryption',
         'implementation_cost': 200000, 'annual_cost': 40000,
         'effectiveness': 0.60, 'coverage': ['Data Breach (Customer PII)', 'Ransomware Attack', 'Insider Threat']},
        {'id': 'CTRL-008', 'name': 'Cloud Security Posture Management (CSPM)',
         'category': 'Cloud', 'subcategory': 'Configuration',
         'implementation_cost': 180000, 'annual_cost': 80000,
         'effectiveness': 0.72, 'coverage': ['Cloud Misconfiguration', 'Data Breach (Customer PII)']},
        {'id': 'CTRL-009', 'name': 'Cloud Workload Protection Platform (CWPP)',
         'category': 'Cloud', 'subcategory': 'Runtime Protection',
         'implementation_cost': 250000, 'annual_cost': 100000,
         'effectiveness': 0.68, 'coverage': ['Cloud Misconfiguration', 'Supply Chain Attack', 'Ransomware Attack']},
        {'id': 'CTRL-010', 'name': 'Immutable Backup & Recovery',
         'category': 'Resilience', 'subcategory': 'Backup',
         'implementation_cost': 300000, 'annual_cost': 120000,
         'effectiveness': 0.90, 'coverage': ['Ransomware Attack']},
        {'id': 'CTRL-011', 'name': 'Disaster Recovery as a Service (DRaaS)',
         'category': 'Resilience', 'subcategory': 'Recovery',
         'implementation_cost': 400000, 'annual_cost': 150000,
         'effectiveness': 0.75, 'coverage': ['Ransomware Attack', 'DDoS Attack', 'Cloud Misconfiguration']},
        {'id': 'CTRL-012', 'name': 'Next-Gen Firewall (NGFW)',
         'category': 'Network', 'subcategory': 'Perimeter',
         'implementation_cost': 250000, 'annual_cost': 80000,
         'effectiveness': 0.55, 'coverage': ['Ransomware Attack', 'DDoS Attack', 'Data Breach (Customer PII)']},
        {'id': 'CTRL-013', 'name': 'DDoS Protection Service',
         'category': 'Network', 'subcategory': 'Availability',
         'implementation_cost': 100000, 'annual_cost': 60000,
         'effectiveness': 0.88, 'coverage': ['DDoS Attack']},
        {'id': 'CTRL-014', 'name': 'Vulnerability Management Program',
         'category': 'Vulnerability', 'subcategory': 'Assessment',
         'implementation_cost': 150000, 'annual_cost': 100000,
         'effectiveness': 0.50, 'coverage': ['Ransomware Attack', 'Data Breach (Customer PII)', 'Cloud Misconfiguration', 'Supply Chain Attack']},
        {'id': 'CTRL-015', 'name': 'Penetration Testing (Continuous)',
         'category': 'Vulnerability', 'subcategory': 'Testing',
         'implementation_cost': 200000, 'annual_cost': 150000,
         'effectiveness': 0.45, 'coverage': ['Ransomware Attack', 'Data Breach (Customer PII)', 'Cloud Misconfiguration']},
        {'id': 'CTRL-016', 'name': 'Software Supply Chain Security',
         'category': 'Supply Chain', 'subcategory': 'Integrity',
         'implementation_cost': 350000, 'annual_cost': 120000,
         'effectiveness': 0.70, 'coverage': ['Supply Chain Attack', 'Ransomware Attack']},
        {'id': 'CTRL-017', 'name': 'Third-Party Risk Management',
         'category': 'Supply Chain', 'subcategory': 'Governance',
         'implementation_cost': 180000, 'annual_cost': 90000,
         'effectiveness': 0.55, 'coverage': ['Supply Chain Attack', 'Data Breach (Customer PII)']},
        {'id': 'CTRL-018', 'name': 'Security Operations Center (SOC)',
         'category': 'Monitoring', 'subcategory': 'Detection',
         'implementation_cost': 800000, 'annual_cost': 1200000,
         'effectiveness': 0.65, 'coverage': ['Ransomware Attack', 'Insider Threat', 'Data Breach (Customer PII)', 'Supply Chain Attack', 'DDoS Attack']},
        {'id': 'CTRL-019', 'name': 'Threat Intelligence Platform',
         'category': 'Monitoring', 'subcategory': 'Intelligence',
         'implementation_cost': 200000, 'annual_cost': 150000,
         'effectiveness': 0.40, 'coverage': ['Ransomware Attack', 'Supply Chain Attack', 'DDoS Attack']},
        {'id': 'CTRL-020', 'name': 'User & Entity Behavior Analytics (UEBA)',
         'category': 'Monitoring', 'subcategory': 'Analytics',
         'implementation_cost': 300000, 'annual_cost': 120000,
         'effectiveness': 0.60, 'coverage': ['Insider Threat', 'Ransomware Attack', 'Data Breach (Customer PII)']},
    ]

    def __init__(self):
        self.controls_df = pd.DataFrame(self.CONTROLS_DATA)
        self.controls_df['total_5year_cost'] = (
            self.controls_df['implementation_cost'] + self.controls_df['annual_cost'] * 5
        )
        self.controls = [
            Control(**row) for _, row in self.controls_df.iterrows()
        ]

    def get_controls(self) -> List[Control]:
        return self.controls

    def get_control_by_id(self, control_id: str) -> Optional[Control]:
        for control in self.controls:
            if control.id == control_id:
                return control
        return None

    def get_by_category(self, category: str) -> List[Control]:
        return [c for c in self.controls if c.category == category]

    def calculate_control_impact(self, control_id: str, scenario_risks: List[Dict]) -> float:
        """Calculate risk reduction for a specific control"""
        control = self.get_control_by_id(control_id)
        if not control:
            return 0.0

        total_reduction = 0
        for scenario_name in control.coverage:
            scenario_risk = next(
                (r for r in scenario_risks if r.get('scenario_name') == scenario_name), 
                None
            )
            if scenario_risk:
                reduction = scenario_risk.get('ale_mean', 0) * control.effectiveness * 0.5
                total_reduction += reduction
        return total_reduction

    def get_categories(self) -> List[str]:
        return list(self.controls_df['category'].unique())
