from app.models.membership import NutritionRequest, MacroResult


ACTIVITY_MULTIPLIERS = {
    "sedentary": 1.2,
    "light": 1.375,
    "moderate": 1.55,
    "active": 1.725,
    "very_active": 1.9,
}

GOAL_ADJUSTMENTS = {
    "weight_loss": -400,
    "muscle_gain": 350,
    "maintain": 0,
    "endurance": 200,
}


def calculate_nutrition(req: NutritionRequest) -> MacroResult:
    # Harris-Benedict BMR
    if req.gender.lower() == "male":
        bmr = 88.362 + (13.397 * req.weight) + (4.799 * req.height) - (5.677 * req.age)
    else:
        bmr = 447.593 + (9.247 * req.weight) + (3.098 * req.height) - (4.330 * req.age)

    activity_mult = ACTIVITY_MULTIPLIERS.get(req.activity_level, 1.55)
    tdee = bmr * activity_mult

    goal_adj = GOAL_ADJUSTMENTS.get(req.fitness_goal, 0)
    target_calories = max(1200, tdee + goal_adj)

    # Macronutrient split
    protein_g = req.weight * 2.0  # 2g per kg body weight
    fat_g = (target_calories * 0.25) / 9  # 25% of calories from fat
    protein_calories = protein_g * 4
    fat_calories = fat_g * 9
    carb_calories = target_calories - protein_calories - fat_calories
    carbs_g = max(50, carb_calories / 4)

    # Fiber (daily recommendation)
    fiber_g = 14.0 * (target_calories / 1000)  # 14g per 1000 kcal

    # Water (ml → liters)
    water_liters = round((req.weight * 35) / 1000, 1)  # 35ml per kg

    return MacroResult(
        calories=round(target_calories, 1),
        protein_g=round(protein_g, 1),
        carbs_g=round(carbs_g, 1),
        fat_g=round(fat_g, 1),
        fiber_g=round(fiber_g, 1),
        water_liters=water_liters,
        bmr=round(bmr, 1),
        tdee=round(tdee, 1),
    )
