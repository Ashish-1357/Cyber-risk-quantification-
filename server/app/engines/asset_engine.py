"""Asset Discovery & Simulation Engine"""
import numpy as np
import pandas as pd
from datetime import datetime, timedelta
import random
from typing import List, Dict, Optional
from app.models.schemas import Asset, AssetType, CriticalityLevel


class AssetEngine:
    """Simulates enterprise asset inventory with business context"""

    ASSET_TYPES = [t.value for t in AssetType]
    CRITICALITY_LEVELS = [c.value for c in CriticalityLevel]
    BUSINESS_UNITS = ['Finance', 'HR', 'Engineering', 'Sales', 'Operations', 
                      'Legal', 'Customer Success', 'R&D']
    COMPLIANCE_OPTIONS = ['SOC2', 'ISO27001', 'GDPR+SOC2', 'PCI-DSS', 
                          'HIPAA', 'GDPR', 'NIST', 'NONE']
    LOCATIONS = ['us-east', 'us-west', 'eu-central', 'ap-south']
    CLOUD_PROVIDERS = ['aws', 'azure', 'gcp', 'on-prem']

    def __init__(self, num_assets: int = 500, seed: int = 42):
        self.num_assets = num_assets
        self.seed = seed
        np.random.seed(seed)
        random.seed(seed)
        self.assets_df = self._generate_assets()
        self.assets = [Asset(**row) for _, row in self.assets_df.iterrows()]

    def _generate_assets(self) -> pd.DataFrame:
        assets = []
        for i in range(self.num_assets):
            asset_type = np.random.choice(self.ASSET_TYPES)
            criticality = np.random.choice(self.CRITICALITY_LEVELS, p=[0.1, 0.2, 0.4, 0.3])
            impact_multipliers = {'critical': 10, 'high': 5, 'medium': 2, 'low': 0.5}
            base_revenue = np.random.lognormal(12, 1.5)
            annual_revenue_impact = base_revenue * impact_multipliers[criticality]

            compliance_str = random.choices(
                self.COMPLIANCE_OPTIONS, 
                weights=[15, 15, 20, 10, 10, 10, 10, 10]
            )[0]
            compliance_list = compliance_str.split('+') if compliance_str != 'NONE' else []

            asset = {
                'id': f'AST-{i+1:05d}',
                'name': f'{asset_type.replace("_", " ").title()}-{i+1}',
                'type': asset_type,
                'criticality': criticality,
                'business_unit': np.random.choice(self.BUSINESS_UNITS),
                'annual_revenue_impact': round(annual_revenue_impact, 2),
                'data_classification': np.random.choice(
                    ['public', 'internal', 'confidential', 'restricted'],
                    p=[0.1, 0.3, 0.4, 0.2]
                ),
                'compliance_scope': compliance_list,
                'owner': f'team-{np.random.randint(1, 20)}',
                'location': np.random.choice(self.LOCATIONS),
                'cloud_provider': np.random.choice(
                    self.CLOUD_PROVIDERS, p=[0.4, 0.3, 0.2, 0.1]
                ),
                'created_at': datetime.now() - timedelta(days=np.random.randint(30, 2000))
            }
            assets.append(asset)
        return pd.DataFrame(assets)

    def get_summary(self) -> Dict:
        return {
            'total_assets': len(self.assets_df),
            'by_type': self.assets_df['type'].value_counts().to_dict(),
            'by_criticality': self.assets_df['criticality'].value_counts().to_dict(),
            'by_business_unit': self.assets_df['business_unit'].value_counts().to_dict(),
            'total_revenue_at_risk': float(self.assets_df['annual_revenue_impact'].sum()),
            'avg_revenue_per_asset': float(self.assets_df['annual_revenue_impact'].mean()),
            'by_cloud_provider': self.assets_df['cloud_provider'].value_counts().to_dict()
        }

    def get_assets_by_criticality(self, criticality: str) -> List[Asset]:
        return [a for a in self.assets if a.criticality == criticality]

    def get_asset_by_id(self, asset_id: str) -> Optional[Asset]:
        for asset in self.assets:
            if asset.id == asset_id:
                return asset
        return None
