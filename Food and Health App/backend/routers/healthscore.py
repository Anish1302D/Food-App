"""
SmartBite AI – Health Score Router
Provides the daily health score endpoint.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime
from ..database import get_db
from ..models import FoodLog, UserProfile
from ..schemas import HealthScoreResponse
from ..engine.health_score import calculate_health_score

router = APIRouter(prefix="/api/health-score", tags=["Health Score"])


@router.get("/{user_id}", response_model=HealthScoreResponse)
def get_health_score(user_id: int, db: Session = Depends(get_db)):
    """Get the daily health score for a user."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    # Fetch today's logs
    db_logs = db.query(FoodLog).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= today_start,
    ).order_by(FoodLog.logged_at.asc()).all()

    # Convert to dicts for the engine
    logs = [
        {
            "calories": log.calories,
            "protein": log.protein,
            "carbs": log.carbs,
            "fats": log.fats,
            "category": log.category,
            "logged_at": log.logged_at,
        }
        for log in db_logs
    ]

    consumed = sum(log["calories"] for log in logs)

    result = calculate_health_score(
        consumed_calories=consumed,
        calorie_target=profile.daily_calorie_target,
        logs=logs,
        goal=profile.goal,
    )

    return HealthScoreResponse(**result)
