"""
SmartBite AI – Recommendation Engine (v2)
Core logic for calculating calorie needs, macro splits, and generating
context-aware, explainable meal suggestions.

v2 additions:
  - Every recommendation includes a structured "why" explanation
  - Last-meal-timing awareness (meal gap detection)
  - Fallback logic for missing/anonymous user data
  - Deterministic scoring that changes when inputs change
"""

import hashlib
import random
from datetime import datetime
from .meals_db import get_meals_by_filters, MEALS


# ═══════════════════════════════════════════════════════════════════
# Calorie / Macro helpers (unchanged)
# ═══════════════════════════════════════════════════════════════════

def calculate_bmr(weight_kg: float, height_cm: float, age: int, gender: str = "male") -> float:
    """Calculate Basal Metabolic Rate using Mifflin-St Jeor equation."""
    if gender.lower() == "female":
        return 10 * weight_kg + 6.25 * height_cm - 5 * age - 161
    return 10 * weight_kg + 6.25 * height_cm - 5 * age + 5


def calculate_tdee(bmr: float, activity_level: str = "moderate") -> float:
    """Calculate Total Daily Energy Expenditure."""
    multipliers = {
        "sedentary": 1.2,
        "light": 1.375,
        "moderate": 1.55,
        "active": 1.725,
        "very_active": 1.9,
    }
    return bmr * multipliers.get(activity_level, 1.55)


def get_calorie_target(tdee: float, goal: str) -> float:
    """Adjust calories based on user goal."""
    adjustments = {
        "weight_loss": -500,
        "muscle_gain": 300,
        "maintenance": 0,
    }
    return tdee + adjustments.get(goal, 0)


def get_macro_split(goal: str, total_calories: float) -> dict:
    """Get macronutrient targets based on goal."""
    splits = {
        "weight_loss": {"protein": 0.40, "carbs": 0.30, "fats": 0.30},
        "muscle_gain": {"protein": 0.30, "carbs": 0.45, "fats": 0.25},
        "maintenance": {"protein": 0.30, "carbs": 0.40, "fats": 0.30},
    }
    ratios = splits.get(goal, splits["maintenance"])
    return {
        "protein_g": round((total_calories * ratios["protein"]) / 4),
        "carbs_g": round((total_calories * ratios["carbs"]) / 4),
        "fats_g": round((total_calories * ratios["fats"]) / 9),
        "protein_pct": int(ratios["protein"] * 100),
        "carbs_pct": int(ratios["carbs"] * 100),
        "fats_pct": int(ratios["fats"] * 100),
    }


def get_meal_budget(total_calories: float, meal_type: str) -> dict:
    """Get calorie budget for a specific meal type."""
    distribution = {
        "breakfast": 0.25,
        "lunch": 0.35,
        "dinner": 0.30,
        "snack": 0.10,
    }
    pct = distribution.get(meal_type, 0.25)
    budget = total_calories * pct
    return {
        "min_calories": int(budget * 0.7),
        "max_calories": int(budget * 1.3),
        "target_calories": int(budget),
    }


# ═══════════════════════════════════════════════════════════════════
# Time-of-day helpers
# ═══════════════════════════════════════════════════════════════════

def _time_to_category(time_of_day: str) -> str:
    mapping = {
        "morning": "breakfast",
        "afternoon": "lunch",
        "evening": "dinner",
        "night": "dinner",
    }
    return mapping.get(time_of_day.lower(), "lunch")


def _time_to_time_tag(time_of_day: str) -> str:
    mapping = {
        "morning": "morning",
        "afternoon": "afternoon",
        "evening": "evening",
        "night": "evening",
    }
    return mapping.get(time_of_day.lower(), "afternoon")


def _detect_time_of_day() -> str:
    hour = datetime.now().hour
    if 5 <= hour < 11:
        return "morning"
    elif 11 <= hour < 16:
        return "afternoon"
    elif 16 <= hour < 21:
        return "evening"
    else:
        return "evening"


def _friendly_time_label(time_of_day: str) -> str:
    return {
        "morning": "morning",
        "afternoon": "afternoon",
        "evening": "evening",
        "night": "night",
    }.get(time_of_day, "day")


# ═══════════════════════════════════════════════════════════════════
# NEW – Meal-gap helpers
# ═══════════════════════════════════════════════════════════════════

def _hours_since_last_meal(last_meal_time) -> float | None:
    """Return hours since last meal, or None if unknown."""
    if last_meal_time is None:
        return None
    if isinstance(last_meal_time, str):
        try:
            last_meal_time = datetime.fromisoformat(last_meal_time)
        except ValueError:
            return None
    delta = datetime.utcnow() - last_meal_time
    return delta.total_seconds() / 3600.0


def _meal_gap_label(hours: float | None) -> str | None:
    if hours is None:
        return None
    if hours >= 6:
        return "long_gap"
    if hours >= 4:
        return "moderate_gap"
    if hours >= 2:
        return "recent"
    return "very_recent"


# ═══════════════════════════════════════════════════════════════════
# NEW – Deterministic seed from context (so results change with inputs)
# ═══════════════════════════════════════════════════════════════════

def _context_seed(goal, dietary, time_of_day, mood, consumed, remaining, hour) -> int:
    """Create a seed that changes when any input changes, but is stable
    for the same set of inputs within a 30-min window."""
    blob = f"{goal}|{dietary}|{time_of_day}|{mood}|{int(consumed)}|{int(remaining)}|{hour // 1}"
    return int(hashlib.md5(blob.encode()).hexdigest(), 16) % (2**31)


# ═══════════════════════════════════════════════════════════════════
# NEW – "Why this recommendation" explanation builder
# ═══════════════════════════════════════════════════════════════════

_GOAL_LABELS = {
    "weight_loss": "weight loss",
    "muscle_gain": "muscle gain",
    "maintenance": "maintenance",
}


def _build_why(
    meal: dict,
    goal: str,
    remaining_calories: float,
    total_calories: float,
    consumed_calories: float,
    time_of_day: str,
    mood: str | None,
    meal_gap_hours: float | None,
) -> str:
    """Build a human-readable, structured explanation covering:
    1. Goal alignment
    2. Calorie balance
    3. Behavioral context (time, mood, meal gap)
    """
    reasons: list[str] = []
    goal_label = _GOAL_LABELS.get(goal, goal)

    # ── 1. Goal alignment ──────────────────────────────────────
    if goal == "weight_loss":
        if meal["calories"] <= 350:
            reasons.append(f"Low-calorie option ({meal['calories']} cal) that supports your {goal_label} goal")
        elif meal["protein"] >= 25:
            reasons.append(f"High protein ({meal['protein']}g) keeps you full longer while in a calorie deficit")
        else:
            reasons.append(f"Fits within your {goal_label} calorie budget")
    elif goal == "muscle_gain":
        if meal["protein"] >= 30:
            reasons.append(f"Packed with {meal['protein']}g protein — ideal for {goal_label}")
        elif meal["carbs"] >= 45:
            reasons.append(f"Rich in carbs ({meal['carbs']}g) to fuel workouts and recovery")
        else:
            reasons.append(f"Balanced macros to support your {goal_label} plan")
    else:
        reasons.append(f"Well-balanced meal that fits your {goal_label} plan")

    # ── 2. Calorie balance ─────────────────────────────────────
    pct_consumed = (consumed_calories / total_calories * 100) if total_calories > 0 else 0
    if remaining_calories <= 0:
        reasons.append(f"You've hit your daily limit — this is the lightest option available")
    elif remaining_calories < 400:
        if meal["calories"] <= 250:
            reasons.append(f"Only {int(remaining_calories)} cal left today — this light choice keeps you on track")
        else:
            reasons.append(f"⚠️ Only {int(remaining_calories)} cal remaining — consider a lighter option")
    elif meal["calories"] <= remaining_calories * 0.5:
        reasons.append(f"Uses {int(meal['calories'] / remaining_calories * 100)}% of your remaining {int(remaining_calories)} cal — leaves room for later meals")
    elif pct_consumed < 20:
        reasons.append(f"You've only used {int(pct_consumed)}% of your daily budget — this is a solid start")

    # ── 3. Behavioral context ──────────────────────────────────
    time_label = _friendly_time_label(time_of_day)

    # Meal gap
    if meal_gap_hours is not None:
        if meal_gap_hours >= 5:
            reasons.append(f"It's been {int(meal_gap_hours)}h since your last meal — time to refuel with something substantial")
        elif meal_gap_hours >= 3:
            reasons.append(f"About {int(meal_gap_hours)}h since your last meal — a good time for the next one")

    # Time-of-day feel
    if time_of_day == "morning" and meal["category"] == "breakfast":
        reasons.append("Great way to kickstart your morning with energy")
    elif time_of_day == "evening" and meal["category"] == "dinner":
        reasons.append("A satisfying dinner to end your day right")
    elif time_of_day == "afternoon" and meal["category"] == "snack":
        reasons.append("An afternoon snack to bridge the gap to dinner")

    # Mood
    if mood:
        mood_notes = {
            "tired": "Easy-to-digest, energy-boosting choice for when you're feeling low",
            "stressed": "Comforting option that may help ease stress",
            "energetic": "Matches your upbeat energy with a vibrant meal",
            "happy": "A feel-good pick to keep the good vibes going",
        }
        note = mood_notes.get(mood.lower())
        if note and mood.lower() in [m.lower() for m in meal.get("mood", [])]:
            reasons.append(note)

    # Condense to 2-3 most impactful reasons
    return " · ".join(reasons[:3])


# ═══════════════════════════════════════════════════════════════════
# NEW – Fallback recommendations (no user data)
# ═══════════════════════════════════════════════════════════════════

_FALLBACK_DEFAULTS = {
    "goal": "maintenance",
    "dietary": "veg",
    "total_calories": 2000,
    "consumed_calories": 0,
}


def get_fallback_recommendations(count: int = 5, time_of_day: str = None) -> list:
    """Provide meaningful suggestions even without any user data."""
    if not time_of_day:
        time_of_day = _detect_time_of_day()

    category = _time_to_category(time_of_day)
    time_tag = _time_to_time_tag(time_of_day)

    # Get a broad set of meals for this time
    meals = get_meals_by_filters(category=category, time_of_day=time_tag)
    if len(meals) < count:
        meals = get_meals_by_filters(category=category)
    if len(meals) < count:
        meals = get_meals_by_filters(time_of_day=time_tag)
    if not meals:
        meals = MEALS.copy()

    # Use time-based seed for variety across hours
    seed = _context_seed("maintenance", "veg", time_of_day, None, 0, 2000, datetime.now().hour)
    rng = random.Random(seed)
    rng.shuffle(meals)

    results = []
    for meal in meals[:count]:
        m = dict(meal)
        m["why"] = _build_fallback_why(m, time_of_day)
        m["ai_note"] = m["why"]
        results.append(m)

    return results


def _build_fallback_why(meal: dict, time_of_day: str) -> str:
    reasons = []
    time_label = _friendly_time_label(time_of_day)

    if meal["category"] == "breakfast":
        reasons.append(f"A nutritious {time_label} option to get your day started")
    elif meal["category"] == "lunch":
        reasons.append(f"Balanced {time_label} meal with {meal['protein']}g protein and {meal['carbs']}g carbs")
    elif meal["category"] == "dinner":
        reasons.append(f"Wholesome {time_label} meal to round off your day")
    else:
        reasons.append(f"A healthy snack option for the {time_label}")

    if meal["calories"] <= 350:
        reasons.append("Light and easy on calories")
    elif meal["protein"] >= 25:
        reasons.append(f"High protein ({meal['protein']}g) helps keep you full")

    reasons.append("Set up your profile for personalized recommendations tailored to your goals")
    return " · ".join(reasons[:3])


# ═══════════════════════════════════════════════════════════════════
# UPGRADED – Main recommendation engine
# ═══════════════════════════════════════════════════════════════════

def get_recommendations(
    goal: str,
    dietary: str,
    total_calories: float,
    time_of_day: str = None,
    mood: str = None,
    consumed_calories: float = 0,
    count: int = 5,
    last_meal_time=None,
) -> list:
    """
    Generate meal recommendations based on user context.

    v2 changes:
    - Each meal now includes a `why` explanation
    - last_meal_time awareness for gap-based scoring
    - Deterministic shuffling keyed to inputs (results change when context changes)
    """
    if not time_of_day:
        time_of_day = _detect_time_of_day()

    category = _time_to_category(time_of_day)
    time_tag = _time_to_time_tag(time_of_day)
    remaining_calories = total_calories - consumed_calories
    budget = get_meal_budget(remaining_calories if remaining_calories > 0 else total_calories, category)

    meal_gap = _hours_since_last_meal(last_meal_time)
    gap_label = _meal_gap_label(meal_gap)

    # ── Fetch candidate meals (progressive filter relaxation) ──
    meals = get_meals_by_filters(
        dietary=dietary,
        category=category,
        time_of_day=time_tag,
        mood=mood,
        min_calories=budget["min_calories"],
        max_calories=budget["max_calories"],
    )
    if len(meals) < count:
        meals = get_meals_by_filters(dietary=dietary, category=category, time_of_day=time_tag, mood=mood)
    if len(meals) < count:
        meals = get_meals_by_filters(dietary=dietary, category=category, time_of_day=time_tag)
    if len(meals) < count:
        meals = get_meals_by_filters(dietary=dietary, category=category)
    if len(meals) < count:
        meals = get_meals_by_filters(dietary=dietary)

    # ── Score each meal ──
    seed = _context_seed(goal, dietary, time_of_day, mood, consumed_calories, remaining_calories, datetime.now().hour)
    rng = random.Random(seed)

    scored = []
    for meal in meals:
        score = 0.0

        # Calorie proximity (closer to budget target = higher)
        cal_diff = abs(meal["calories"] - budget["target_calories"])
        score += max(0, 100 - cal_diff * 0.5)

        # Mood match
        if mood and mood.lower() in [m.lower() for m in meal["mood"]]:
            score += 30

        # Time match
        if time_tag in [t.lower() for t in meal["time"]]:
            score += 20

        # Goal-based bonuses
        if goal == "muscle_gain":
            if meal["protein"] > 30:
                score += 30
            elif meal["protein"] > 20:
                score += 15
        elif goal == "weight_loss":
            if meal["calories"] < 350:
                score += 25
            if meal["protein"] > 20:
                score += 15
            # Penalize high-cal meals when remaining is low
            if remaining_calories < 500 and meal["calories"] > 400:
                score -= 30

        # Meal gap bonuses
        if gap_label == "long_gap":
            # After a long gap, prefer more substantial meals
            if meal["calories"] >= 350:
                score += 20
            if meal["protein"] >= 20:
                score += 10
        elif gap_label == "very_recent":
            # Just ate → prefer lighter snacks
            if meal["calories"] <= 250:
                score += 15
            elif meal["calories"] >= 400:
                score -= 10

        # Remaining-calories aware
        if remaining_calories > 0 and meal["calories"] <= remaining_calories:
            score += 10  # fits within budget
        elif remaining_calories > 0 and meal["calories"] > remaining_calories:
            score -= 20  # would push over target

        # Deterministic variety factor (changes when inputs change)
        score += rng.uniform(0, 15)

        scored.append((score, meal))

    scored.sort(key=lambda x: x[0], reverse=True)
    top_meals = scored[:count]

    # ── Attach "why" explanation to each result ──
    results = []
    for _score, meal in top_meals:
        m = dict(meal)
        m["why"] = _build_why(
            meal=meal,
            goal=goal,
            remaining_calories=remaining_calories,
            total_calories=total_calories,
            consumed_calories=consumed_calories,
            time_of_day=time_of_day,
            mood=mood,
            meal_gap_hours=meal_gap,
        )
        m["ai_note"] = m["why"]
        results.append(m)

    return results


# ═══════════════════════════════════════════════════════════════════
# UPGRADED – Instant recommendation
# ═══════════════════════════════════════════════════════════════════

def get_instant_recommendation(
    goal: str,
    dietary: str,
    total_calories: float,
    consumed_calories: float = 0,
    last_meal_time=None,
) -> dict:
    """Generate a single instant recommendation ('What Should I Eat Now?')
    with full 'why' explanation."""
    time_of_day = _detect_time_of_day()

    recommendations = get_recommendations(
        goal=goal,
        dietary=dietary,
        total_calories=total_calories,
        time_of_day=time_of_day,
        consumed_calories=consumed_calories,
        count=3,
        last_meal_time=last_meal_time,
    )

    if recommendations:
        # Pick the top-scored one (already sorted)
        chosen = recommendations[0]
        return chosen

    # ── Fallback: still return a useful meal ──
    remaining = total_calories - consumed_calories
    fallback_cat = _time_to_category(time_of_day)
    return {
        "name": "Mixed Salad with Grilled Protein",
        "calories": 350,
        "protein": 28,
        "carbs": 20,
        "fats": 16,
        "category": fallback_cat,
        "description": "A balanced mixed salad with your choice of grilled protein.",
        "why": f"A safe, balanced choice for any time of day · Fits your {_GOAL_LABELS.get(goal, goal)} plan · You have {int(max(remaining, 0))} cal remaining today",
        "ai_note": f"A safe, balanced choice that keeps you on track with {int(max(remaining, 0))} cal remaining.",
    }


# ═══════════════════════════════════════════════════════════════════
# UPGRADED – Smart feedback
# ═══════════════════════════════════════════════════════════════════

def get_smart_feedback(
    total_calories: float,
    consumed_calories: float,
    meals_logged: int,
    goal: str,
    dietary: str,
    last_meal_time=None,
) -> dict:
    """Generate smart feedback based on eating patterns.
    v2: now includes last-meal-timing awareness."""
    remaining = total_calories - consumed_calories
    pct_consumed = (consumed_calories / total_calories * 100) if total_calories > 0 else 0
    meal_gap = _hours_since_last_meal(last_meal_time)

    feedback = {
        "status": "on_track",
        "message": "",
        "suggestion": None,
        "emoji": "✅",
    }

    # Overeating detection
    if consumed_calories > total_calories:
        over_by = consumed_calories - total_calories
        feedback["status"] = "over"
        feedback["emoji"] = "⚠️"
        feedback["message"] = f"You've exceeded your daily target by {int(over_by)} calories."
        light_meals = get_meals_by_filters(dietary=dietary, max_calories=200)
        if light_meals:
            suggestion = random.choice(light_meals)
            feedback["suggestion"] = {
                "text": "Consider a lighter option for your next meal:",
                "meal": suggestion,
            }
        else:
            feedback["suggestion"] = {
                "text": "Try drinking water or herbal tea to curb cravings.",
                "meal": None,
            }

    elif pct_consumed > 85:
        feedback["status"] = "warning"
        feedback["emoji"] = "🟡"
        feedback["message"] = f"You've used {int(pct_consumed)}% of your daily calories. Be mindful with remaining meals."
        light_meals = get_meals_by_filters(dietary=dietary, max_calories=250, category="snack")
        if light_meals:
            feedback["suggestion"] = {
                "text": "Keep it light with a healthy snack:",
                "meal": random.choice(light_meals),
            }

    # Long meal gap detection (NEW)
    elif meal_gap is not None and meal_gap >= 5 and meals_logged > 0:
        feedback["status"] = "skipped"
        feedback["emoji"] = "⏰"
        feedback["message"] = f"It's been {int(meal_gap)} hours since your last meal. Eating regularly helps maintain energy and metabolism!"
        time_of_day = _detect_time_of_day()
        cat = _time_to_category(time_of_day)
        next_meals = get_meals_by_filters(dietary=dietary, category=cat)
        if not next_meals:
            next_meals = get_meals_by_filters(dietary=dietary, category="snack")
        if next_meals:
            feedback["suggestion"] = {
                "text": f"Time for your next meal — here's a great {cat} option:",
                "meal": random.choice(next_meals),
            }

    # Meal skipping detection
    elif meals_logged == 0:
        hour = datetime.now().hour
        if hour > 10:
            feedback["status"] = "skipped"
            feedback["emoji"] = "🍽️"
            feedback["message"] = "Looks like you haven't eaten yet today! Don't skip meals."
            snacks = get_meals_by_filters(dietary=dietary, category="snack")
            if snacks:
                feedback["suggestion"] = {
                    "text": "Grab a quick healthy snack to get started:",
                    "meal": random.choice(snacks),
                }

    elif meals_logged == 1 and datetime.now().hour > 14:
        feedback["status"] = "skipped"
        feedback["emoji"] = "🍽️"
        feedback["message"] = "You've only had one meal today. Regular eating helps maintain energy!"
        quick_meals = get_meals_by_filters(dietary=dietary, category="snack")
        if quick_meals:
            feedback["suggestion"] = {
                "text": "Have a quick nutritious snack:",
                "meal": random.choice(quick_meals),
            }

    # On track
    elif 40 <= pct_consumed <= 70:
        feedback["status"] = "on_track"
        feedback["emoji"] = "✅"
        feedback["message"] = f"Great job! You've consumed {int(pct_consumed)}% of your daily target. Keep it up!"

    elif pct_consumed < 40 and datetime.now().hour > 16:
        feedback["status"] = "under"
        feedback["emoji"] = "📉"
        feedback["message"] = "You're under your calorie target. Make sure to eat enough to fuel your body."

    else:
        feedback["status"] = "on_track"
        feedback["emoji"] = "✅"
        feedback["message"] = f"You're on track with {int(pct_consumed)}% of daily calories consumed."

    return feedback
