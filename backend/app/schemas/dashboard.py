from pydantic import BaseModel
from typing import Dict

class DashboardSummaryResponse(BaseModel):
    total_predictions: int
    high_risk_locations: int
    active_alerts: int
    acknowledged_alerts: int
    risk_level_breakdown: Dict[str, int]