from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import SessionLocal
from app.services.report_service import ingredient_usage_report,get_inventory_valuation ,get_dish_costs_and_profit,sales_summary_report, purchase_summary_report
from app.services.forecast_service import compare_ma_vs_ema, dynamic_par_level, ema_forecast_ingredient_demand, forecast_accuracy, forecast_ingredient_demand, seasonal_ema_forecast, seasonal_par_level, stockout_prediction
from app.services.what_if_scene import simulate_what_if

router = APIRouter(prefix="/reports", tags=["Reports"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get("/ingredient-usage")
def ingredient_usage(days: int = 7, db: Session = Depends(get_db)):
    return ingredient_usage_report(db, days)

@router.get("/dish-profit")
def dish_profit_report(db: Session = Depends(get_db)):
    return get_dish_costs_and_profit(db)

@router.get("/inventory-valuation")
def inventory_valuation(db: Session = Depends(get_db)):
    return get_inventory_valuation(db)

@router.get("/sales-summary")
def sales_summary(days: int = 7, db: Session = Depends(get_db)):
    data = sales_summary_report(db, days)
    return [
        {
            "menu_item": row.name,
            "quantity_sold": row.total_quantity,
            "revenue": row.total_revenue
        }
        for row in data
    ]

@router.get("/purchase-summary")
def purchase_summary(days: int = 7, db: Session = Depends(get_db)):
    data = purchase_summary_report(db, days)
    return [
        {
            "ingredient": row.name,
            "purchased_quantity": row.purchased_quantity
        }
        for row in data
    ]

@router.get("/forecast/ingredient/{inventory_item_id}")
def ingredient_forecast(
    inventory_item_id: int,
    window: int = 7,
    db: Session = Depends(get_db)
):
    return forecast_ingredient_demand(db, inventory_item_id, window)

@router.get("/forecast/ingredient/{inventory_item_id}/ema")
def ingredient_ema_forecast(
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3,
    db: Session = Depends(get_db)
):
    return ema_forecast_ingredient_demand(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )


@router.get("/forecast/ingredient/{inventory_item_id}/stockout")
def ingredient_stockout_forecast(
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3,
    db: Session = Depends(get_db)
):
    return stockout_prediction(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )




@router.get("/forecast/ingredient/{inventory_item_id}/par-level")
def ingredient_par_level(
    inventory_item_id: int,
    window: int = 14,
    alpha: float = 0.3,
    lead_time_days: int = 3,
    safety_factor: float = 1.3,
    db: Session = Depends(get_db)
):
    return dynamic_par_level(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha,
        lead_time_days=lead_time_days,
        safety_factor=safety_factor
    )



@router.get("/forecast/ingredient/{inventory_item_id}/accuracy")
def ingredient_forecast_accuracy(
    inventory_item_id: int,
    forecast_window: int = 14,
    evaluation_days: int = 7,
    alpha: float = 0.3,
    db: Session = Depends(get_db)
):
    return forecast_accuracy(
        db=db,
        inventory_item_id=inventory_item_id,
        forecast_window=forecast_window,
        evaluation_days=evaluation_days,
        alpha=alpha
    )




    
@router.get("/forecast/ingredient/{inventory_item_id}/compare")
def compare_forecast_models(
    inventory_item_id: int,
    forecast_window: int = 14,
    evaluation_days: int = 7,
    alpha: float = 0.3,
    db: Session = Depends(get_db)
):
    return compare_ma_vs_ema(
        db=db,
        inventory_item_id=inventory_item_id,
        forecast_window=forecast_window,
        evaluation_days=evaluation_days,
        alpha=alpha
    )



@router.get("/forecast/ingredient/{inventory_item_id}/seasonal")
def seasonal_forecast(
    inventory_item_id: int,
    window: int = 28,
    alpha: float = 0.3,
    db: Session = Depends(get_db)
):
    return seasonal_ema_forecast(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha
    )


@router.get("/forecast/ingredient/{inventory_item_id}/seasonal-par")
def seasonal_par(
    inventory_item_id: int,
    window: int = 28,
    alpha: float = 0.3,
    lead_time_days: int = 3,
    safety_factor: float = 1.3,
    db: Session = Depends(get_db)
):
    return seasonal_par_level(
        db=db,
        inventory_item_id=inventory_item_id,
        window=window,
        alpha=alpha,
        lead_time_days=lead_time_days,
        safety_factor=safety_factor
    )


    
@router.get("/what-if/ingredient/{inventory_item_id}")
def what_if_simulation(
    inventory_item_id: int,
    horizon_days: int = 7,
    event_multiplier: float = 1.0,
    extra_lead_time_days: int = 0,
    alpha: float = 0.3,
    window: int = 28,
    safety_factor: float = 1.3,
    db: Session = Depends(get_db)
):
    return simulate_what_if(
        db=db,
        inventory_item_id=inventory_item_id,
        horizon_days=horizon_days,
        event_multiplier=event_multiplier,
        extra_lead_time_days=extra_lead_time_days,
        alpha=alpha,
        window=window,
        safety_factor=safety_factor
    )

