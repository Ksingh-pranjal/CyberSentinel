from pydantic import BaseModel, ConfigDict
from typing import Optional, Dict

class DashboardSummaryResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    totalComplaints: int
    highRiskZones: int
    activeAlerts: int
    atRiskAtms: int
    risk_level_breakdown: Optional[Dict[str, int]] = None