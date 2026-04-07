"""
SmartBite AI – Recommendation Router (v2)
Generates context-aware meal recommendations with:
  - last_meal_time awareness
  - "why this recommendation" explanations
  - fallback logic for missing user profiles
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from datetime import datetime, timedelta
from ..database import get_db
from ..models import UserProfile, FoodLog
from ..schemas import RecommendRequest, InstantRecommendRequest, MealResponse
from ..engine.recommendation import (
    get_recommendations,
    get_instant_recommendation,
    get_fallback_recommendations,
)

router = APIRouter(prefix="/api/recommend", tags=["Recommendations"])


# ── Helpers ──────────────────────────────────────────────────────

def _get_today_consumed(user_id: int, db: Session) -> tuple:
    """Get today's consumed calories and meal count."""
    today_start = datetime.utcnow().replace(hour=0, minute=0, second=0, microsecond=0)
    result = db.query(
        func.coalesce(func.sum(FoodLog.calories), 0),
        func.count(FoodLog.id)
    ).filter(
        FoodLog.user_id == user_id,
        FoodLog.logged_at >= today_start
    ).first()
    return float(result[0]), int(result[1])


def _get_last_meal_time(user_id: int, db: Session):
    """Get the timestamp of the user's most recent food log entry."""
    last_log = db.query(FoodLog.logged_at).filter(
        FoodLog.user_id == user_id,
    ).order_by(desc(FoodLog.logged_at)).first()
    return last_log[0] if last_log else None


def _meal_to_response(m: dict) -> MealResponse:
    """Convert an engine meal dict to a MealResponse, including 'why'."""
    return MealResponse(
        name=m["name"],
        calories=m["calories"],
        protein=m["protein"],
        carbs=m["carbs"],
        fats=m["fats"],
        category=m.get("category", "lunch"),
        description=m.get("description", ""),
        ai_note=m.get("ai_note"),
        why=m.get("why"),
    )


# ── Endpoints ────────────────────────────────────────────────────

@router.post("/", response_model=list[MealResponse])
def recommend_meals(req: RecommendRequest, db: Session = Depends(get_db)):
    """Get meal recommendations based on user context.
    Falls back to generic suggestions if no profile exists."""
    profile = db.query(UserProfile).filter(UserProfile.id == req.user_id).first()

    # ── Fallback: no profile → still give meaningful suggestions ──
    if not profile:
        fallback = get_fallback_recommendations(
            count=req.count,
            time_of_day=req.time_of_day,
        )
        return [_meal_to_response(m) for m in fallback]

    consumed, _ = _get_today_consumed(req.user_id, db)
    last_meal_time = _get_last_meal_time(req.user_id, db)

    meals = get_recommendations(
        goal=profile.goal,
        dietary=profile.dietary,
        total_calories=profile.daily_calorie_target,
        time_of_day=req.time_of_day,
        mood=req.mood,
        consumed_calories=consumed,
        count=req.count,
        last_meal_time=last_meal_time,
    )

    return [_meal_to_response(m) for m in meals]


@router.post("/instant", response_model=MealResponse)
def instant_recommendation(req: InstantRecommendRequest, db: Session = Depends(get_db)):
    """Generate instant 'What Should I Eat Now?' recommendation.
    Falls back to generic suggestion if no profile exists."""
    profile = db.query(UserProfile).filter(UserProfile.id == req.user_id).first()

    # ── Fallback: no profile → still pick a meal ──
    if not profile:
        fallback = get_fallback_recommendations(count=1)
        if fallback:
            return _meal_to_response(fallback[0])
        # Ultimate fallback (should never happen)
        return MealResponse(
            name="Mixed Salad with Grilled Protein",
            calories=350,
            protein=28,
            carbs=20,
            fats=16,
            category="lunch",
            description="A balanced mixed salad with your choice of grilled protein.",
            ai_note="A healthy, balanced choice for any time of day. Set up your profile for personalized recommendations!",
            why="A safe balanced option · No profile set up yet — create one for personalized meals · Good nutrition at any time of day",
        )

    consumed, _ = _get_today_consumed(req.user_id, db)
    last_meal_time = _get_last_meal_time(req.user_id, db)

    meal = get_instant_recommendation(
        goal=profile.goal,
        dietary=profile.dietary,
        total_calories=profile.daily_calorie_target,
        consumed_calories=consumed,
        last_meal_time=last_meal_time,
    )

    return _meal_to_response(meal)


@router.get("/fallback", response_model=list[MealResponse])
def fallback_recommendations(count: int = 5, time_of_day: str = None):
    """Get generic recommendations without any user context.
    Useful for anonymous/first-time visitors."""
    meals = get_fallback_recommendations(count=count, time_of_day=time_of_day)
    return [_meal_to_response(m) for m in meals]
