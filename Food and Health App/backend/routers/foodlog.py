"""
SmartBite AI – Food Log Router
Handles meal logging and daily summaries.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from ..database import get_db
from ..models import FoodLog, UserProfile
from ..schemas import FoodLogCreate, FoodLogResponse, DailySummary

router = APIRouter(prefix="/api/log", tags=["Food Log"])


@router.post("/", response_model=FoodLogResponse)
def log_meal(log: FoodLogCreate, db: Session = Depends(get_db)):
    """Log a meal."""
    db_log = FoodLog(
        user_id=log.user_id,
        meal_name=log.meal_name,
        calories=log.calories,
        protein=log.protein,
        carbs=log.carbs,
        fats=log.fats,
        category=log.category,
    )
    db.add(db_log)
    db.commit()
    db.refresh(db_log)
    return db_log


@router.get("/{user_id}/today", response_model=list[FoodLogResponse])
def get_today_logs(user_id: int, db: Session = Depends(get_db)):
    """Get today's food logs for a user."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    logs = db.query(FoodLog).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= today_start,
    ).order_by(FoodLog.logged_at.desc()).all()
    return logs


@router.get("/{user_id}/summary", response_model=DailySummary)
def get_daily_summary(user_id: int, db: Session = Depends(get_db)):
    """Get daily calorie summary for a user."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    result = db.query(
        func.coalesce(func.sum(FoodLog.calories), 0),
        func.coalesce(func.sum(FoodLog.protein), 0),
        func.coalesce(func.sum(FoodLog.carbs), 0),
        func.coalesce(func.sum(FoodLog.fats), 0),
        func.count(FoodLog.id),
    ).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= today_start,
    ).first()

    total_cal = float(result[0])
    remaining = profile.daily_calorie_target - total_cal
    pct = (total_cal / profile.daily_calorie_target * 100) if profile.daily_calorie_target > 0 else 0

    return DailySummary(
        total_calories=round(total_cal),
        total_protein=round(float(result[1])),
        total_carbs=round(float(result[2])),
        total_fats=round(float(result[3])),
        meals_count=int(result[4]),
        calorie_target=profile.daily_calorie_target,
        remaining_calories=round(remaining),
        percentage_consumed=round(pct, 1),
    )


@router.delete("/{log_id}")
def delete_log(log_id: int, db: Session = Depends(get_db)):
    """Delete a food log entry."""
    log = db.query(FoodLog).filter(FoodLog.id == log_id).first()
    if not log:
        raise HTTPException(status_code=404, detail="Log entry not found")
    db.delete(log)
    db.commit()
    return {"message": "Log entry deleted"}
