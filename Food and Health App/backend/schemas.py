"""
SmartBite AI – Pydantic Schemas for request/response validation
"""

from pydantic import BaseModel
from typing import Optional
from datetime import datetime


# ======================== Profile Schemas ========================

class ProfileCreate(BaseModel):
    name: str = "User"
    age: int
    weight: float  # kg
    height: float  # cm
    gender: str = "male"
    goal: str  # weight_loss, muscle_gain, maintenance
    dietary: str = "veg"  # veg, vegan, non-veg, keto
    activity_level: str = "moderate"


class ProfileResponse(BaseModel):
    id: int
    name: str
    age: int
    weight: float
    height: float
    gender: str
    goal: str
    dietary: str
    activity_level: str
    daily_calorie_target: float

    class Config:
        from_attributes = True


# ======================== Recommendation Schemas ========================

class RecommendRequest(BaseModel):
    user_id: int
    time_of_day: Optional[str] = None  # morning, afternoon, evening
    mood: Optional[str] = None  # tired, stressed, energetic, happy
    count: int = 5


class InstantRecommendRequest(BaseModel):
    user_id: int


class MealResponse(BaseModel):
    name: str
    calories: int
    protein: int
    carbs: int
    fats: int
    category: str
    description: str
    ai_note: Optional[str] = None
    why: Optional[str] = None


# ======================== Food Log Schemas ========================

class FoodLogCreate(BaseModel):
    user_id: int
    meal_name: str
    calories: float
    protein: float = 0
    carbs: float = 0
    fats: float = 0
    category: str = "other"


class FoodLogResponse(BaseModel):
    id: int
    user_id: int
    meal_name: str
    calories: float
    protein: float
    carbs: float
    fats: float
    category: str
    logged_at: datetime

    class Config:
        from_attributes = True


class DailySummary(BaseModel):
    total_calories: float
    total_protein: float
    total_carbs: float
    total_fats: float
    meals_count: int
    calorie_target: float
    remaining_calories: float
    percentage_consumed: float


# ======================== Feedback Schemas ========================

class FeedbackResponse(BaseModel):
    status: str
    message: str
    emoji: str
    suggestion: Optional[dict] = None


# ======================== Health Score Schemas ========================

class ScoreBreakdownItem(BaseModel):
    score: float
    max: int
    note: str


class ScoreBreakdown(BaseModel):
    calorie_balance: ScoreBreakdownItem
    meal_timing: ScoreBreakdownItem
    food_quality: ScoreBreakdownItem


class HealthScoreResponse(BaseModel):
    score: int
    label: str
    emoji: str
    explanation: str
    display: str
    breakdown: ScoreBreakdown
