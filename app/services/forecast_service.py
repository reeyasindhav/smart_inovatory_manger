from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta

from app.models.transactions import InventoryTransaction
from app.models.inventory import InventoryItem
# from app.services.forecast_service import ema_forecast_ingredient_demand


def forecast_ingredient_demand(
    db: Session,
    inventory_item_id: int,
    window: int = 7
):
    """
    Forecast next-day demand using moving average
    """
    since_date = datetime.utcnow() - timedelta(days=window)

    daily_usage = (
        db.query(
            func.date(InventoryTransaction.created_at).label("day"),
            func.sum(
                InventoryTransaction.change_quantity * -1
            ).label("used_quantity")
        )
        .filter(
            InventoryTransaction.inventory_item_id == inventory_item_id,
            InventoryTransaction.transaction_type == "sale",
            InventoryTransaction.created_at >= since_date
        )
        .group_by("day")
        .all()
    )

    if not daily_usage:
        return {
            "inventory_item_id": inventory_item_id,
            "forecast_daily_demand": 0,
            "window_days": window,
            "data_points": 0
        }

    total_used = sum(row.used_quantity for row in daily_usage)
    avg_daily_demand = total_used / len(daily_usage)

    return {
        "inventory_item_id": inventory_item_id,
        "forecast_daily_demand": round(avg_daily_demand, 2),
        "window_days": window,
        "data_points": len(daily_usage)
    }



def ema_forecast_ingredient_demand(
    db: Session,
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3
):
    """
    Exponential Moving Average (EMA) forecast for daily ingredient demand
    """

    since_date = datetime.utcnow() - timedelta(days=window)

    # 1️⃣ Get daily usage (ordered by date)
    daily_usage = (
        db.query(
            func.date(InventoryTransaction.created_at).label("day"),
            func.sum(
                InventoryTransaction.change_quantity * -1
            ).label("used_quantity")
        )
        .filter(
            InventoryTransaction.inventory_item_id == inventory_item_id,
            InventoryTransaction.transaction_type == "sale",
            InventoryTransaction.created_at >= since_date
        )
        .group_by("day")
        .order_by("day")
        .all()
    )

    if not daily_usage:
        return {
            "inventory_item_id": inventory_item_id,
            "ema_daily_demand": 0,
            "alpha": alpha,
            "data_points": 0
        }

    # 2️⃣ Initialize EMA with first day's demand
    ema = daily_usage[0].used_quantity

    # 3️⃣ Apply EMA formula
    for row in daily_usage[1:]:
        ema = alpha * row.used_quantity + (1 - alpha) * ema

    return {
        "inventory_item_id": inventory_item_id,
        "ema_daily_demand": round(ema, 2),
        "alpha": alpha,
        "data_points": len(daily_usage)
    }




def stockout_prediction(
    db: Session,
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3
):
    item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not item:
        raise Exception("Inventory item not found")

    ema_result = ema_forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )

    daily_demand = ema_result["ema_daily_demand"]

    if daily_demand <= 0:
        return {
            "inventory_item": item.name,
            "current_stock": item.current_stock,
            "days_until_stockout": None,
            "status": "No demand"
        }

    days_left = item.current_stock / daily_demand

    return {
        "inventory_item": item.name,
        "current_stock": round(item.current_stock, 2),
        "ema_daily_demand": daily_demand,
        "days_until_stockout": round(days_left, 2),
        "status": (
            "Critical" if days_left < 2
            else "Warning" if days_left < 5
            else "Safe"
        )
    }


def dynamic_par_level(
    db: Session,
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3,
    lead_time_days: int = 3,
    safety_factor: float = 1.3
):
    item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not item:
        raise Exception("Inventory item not found")

    ema_result = ema_forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )

    daily_demand = ema_result["ema_daily_demand"]

    if daily_demand <= 0:
        return {
            "inventory_item": item.name,
            "status": "No demand"
        }

    par_level = daily_demand * lead_time_days * safety_factor
    reorder_qty = max(0, par_level - item.current_stock)

    return {
        "inventory_item": item.name,
        "current_stock": round(item.current_stock, 2),
        "ema_daily_demand": daily_demand,
        "par_level": round(par_level, 2),
        "suggested_reorder_qty": round(reorder_qty, 2),
        "lead_time_days": lead_time_days,
        "safety_factor": safety_factor,
        "status": (
            "Reorder Now" if reorder_qty > 0
            else "Stock OK"
        )
    }




def forecast_accuracy(
    db: Session,
    inventory_item_id: int,
    forecast_window: int = 14,
    evaluation_days: int = 7,
    alpha: float = 0.3
):
    """
    Compare EMA forecast vs actual usage
    """

    # 1️⃣ Get forecast
    forecast_result = ema_forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=forecast_window,
        alpha=alpha
    )

    predicted_daily = forecast_result["ema_daily_demand"]

    if predicted_daily <= 0:
        return {
            "inventory_item_id": inventory_item_id,
            "status": "No forecast available"
        }

    # 2️⃣ Get actual usage for evaluation period
    end_date = datetime.utcnow()
    start_date = end_date - timedelta(days=evaluation_days)

    actual_usage = (
        db.query(
            func.sum(
                InventoryTransaction.change_quantity * -1
            ).label("actual_total")
        )
        .filter(
            InventoryTransaction.inventory_item_id == inventory_item_id,
            InventoryTransaction.transaction_type == "sale",
            InventoryTransaction.created_at >= start_date
        )
        .scalar()
    ) or 0

    actual_daily = actual_usage / evaluation_days if evaluation_days else 0

    # 3️⃣ Errors
    mae = abs(actual_daily - predicted_daily)
    mape = (
        (mae / actual_daily) * 100
        if actual_daily > 0 else None
    )

    return {
        "inventory_item_id": inventory_item_id,
        "predicted_daily_demand": round(predicted_daily, 2),
        "actual_daily_demand": round(actual_daily, 2),
        "MAE": round(mae, 2),
        "MAPE_percent": round(mape, 2) if mape is not None else None,
        "evaluation_days": evaluation_days,
        "forecast_window": forecast_window
    }





def compare_ma_vs_ema(
    db,
    inventory_item_id: int,
    forecast_window: int = 14,
    evaluation_days: int = 7,
    alpha: float = 0.3
):
    # --- MA accuracy ---
    ma_forecast = forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=forecast_window
    )

    ma_accuracy = forecast_accuracy(
        db=db,
        inventory_item_id=inventory_item_id,
        forecast_window=forecast_window,
        evaluation_days=evaluation_days,
        alpha=alpha
    )

    # --- EMA accuracy ---
    ema_forecast = ema_forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=forecast_window,
        alpha=alpha
    )

    ema_accuracy = forecast_accuracy(
        db=db,
        inventory_item_id=inventory_item_id,
        forecast_window=forecast_window,
        evaluation_days=evaluation_days,
        alpha=alpha
    )

    # Compare by MAPE (lower is better)
    ma_mape = ma_accuracy.get("MAPE_percent")
    ema_mape = ema_accuracy.get("MAPE_percent")

    if ma_mape is None:
        winner = "EMA"
    elif ema_mape is None:
        winner = "MA"
    else:
        winner = "EMA" if ema_mape < ma_mape else "MA"

    return {
        "inventory_item_id": inventory_item_id,
        "MA": ma_accuracy,
        "EMA": ema_accuracy,
        "winner": winner
    }



def seasonal_ema_forecast(
    db: Session,
    inventory_item_id: int,
    window: int = 28,
    alpha: float = 0.3
):
    """
    Separate EMA for weekday and weekend demand
    """

    since_date = datetime.utcnow() - timedelta(days=window)

    rows = (
        db.query(
            func.date(InventoryTransaction.created_at).label("day"),
            func.extract("dow", InventoryTransaction.created_at).label("dow"),
            func.sum(
                InventoryTransaction.change_quantity * -1
            ).label("used_quantity")
        )
        .filter(
            InventoryTransaction.inventory_item_id == inventory_item_id,
            InventoryTransaction.transaction_type == "sale",
            InventoryTransaction.created_at >= since_date
        )
        .group_by("day", "dow")
        .order_by("day")
        .all()
    )

    weekday_values = []
    weekend_values = []

    for r in rows:
        # PostgreSQL: 0=Sunday, 6=Saturday
        if r.dow in (0, 6):
            weekend_values.append(r.used_quantity)
        else:
            weekday_values.append(r.used_quantity)

    def compute_ema(values, alpha):
        if not values:
            return 0
        ema = values[0]
        for v in values[1:]:
            ema = alpha * v + (1 - alpha) * ema
        return ema

    weekday_ema = compute_ema(weekday_values, alpha)
    weekend_ema = compute_ema(weekend_values, alpha)

    today_dow = datetime.utcnow().weekday()  # Python: 0=Mon, 6=Sun
    is_weekend = today_dow >= 5

    selected_ema = weekend_ema if is_weekend else weekday_ema

    return {
        "inventory_item_id": inventory_item_id,
        "weekday_ema": round(weekday_ema, 2),
        "weekend_ema": round(weekend_ema, 2),
        "selected_forecast": round(selected_ema, 2),
        "season_used": "weekend" if is_weekend else "weekday",
        "alpha": alpha,
        "window_days": window
    }




def seasonal_par_level(
    db,
    inventory_item_id: int,
    window: int = 28,
    alpha: float = 0.3,
    lead_time_days: int = 3,
    safety_factor: float = 1.3
):
    item = db.query(InventoryItem).filter(
        InventoryItem.id == inventory_item_id
    ).first()

    if not item:
        raise Exception("Inventory item not found")

    seasonal = seasonal_ema_forecast(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )

    seasonal_demand = seasonal["selected_forecast"]

    par_level = seasonal_demand * lead_time_days * safety_factor
    reorder_qty = max(0, par_level - item.current_stock)

    return {
        "inventory_item": item.name,
        "season_used": seasonal["season_used"],
        "current_stock": round(item.current_stock, 2),
        "seasonal_daily_demand": round(seasonal_demand, 2),
        "par_level": round(par_level, 2),
        "suggested_reorder_qty": round(reorder_qty, 2),
        "status": (
            "Reorder Now" if reorder_qty > 0
            else "Stock OK"
        )
    }