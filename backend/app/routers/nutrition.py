from fastapi import APIRouter, HTTPException, Depends, Query
from typing import Optional, List
from app.models.membership import NutritionRequest, NutritionResponse
from app.models.food import Food
from app.services.auth_service import get_current_premium_member
from app.services.nutrition_service import calculate_nutrition
from app.database import get_db

router = APIRouter(prefix="/nutrition", tags=["Nutrition (Premium)"])


def serialize_food(f: dict) -> dict:
    return {
        "id": str(f["_id"]),
        "name": f["name"],
        "category": f["category"],
        "calories_per_100g": f["calories_per_100g"],
        "protein_g": f["protein_g"],
        "carbs_g": f["carbs_g"],
        "fat_g": f["fat_g"],
        "fiber_g": f["fiber_g"],
        "dietary_tags": f.get("dietary_tags", []),
        "description": f["description"],
        "serving_suggestion": f.get("serving_suggestion"),
    }


@router.post("/calculate", response_model=NutritionResponse)
async def calculate_nutrition_endpoint(
    req: NutritionRequest,
    current_user=Depends(get_current_premium_member),
):
    macros = calculate_nutrition(req)
    return NutritionResponse(macros=macros)


@router.get("/foods")
async def get_foods(
    category: Optional[str] = Query(None),
    dietary_tag: Optional[str] = Query(None),
    current_user=Depends(get_current_premium_member),
    db=Depends(get_db),
):
    query = {}
    if category:
        query["category"] = category
    if dietary_tag:
        query["dietary_tags"] = dietary_tag

    cursor = db.foods.find(query)
    foods = await cursor.to_list(length=500)
    return [serialize_food(f) for f in foods]


@router.get("/meal-suggestions")
async def get_meal_suggestions(
    dietary_preference: Optional[str] = Query(None),
    fitness_goal: Optional[str] = Query(None),
    current_user=Depends(get_current_premium_member),
    db=Depends(get_db),
):
    # Return structured meal ideas based on goal and preference
    meals = generate_meal_suggestions(
        dietary_preference or current_user.get("dietary_preference", "non_vegetarian"),
        fitness_goal or current_user.get("fitness_goal", "maintain"),
    )
    return {"meals": meals}


def generate_meal_suggestions(dietary_preference: str, fitness_goal: str) -> list:
    is_veg = dietary_preference in ("vegetarian", "vegan")

    base_meals = {
        "breakfast": [
            {
                "name": "Protein Oats Bowl",
                "description": "Oats with milk/oat milk, banana, and a scoop of protein powder",
                "macros": "~400 kcal | 30g protein | 50g carbs",
                "vegetarian": True,
            },
            {
                "name": "Eggs & Whole Wheat Toast" if not is_veg else "Tofu Scramble & Toast",
                "description": "3 scrambled eggs / tofu with 2 slices of whole wheat toast and avocado",
                "macros": "~350 kcal | 25g protein | 35g carbs",
                "vegetarian": is_veg,
            },
        ],
        "lunch": [
            {
                "name": "Grilled Chicken Rice Bowl" if not is_veg else "Dal & Brown Rice Bowl",
                "description": "Brown rice, grilled chicken / dal, and steamed vegetables",
                "macros": "~500 kcal | 40g protein | 55g carbs" if not is_veg else "~450 kcal | 20g protein | 65g carbs",
                "vegetarian": is_veg,
            },
            {
                "name": "Tuna Salad Wrap" if not is_veg else "Chickpea Salad Wrap",
                "description": "Whole wheat wrap with tuna / chickpeas, leafy greens, and Greek yogurt dressing",
                "macros": "~400 kcal | 35g protein | 40g carbs",
                "vegetarian": is_veg,
            },
        ],
        "dinner": [
            {
                "name": "Baked Salmon & Vegetables" if not is_veg else "Paneer Stir-Fry & Quinoa",
                "description": "Baked salmon / paneer with roasted broccoli, carrots, and quinoa",
                "macros": "~450 kcal | 38g protein | 30g carbs",
                "vegetarian": is_veg,
            },
            {
                "name": "Chicken & Sweet Potato" if not is_veg else "Lentil Soup & Roti",
                "description": "Grilled chicken / lentil soup with baked sweet potato",
                "macros": "~420 kcal | 35g protein | 45g carbs",
                "vegetarian": is_veg,
            },
        ],
        "snacks": [
            {"name": "Greek Yogurt + Berries", "description": "High protein snack with antioxidants", "macros": "~150 kcal | 15g protein", "vegetarian": True},
            {"name": "Handful of Mixed Nuts", "description": "Healthy fats, quick energy", "macros": "~180 kcal | 5g protein | 15g fat", "vegetarian": True},
            {"name": "Boiled Eggs x2" if not is_veg else "Hummus & Veggie Sticks", "description": "Quick protein hit / fiber-rich snack", "macros": "~140 kcal | 12g protein", "vegetarian": is_veg},
        ],
    }

    return [{"meal_time": k, "options": v} for k, v in base_meals.items()]
