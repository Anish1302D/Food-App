"""
SmartBite AI – Smart Feedback Router
Provides intelligent feedback based on user eating patterns.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime
from ..database import get_db
from ..models import FoodLog, UserProfile
from ..schemas import FeedbackResponse
from sqlalchemy import desc
from ..engine.recommendation import get_smart_feedback

router = APIRouter(prefix="/api/feedback", tags=["Smart Feedback"])


@router.get("/{user_id}", response_model=FeedbackResponse)
def get_feedback(user_id: int, db: Session = Depends(get_db)):
    """Get smart feedback based on today's eating patterns."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")

    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)

    result = db.query(
        func.coalesce(func.sum(FoodLog.calories), 0),
        func.count(FoodLog.id),
    ).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= today_start,
    ).first()

    consumed = float(result[0])
    meals_count = int(result[1])

    last_log = db.query(FoodLog.logged_at).filter(
        FoodLog.user_id == user_id,
    ).order_by(desc(FoodLog.logged_at)).first()
    last_meal_time = last_log[0] if last_log else None

    feedback = get_smart_feedback(
        total_calories=profile.daily_calorie_target,
        consumed_calories=consumed,
        meals_logged=meals_count,
        goal=profile.goal,
        dietary=profile.dietary,
        last_meal_time=last_meal_time,
    )

    return FeedbackResponse(**feedback)
