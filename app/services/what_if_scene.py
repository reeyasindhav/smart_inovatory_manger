from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from app.models.inventory import InventoryItem
from app.services.forecast_service import seasonal_ema_forecast

def simulate_what_if(
    db: Session,
    inventory_item_id: int,
    horizon_days: int = 7,
    event_multiplier: float = 1.0,
    extra_lead_time_days: int = 0,
    alpha: float = 0.3,
    window: int = 28,
    safety_factor: float = 1.3
):
    item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not item:
        raise Exception("Inventory item not found")

    # 1️⃣ Base seasonal forecast
    seasonal = seasonal_ema_forecast(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )

    base_daily_demand = seasonal["selected_forecast"]
    simulated_daily_demand = base_daily_demand * event_multiplier

    # 2️⃣ Simulate stock consumption
    remaining_stock = item.current_stock
    stockout_day = None

    for day in range(1, horizon_days + 1):
        remaining_stock -= simulated_daily_demand
        if remaining_stock <= 0 and stockout_day is None:
            stockout_day = day

    # 3️⃣ Adjust par level with supplier delay
    lead_time_days = 3 + extra_lead_time_days
    par_level = simulated_daily_demand * lead_time_days * safety_factor
    suggested_reorder_qty = max(0, par_level - item.current_stock)

    return {
        "inventory_item": item.name,
        "current_stock": round(item.current_stock, 2),

        "base_daily_demand": round(base_daily_demand, 2),
        "event_multiplier": event_multiplier,
        "simulated_daily_demand": round(simulated_daily_demand, 2),

        "horizon_days": horizon_days,
        "projected_stock_after_horizon": round(remaining_stock, 2),
        "stockout_in_days": stockout_day,

        "lead_time_days": lead_time_days,
        "simulated_par_level": round(par_level, 2),
        "suggested_reorder_qty": round(suggested_reorder_qty, 2),

        "risk_level": (
            "High" if stockout_day and stockout_day <= lead_time_days
            else "Medium" if stockout_day
            else "Low"
        )
    }
