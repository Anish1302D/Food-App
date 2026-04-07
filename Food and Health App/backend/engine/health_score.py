"""
SmartBite AI – Daily Health Score Engine
Calculates a 0-100 health score based on:
  - Calorie balance (40 pts)
  - Meal timing consistency (30 pts)
  - Food quality (30 pts)
"""

from datetime import datetime


# ═══════════════════════════════════════════════════════════════════
# Score labels & thresholds
# ═══════════════════════════════════════════════════════════════════

def _score_label(score: int) -> tuple[str, str]:
    """Return (label, emoji) for a given score."""
    if score >= 85:
        return "Excellent", "🌟"
    elif score >= 70:
        return "Good", "👍"
    elif score >= 50:
        return "Fair", "⚡"
    elif score >= 30:
        return "Needs Work", "📉"
    else:
        return "Poor", "⚠️"


# ═══════════════════════════════════════════════════════════════════
# Factor 1: Calorie Balance (0-40 pts)
# ═══════════════════════════════════════════════════════════════════

def _calorie_balance_score(
    consumed: float,
    target: float,
    hour: int,
) -> tuple[float, str]:
    """
    Score how well calorie intake aligns with the daily target.
    Adjusts expectations based on time of day (eating 30% by noon is fine).
    """
    if target <= 0:
        return 0.0, "No calorie target set"

    # Expected consumption fraction based on time of day
    if hour < 8:
        expected_fraction = 0.0
    elif hour < 12:
        expected_fraction = 0.25
    elif hour < 15:
        expected_fraction = 0.50
    elif hour < 18:
        expected_fraction = 0.70
    elif hour < 21:
        expected_fraction = 0.90
    else:
        expected_fraction = 1.0

    ratio = consumed / target

    if expected_fraction < 0.1:
        # Too early to judge, give full marks if not overeating
        if ratio <= 0.15:
            return 40.0, "Good start to the day"
        else:
            return max(0, 40 - (ratio - 0.15) * 200), "Eating a lot early"

    # How close is actual ratio to the expected fraction?
    # Perfect: ratio == expected_fraction (within ±10%)
    deviation = abs(ratio - expected_fraction) / max(expected_fraction, 0.1)

    if deviation <= 0.10:
        score = 40.0
        note = "Calorie intake perfectly on track"
    elif deviation <= 0.25:
        score = 35.0
        note = "Calorie intake mostly on track"
    elif deviation <= 0.50:
        score = 25.0
        if ratio > expected_fraction:
            note = "Slightly high calorie intake"
        else:
            note = "Slightly low calorie intake"
    elif deviation <= 0.75:
        score = 15.0
        if ratio > expected_fraction:
            note = "High calorie intake for this time of day"
        else:
            note = "Low calorie intake – eat more to stay fueled"
    else:
        score = 5.0
        if ratio > 1.0:
            note = "Exceeded daily calorie target"
        elif ratio > expected_fraction:
            note = "Significantly over expected intake"
        else:
            note = "Very low calorie intake – don't skip meals"

    # Hard penalty for exceeding daily target entirely
    if ratio > 1.15:
        score = max(0, score - 15)
        note = "Exceeded daily calorie target"
    elif ratio > 1.05:
        score = max(0, score - 8)
        note = "Slightly exceeded daily calorie target"

    return round(score, 1), note


# ═══════════════════════════════════════════════════════════════════
# Factor 2: Meal Timing Consistency (0-30 pts)
# ═══════════════════════════════════════════════════════════════════

def _meal_timing_score(
    logs: list,
    hour: int,
) -> tuple[float, str]:
    """
    Score meal timing regularity:
    - Having 3+ meals: up to 10 pts
    - Covering breakfast/lunch/dinner categories: up to 10 pts
    - No large gaps (>5h between meals): up to 10 pts
    """
    if not logs:
        if hour < 9:
            return 20.0, "Day just started – log your first meal!"
        elif hour < 12:
            return 10.0, "No meals logged yet – time for breakfast"
        else:
            return 0.0, "No meals logged – meal timing needs attention"

    meals_count = len(logs)
    score = 0.0
    notes = []

    # Sub-score 1: Meal count (0-10)
    if meals_count >= 4:
        score += 10.0
    elif meals_count >= 3:
        score += 8.0
    elif meals_count >= 2:
        score += 5.0
    else:
        score += 2.0

    # Sub-score 2: Category coverage (0-10)
    categories = set()
    for log in logs:
        cat = log.get("category", "other")
        if cat in ("breakfast", "lunch", "dinner"):
            categories.add(cat)

    expected_cats = set()
    if hour >= 9:
        expected_cats.add("breakfast")
    if hour >= 14:
        expected_cats.add("lunch")
    if hour >= 20:
        expected_cats.add("dinner")

    if expected_cats:
        coverage = len(categories & expected_cats) / len(expected_cats)
        score += round(coverage * 10, 1)
        missing = expected_cats - categories
        if missing:
            notes.append(f"Missing {', '.join(sorted(missing))}")
    else:
        score += 10.0  # Too early to judge

    # Sub-score 3: Meal gaps (0-10)
    times = sorted([log["logged_at"] for log in logs if log.get("logged_at")])
    if len(times) >= 2:
        max_gap_hours = 0
        for i in range(1, len(times)):
            t1 = times[i - 1]
            t2 = times[i]
            if isinstance(t1, str):
                t1 = datetime.fromisoformat(t1)
            if isinstance(t2, str):
                t2 = datetime.fromisoformat(t2)
            gap = (t2 - t1).total_seconds() / 3600
            max_gap_hours = max(max_gap_hours, gap)

        if max_gap_hours <= 3:
            score += 10.0
        elif max_gap_hours <= 4:
            score += 7.0
        elif max_gap_hours <= 5:
            score += 4.0
            notes.append("Long gap between meals")
        else:
            score += 1.0
            notes.append(f"Very long gap ({int(max_gap_hours)}h) between meals")
    elif len(times) == 1:
        score += 5.0  # Only 1 meal, can't measure gaps

    note = " · ".join(notes) if notes else "Good meal timing"
    if meals_count >= 3 and not notes:
        note = "Consistent meal schedule"

    return round(min(score, 30.0), 1), note


# ═══════════════════════════════════════════════════════════════════
# Factor 3: Food Quality (0-30 pts)
# ═══════════════════════════════════════════════════════════════════

def _food_quality_score(
    logs: list,
    calorie_target: float,
) -> tuple[float, str]:
    """
    Score food quality based on:
    - Protein adequacy (0-10): higher protein ratio = better
    - Calorie density per meal (0-10): moderate = better than extreme
    - Macro balance (0-10): balanced P/C/F is best
    """
    if not logs:
        return 0.0, "No food data to evaluate"

    total_cal = sum(log.get("calories", 0) for log in logs)
    total_protein = sum(log.get("protein", 0) for log in logs)
    total_carbs = sum(log.get("carbs", 0) for log in logs)
    total_fats = sum(log.get("fats", 0) for log in logs)
    n = len(logs)

    score = 0.0
    notes = []

    # Sub-score 1: Protein adequacy (0-10)
    # Good: protein provides 20-35% of total calories
    if total_cal > 0:
        protein_cal_pct = (total_protein * 4) / total_cal * 100
        if 25 <= protein_cal_pct <= 35:
            score += 10.0
        elif 20 <= protein_cal_pct <= 40:
            score += 7.0
        elif 15 <= protein_cal_pct <= 45:
            score += 4.0
        else:
            score += 1.0
            if protein_cal_pct < 15:
                notes.append("Low protein intake")
            else:
                notes.append("Very high protein ratio")
    else:
        score += 5.0

    # Sub-score 2: Calorie density per meal (0-10)
    # Healthy meals are usually 250-600 cal range
    avg_cal = total_cal / n if n > 0 else 0
    if 250 <= avg_cal <= 550:
        score += 10.0
    elif 200 <= avg_cal <= 650:
        score += 7.0
    elif 150 <= avg_cal <= 750:
        score += 4.0
    else:
        score += 1.0
        if avg_cal > 750:
            notes.append("Meals are very calorie-dense")
        elif avg_cal < 150:
            notes.append("Meals are very low calorie")

    # Sub-score 3: Macro balance (0-10)
    # Ideal: ~30% protein, ~40% carbs, ~30% fats (by calories)
    if total_cal > 0:
        p_pct = (total_protein * 4) / total_cal
        c_pct = (total_carbs * 4) / total_cal
        f_pct = (total_fats * 9) / total_cal

        # Deviation from ideal
        p_dev = abs(p_pct - 0.30)
        c_dev = abs(c_pct - 0.40)
        f_dev = abs(f_pct - 0.30)
        total_dev = p_dev + c_dev + f_dev

        if total_dev <= 0.15:
            score += 10.0
        elif total_dev <= 0.30:
            score += 7.0
        elif total_dev <= 0.50:
            score += 4.0
            notes.append("Macros slightly imbalanced")
        else:
            score += 1.0
            notes.append("Macros significantly imbalanced")
    else:
        score += 5.0

    if not notes:
        note = "Great food quality choices"
    else:
        note = " · ".join(notes)

    return round(min(score, 30.0), 1), note


# ═══════════════════════════════════════════════════════════════════
# Main: Calculate Health Score
# ═══════════════════════════════════════════════════════════════════

def calculate_health_score(
    consumed_calories: float,
    calorie_target: float,
    logs: list,
    goal: str = "maintenance",
) -> dict:
    """
    Calculate the Daily Health Score (0-100).

    Args:
        consumed_calories: Total calories consumed today
        calorie_target: User's daily calorie target
        logs: List of today's food log dicts (with calories, protein, carbs, fats, category, logged_at)
        goal: User's fitness goal

    Returns:
        dict with score, label, emoji, explanation, breakdown
    """
    hour = datetime.now().hour

    # Calculate each factor
    cal_score, cal_note = _calorie_balance_score(consumed_calories, calorie_target, hour)
    timing_score, timing_note = _meal_timing_score(logs, hour)
    quality_score, quality_note = _food_quality_score(logs, calorie_target)

    # Total score
    total = round(cal_score + timing_score + quality_score)
    total = max(0, min(100, total))

    label, emoji = _score_label(total)

    # Build explanation
    explanation_parts = []
    if cal_note:
        explanation_parts.append(cal_note)
    if timing_note and timing_note not in ("Good meal timing", "Consistent meal schedule"):
        explanation_parts.append(timing_note)
    if quality_note and quality_note != "Great food quality choices":
        explanation_parts.append(quality_note)

    if not explanation_parts:
        if total >= 85:
            explanation = "Outstanding! You're nailing your nutrition today"
        elif total >= 70:
            explanation = "Good balance across all factors"
        else:
            explanation = "Keep logging meals to improve your score"
    else:
        explanation = " · ".join(explanation_parts[:2])

    # Short display text like: "Score: 78 – Good balance but slightly high calorie intake"
    display = f"Score: {total} – {explanation}"

    return {
        "score": total,
        "label": label,
        "emoji": emoji,
        "explanation": explanation,
        "display": display,
        "breakdown": {
            "calorie_balance": {
                "score": cal_score,
                "max": 40,
                "note": cal_note,
            },
            "meal_timing": {
                "score": timing_score,
                "max": 30,
                "note": timing_note,
            },
            "food_quality": {
                "score": quality_score,
                "max": 30,
                "note": quality_note,
            },
        },
    }
