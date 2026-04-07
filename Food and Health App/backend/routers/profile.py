"""
SmartBite AI – Profile Router
Handles user profile creation, retrieval, and calorie target calculation.
"""

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..database import get_db
from ..models import UserProfile
from ..schemas import ProfileCreate, ProfileResponse
from ..engine.recommendation import calculate_bmr, calculate_tdee, get_calorie_target

router = APIRouter(prefix="/api/profile", tags=["Profile"])


@router.post("/", response_model=ProfileResponse)
def create_or_update_profile(profile: ProfileCreate, db: Session = Depends(get_db)):
    """Create or update user profile and calculate daily calorie target."""
    bmr = calculate_bmr(profile.weight, profile.height, profile.age, profile.gender)
    tdee = calculate_tdee(bmr, profile.activity_level)
    calorie_target = get_calorie_target(tdee, profile.goal)

    # Check if profile exists (use id=1 for single-user app)
    existing = db.query(UserProfile).filter(UserProfile.id == 1).first()

    if existing:
        existing.name = profile.name
        existing.age = profile.age
        existing.weight = profile.weight
        existing.height = profile.height
        existing.gender = profile.gender
        existing.goal = profile.goal
        existing.dietary = profile.dietary
        existing.activity_level = profile.activity_level
        existing.daily_calorie_target = round(calorie_target)
        db.commit()
        db.refresh(existing)
        return existing
    else:
        db_profile = UserProfile(
            id=1,
            name=profile.name,
            age=profile.age,
            weight=profile.weight,
            height=profile.height,
            gender=profile.gender,
            goal=profile.goal,
            dietary=profile.dietary,
            activity_level=profile.activity_level,
            daily_calorie_target=round(calorie_target),
        )
        db.add(db_profile)
        db.commit()
        db.refresh(db_profile)
        return db_profile


@router.get("/{user_id}", response_model=ProfileResponse)
def get_profile(user_id: int, db: Session = Depends(get_db)):
    """Get user profile by ID."""
    profile = db.query(UserProfile).filter(UserProfile.id == user_id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found")
    return profile
