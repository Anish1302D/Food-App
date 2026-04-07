"""
SmartBite AI – Database Models
"""

from sqlalchemy import Column, Integer, Float, String, DateTime
from datetime import datetime
from .database import Base


class UserProfile(Base):
    __tablename__ = "user_profiles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, default="User")
    age = Column(Integer, nullable=False)
    weight = Column(Float, nullable=False)  # kg
    height = Column(Float, nullable=False)  # cm
    gender = Column(String, default="male")
    goal = Column(String, nullable=False)  # weight_loss, muscle_gain, maintenance
    dietary = Column(String, default="veg")  # veg, vegan, non-veg, keto
    activity_level = Column(String, default="moderate")
    daily_calorie_target = Column(Float, default=2000)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)


class FoodLog(Base):
    __tablename__ = "food_logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False)
    meal_name = Column(String, nullable=False)
    calories = Column(Float, nullable=False)
    protein = Column(Float, default=0)
    carbs = Column(Float, default=0)
    fats = Column(Float, default=0)
    category = Column(String, default="other")  # breakfast, lunch, dinner, snack
    logged_at = Column(DateTime, default=datetime.utcnow)
