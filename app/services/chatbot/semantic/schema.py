from typing import Optional, Dict
from pydantic import BaseModel


class SemanticRequest(BaseModel):
    capability: str
    parameters: Optional[Dict] = {}


ALLOWED_CAPABILITIES = {
    "INVENTORY_STATUS",
    "INVENTORY_RISK",
    "SALES_OVERVIEW",
    "PROFIT_ANALYSIS",
    "PURCHASE_OVERVIEW",
    "PURCHASE_RECOMMENDATION",
    "PURCHASE_CREATE",
    "FORECAST",
    "WHAT_IF_SIMULATION",
    "EXPLANATION"
}
