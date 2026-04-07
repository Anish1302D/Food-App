"""
SmartBite AI – Comprehensive Meal Database
~80+ meals with full nutritional info, tags for dietary preference, time of day, and mood.
"""

MEALS = [
    # ======================== BREAKFAST ========================
    {
        "name": "Greek Yogurt Parfait with Berries & Granola",
        "calories": 320,
        "protein": 18,
        "carbs": 42,
        "fats": 10,
        "category": "breakfast",
        "dietary": ["veg"],
        "mood": ["energetic", "happy"],
        "time": ["morning"],
        "description": "Creamy Greek yogurt layered with mixed berries, honey, and crunchy granola."
    },
    {
        "name": "Avocado Toast with Poached Eggs",
        "calories": 380,
        "protein": 16,
        "carbs": 30,
        "fats": 22,
        "category": "breakfast",
        "dietary": ["veg"],
        "mood": ["energetic", "happy"],
        "time": ["morning"],
        "description": "Whole grain toast topped with smashed avocado and perfectly poached eggs."
    },
    {
        "name": "Oatmeal with Banana & Almond Butter",
        "calories": 350,
        "protein": 12,
        "carbs": 52,
        "fats": 14,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "stressed"],
        "time": ["morning"],
        "description": "Warm oatmeal topped with sliced banana and a drizzle of almond butter."
    },
    {
        "name": "Veggie Scramble with Whole Wheat Toast",
        "calories": 290,
        "protein": 15,
        "carbs": 28,
        "fats": 14,
        "category": "breakfast",
        "dietary": ["veg"],
        "mood": ["energetic"],
        "time": ["morning"],
        "description": "Scrambled eggs with bell peppers, spinach, onions served with toast."
    },
    {
        "name": "Smoothie Bowl – Tropical Bliss",
        "calories": 340,
        "protein": 10,
        "carbs": 58,
        "fats": 8,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "energetic"],
        "time": ["morning"],
        "description": "Frozen mango & pineapple blended smooth, topped with coconut and chia seeds."
    },
    {
        "name": "Protein Pancakes with Maple Syrup",
        "calories": 420,
        "protein": 28,
        "carbs": 48,
        "fats": 12,
        "category": "breakfast",
        "dietary": ["veg"],
        "mood": ["happy", "stressed"],
        "time": ["morning"],
        "description": "Fluffy protein-packed pancakes drizzled with pure maple syrup."
    },
    {
        "name": "Chia Seed Pudding with Mango",
        "calories": 280,
        "protein": 8,
        "carbs": 36,
        "fats": 12,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["tired"],
        "time": ["morning"],
        "description": "Overnight chia pudding with coconut milk and fresh mango chunks."
    },
    {
        "name": "Egg White Omelette with Spinach",
        "calories": 180,
        "protein": 22,
        "carbs": 6,
        "fats": 8,
        "category": "breakfast",
        "dietary": ["veg", "keto"],
        "mood": ["energetic"],
        "time": ["morning"],
        "description": "Light and fluffy egg white omelette packed with fresh spinach and feta."
    },
    {
        "name": "Masala Dosa with Coconut Chutney",
        "calories": 370,
        "protein": 8,
        "carbs": 52,
        "fats": 14,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "energetic"],
        "time": ["morning"],
        "description": "Crispy rice & lentil crepe filled with spiced potato, served with chutney."
    },
    {
        "name": "Overnight Oats with Apple & Cinnamon",
        "calories": 310,
        "protein": 10,
        "carbs": 48,
        "fats": 10,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "stressed"],
        "time": ["morning"],
        "description": "Cold-soaked oats with diced apple, cinnamon, and a touch of honey."
    },

    # ======================== LUNCH ========================
    {
        "name": "Grilled Chicken Caesar Salad",
        "calories": 420,
        "protein": 38,
        "carbs": 18,
        "fats": 22,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["energetic", "happy"],
        "time": ["afternoon"],
        "description": "Crisp romaine with grilled chicken, parmesan, croutons, and Caesar dressing."
    },
    {
        "name": "Quinoa Buddha Bowl",
        "calories": 460,
        "protein": 16,
        "carbs": 58,
        "fats": 18,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["energetic", "happy"],
        "time": ["afternoon"],
        "description": "Quinoa with roasted sweet potato, chickpeas, avocado, and tahini dressing."
    },
    {
        "name": "Turkey & Avocado Wrap",
        "calories": 480,
        "protein": 32,
        "carbs": 38,
        "fats": 22,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["energetic"],
        "time": ["afternoon"],
        "description": "Whole wheat wrap with sliced turkey, avocado, lettuce, and mustard."
    },
    {
        "name": "Lentil Soup with Whole Grain Bread",
        "calories": 380,
        "protein": 20,
        "carbs": 52,
        "fats": 8,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "stressed"],
        "time": ["afternoon"],
        "description": "Hearty red lentil soup with cumin and turmeric, served with crusty bread."
    },
    {
        "name": "Grilled Salmon with Steamed Vegetables",
        "calories": 440,
        "protein": 42,
        "carbs": 14,
        "fats": 26,
        "category": "lunch",
        "dietary": ["non-veg", "keto"],
        "mood": ["energetic"],
        "time": ["afternoon"],
        "description": "Perfectly grilled salmon fillet with seasonal steamed vegetables."
    },
    {
        "name": "Chickpea & Spinach Curry with Brown Rice",
        "calories": 480,
        "protein": 18,
        "carbs": 68,
        "fats": 14,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["stressed", "tired"],
        "time": ["afternoon"],
        "description": "Aromatic chickpea curry with fresh spinach, served over fluffy brown rice."
    },
    {
        "name": "Mediterranean Falafel Plate",
        "calories": 520,
        "protein": 18,
        "carbs": 56,
        "fats": 24,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["happy"],
        "time": ["afternoon"],
        "description": "Crispy falafel with hummus, tabbouleh, pickled vegetables, and warm pita."
    },
    {
        "name": "Chicken Stir-Fry with Brown Rice",
        "calories": 490,
        "protein": 36,
        "carbs": 52,
        "fats": 14,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["energetic", "happy"],
        "time": ["afternoon"],
        "description": "Tender chicken strips with colorful veggies in a savory sauce over brown rice."
    },
    {
        "name": "Paneer Tikka Wrap",
        "calories": 450,
        "protein": 22,
        "carbs": 42,
        "fats": 22,
        "category": "lunch",
        "dietary": ["veg"],
        "mood": ["happy", "energetic"],
        "time": ["afternoon"],
        "description": "Spiced paneer tikka with mint chutney, onions, and peppers in a whole wheat wrap."
    },
    {
        "name": "Tuna Poke Bowl",
        "calories": 430,
        "protein": 34,
        "carbs": 48,
        "fats": 12,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["energetic", "happy"],
        "time": ["afternoon"],
        "description": "Fresh tuna with sushi rice, edamame, cucumber, avocado, and soy-ginger dressing."
    },
    {
        "name": "Black Bean Burrito Bowl",
        "calories": 510,
        "protein": 20,
        "carbs": 64,
        "fats": 18,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "stressed"],
        "time": ["afternoon"],
        "description": "Seasoned black beans, cilantro-lime rice, corn salsa, guacamole, and salsa verde."
    },
    {
        "name": "Egg Fried Rice with Vegetables",
        "calories": 420,
        "protein": 14,
        "carbs": 58,
        "fats": 16,
        "category": "lunch",
        "dietary": ["veg"],
        "mood": ["tired", "stressed"],
        "time": ["afternoon"],
        "description": "Quick stir-fried rice with scrambled eggs, peas, carrots, and soy sauce."
    },
    {
        "name": "Caprese Sandwich on Ciabatta",
        "calories": 440,
        "protein": 18,
        "carbs": 42,
        "fats": 24,
        "category": "lunch",
        "dietary": ["veg"],
        "mood": ["happy"],
        "time": ["afternoon"],
        "description": "Fresh mozzarella, tomato, basil, and balsamic glaze on toasted ciabatta."
    },
    {
        "name": "Shrimp Tacos with Mango Salsa",
        "calories": 400,
        "protein": 28,
        "carbs": 38,
        "fats": 16,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["happy", "energetic"],
        "time": ["afternoon"],
        "description": "Grilled shrimp tacos with fresh mango salsa, cabbage slaw, and lime crema."
    },

    # ======================== DINNER ========================
    {
        "name": "Baked Chicken Breast with Sweet Potato",
        "calories": 450,
        "protein": 40,
        "carbs": 38,
        "fats": 14,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["tired", "energetic"],
        "time": ["evening"],
        "description": "Herb-seasoned baked chicken with roasted sweet potato wedges."
    },
    {
        "name": "Vegetable Thai Green Curry",
        "calories": 420,
        "protein": 12,
        "carbs": 48,
        "fats": 20,
        "category": "dinner",
        "dietary": ["veg", "vegan"],
        "mood": ["stressed", "tired"],
        "time": ["evening"],
        "description": "Coconut milk curry with Thai basil, bell peppers, bamboo shoots, and jasmine rice."
    },
    {
        "name": "Grilled Steak with Asparagus",
        "calories": 520,
        "protein": 48,
        "carbs": 8,
        "fats": 32,
        "category": "dinner",
        "dietary": ["non-veg", "keto"],
        "mood": ["energetic", "happy"],
        "time": ["evening"],
        "description": "Perfectly seared steak with grilled asparagus and garlic butter."
    },
    {
        "name": "Mushroom Risotto",
        "calories": 480,
        "protein": 14,
        "carbs": 62,
        "fats": 18,
        "category": "dinner",
        "dietary": ["veg"],
        "mood": ["stressed", "tired"],
        "time": ["evening"],
        "description": "Creamy arborio rice with sautéed wild mushrooms, parmesan, and truffle oil."
    },
    {
        "name": "Baked Salmon with Quinoa Pilaf",
        "calories": 480,
        "protein": 40,
        "carbs": 34,
        "fats": 20,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["tired", "energetic"],
        "time": ["evening"],
        "description": "Lemon-herb baked salmon with fluffy quinoa pilaf and roasted vegetables."
    },
    {
        "name": "Palak Paneer with Roti",
        "calories": 440,
        "protein": 20,
        "carbs": 38,
        "fats": 24,
        "category": "dinner",
        "dietary": ["veg"],
        "mood": ["stressed", "tired"],
        "time": ["evening"],
        "description": "Creamy spinach curry with soft paneer cubes, served with whole wheat roti."
    },
    {
        "name": "Pasta Primavera",
        "calories": 460,
        "protein": 14,
        "carbs": 64,
        "fats": 16,
        "category": "dinner",
        "dietary": ["veg"],
        "mood": ["happy", "stressed"],
        "time": ["evening"],
        "description": "Penne pasta with sautéed seasonal vegetables in a light garlic olive oil sauce."
    },
    {
        "name": "Tofu Teriyaki with Steamed Rice",
        "calories": 400,
        "protein": 18,
        "carbs": 52,
        "fats": 14,
        "category": "dinner",
        "dietary": ["veg", "vegan"],
        "mood": ["happy"],
        "time": ["evening"],
        "description": "Crispy glazed tofu in homemade teriyaki sauce with fluffy steamed rice."
    },
    {
        "name": "Chicken Tikka Masala with Naan",
        "calories": 560,
        "protein": 34,
        "carbs": 48,
        "fats": 24,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["happy", "stressed"],
        "time": ["evening"],
        "description": "Tender chicken in creamy tomato-spice sauce with warm garlic naan."
    },
    {
        "name": "Stuffed Bell Peppers",
        "calories": 380,
        "protein": 16,
        "carbs": 42,
        "fats": 16,
        "category": "dinner",
        "dietary": ["veg"],
        "mood": ["happy"],
        "time": ["evening"],
        "description": "Bell peppers stuffed with rice, black beans, corn, and cheese, then baked."
    },
    {
        "name": "Seared Tuna with Asian Slaw",
        "calories": 360,
        "protein": 38,
        "carbs": 14,
        "fats": 18,
        "category": "dinner",
        "dietary": ["non-veg", "keto"],
        "mood": ["energetic"],
        "time": ["evening"],
        "description": "Sesame-crusted seared tuna with crunchy Asian cabbage slaw."
    },
    {
        "name": "Vegetable Biryani",
        "calories": 460,
        "protein": 12,
        "carbs": 68,
        "fats": 16,
        "category": "dinner",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "stressed"],
        "time": ["evening"],
        "description": "Fragrant basmati rice layered with spiced vegetables, saffron, and fried onions."
    },
    {
        "name": "Grilled Turkey Meatballs with Zucchini Noodles",
        "calories": 350,
        "protein": 32,
        "carbs": 18,
        "fats": 18,
        "category": "dinner",
        "dietary": ["non-veg", "keto"],
        "mood": ["energetic"],
        "time": ["evening"],
        "description": "Lean turkey meatballs in marinara sauce served over spiralized zucchini."
    },
    {
        "name": "Dal Tadka with Jeera Rice",
        "calories": 420,
        "protein": 16,
        "carbs": 62,
        "fats": 12,
        "category": "dinner",
        "dietary": ["veg", "vegan"],
        "mood": ["stressed", "tired"],
        "time": ["evening"],
        "description": "Yellow lentils tempered with garlic, cumin, and ghee, served with cumin rice."
    },
    {
        "name": "Pesto Chicken with Roasted Vegetables",
        "calories": 470,
        "protein": 38,
        "carbs": 22,
        "fats": 26,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["energetic", "happy"],
        "time": ["evening"],
        "description": "Basil pesto-marinated chicken breast with oven-roasted Mediterranean vegetables."
    },

    # ======================== SNACKS ========================
    {
        "name": "Mixed Nuts & Seeds Trail Mix",
        "calories": 180,
        "protein": 6,
        "carbs": 12,
        "fats": 14,
        "category": "snack",
        "dietary": ["veg", "vegan", "keto"],
        "mood": ["tired", "stressed", "energetic"],
        "time": ["morning", "afternoon", "evening"],
        "description": "A crunchy mix of almonds, walnuts, pumpkin seeds, and dried cranberries."
    },
    {
        "name": "Apple Slices with Peanut Butter",
        "calories": 220,
        "protein": 6,
        "carbs": 28,
        "fats": 12,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "stressed"],
        "time": ["morning", "afternoon"],
        "description": "Crisp apple slices with a generous dollop of creamy peanut butter."
    },
    {
        "name": "Protein Bar – Chocolate Chip",
        "calories": 250,
        "protein": 20,
        "carbs": 24,
        "fats": 10,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["tired", "energetic"],
        "time": ["morning", "afternoon"],
        "description": "High-protein bar with chocolate chips – perfect post-workout fuel."
    },
    {
        "name": "Hummus with Carrot & Celery Sticks",
        "calories": 160,
        "protein": 6,
        "carbs": 18,
        "fats": 8,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["energetic", "happy"],
        "time": ["morning", "afternoon", "evening"],
        "description": "Smooth chickpea hummus with crunchy raw vegetable sticks."
    },
    {
        "name": "Dark Chocolate & Almonds",
        "calories": 200,
        "protein": 4,
        "carbs": 18,
        "fats": 14,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["stressed", "happy"],
        "time": ["afternoon", "evening"],
        "description": "Rich 70% dark chocolate squares paired with roasted almonds."
    },
    {
        "name": "Banana Smoothie with Whey Protein",
        "calories": 280,
        "protein": 24,
        "carbs": 34,
        "fats": 6,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["tired", "energetic"],
        "time": ["morning", "afternoon"],
        "description": "Creamy banana smoothie blended with whey protein and a splash of milk."
    },
    {
        "name": "Edamame Pods (Steamed)",
        "calories": 120,
        "protein": 12,
        "carbs": 8,
        "fats": 5,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["energetic"],
        "time": ["afternoon", "evening"],
        "description": "Lightly salted steamed edamame pods – a perfect protein-rich snack."
    },
    {
        "name": "Rice Cakes with Avocado",
        "calories": 170,
        "protein": 3,
        "carbs": 22,
        "fats": 8,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["tired"],
        "time": ["morning", "afternoon"],
        "description": "Crunchy brown rice cakes topped with smashed avocado and chili flakes."
    },
    {
        "name": "Cottage Cheese with Pineapple",
        "calories": 150,
        "protein": 14,
        "carbs": 16,
        "fats": 4,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["happy"],
        "time": ["morning", "afternoon"],
        "description": "Creamy cottage cheese paired with sweet pineapple chunks."
    },
    {
        "name": "Roasted Chickpeas (Spicy)",
        "calories": 140,
        "protein": 6,
        "carbs": 20,
        "fats": 4,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["stressed", "energetic"],
        "time": ["afternoon", "evening"],
        "description": "Crunchy oven-roasted chickpeas seasoned with paprika and cumin."
    },
    {
        "name": "Hard Boiled Eggs (2)",
        "calories": 140,
        "protein": 12,
        "carbs": 1,
        "fats": 10,
        "category": "snack",
        "dietary": ["veg", "keto"],
        "mood": ["tired", "energetic"],
        "time": ["morning", "afternoon"],
        "description": "Two perfectly boiled eggs – simple, portable, and protein-packed."
    },
    {
        "name": "Mango Lassi",
        "calories": 200,
        "protein": 6,
        "carbs": 34,
        "fats": 5,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["happy", "stressed"],
        "time": ["afternoon"],
        "description": "Cool, creamy yogurt drink blended with sweet mango and cardamom."
    },
    {
        "name": "Green Detox Smoothie",
        "calories": 160,
        "protein": 4,
        "carbs": 28,
        "fats": 4,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "energetic"],
        "time": ["morning", "afternoon"],
        "description": "Spinach, cucumber, green apple, ginger, and lemon blended fresh."
    },
    {
        "name": "Yogurt with Honey & Walnuts",
        "calories": 190,
        "protein": 8,
        "carbs": 22,
        "fats": 10,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["stressed", "tired"],
        "time": ["morning", "evening"],
        "description": "Thick natural yogurt drizzled with raw honey and topped with walnuts."
    },
    {
        "name": "Popcorn (Air-Popped, Lightly Salted)",
        "calories": 110,
        "protein": 3,
        "carbs": 22,
        "fats": 2,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "stressed"],
        "time": ["evening"],
        "description": "Light, crunchy air-popped popcorn with just a pinch of sea salt."
    },

    # ======================== EXTRA MEALS ========================
    {
        "name": "Acai Bowl with Granola",
        "calories": 360,
        "protein": 8,
        "carbs": 56,
        "fats": 12,
        "category": "breakfast",
        "dietary": ["veg", "vegan"],
        "mood": ["happy", "energetic"],
        "time": ["morning"],
        "description": "Frozen acai blended thick, topped with granola, banana, and coconut flakes."
    },
    {
        "name": "Tandoori Chicken with Mint Raita",
        "calories": 380,
        "protein": 36,
        "carbs": 12,
        "fats": 22,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["happy", "energetic"],
        "time": ["evening"],
        "description": "Yogurt-marinated tandoori chicken with cooling mint raita."
    },
    {
        "name": "Veggie Sushi Rolls (8 pcs)",
        "calories": 320,
        "protein": 8,
        "carbs": 58,
        "fats": 6,
        "category": "lunch",
        "dietary": ["veg", "vegan"],
        "mood": ["happy"],
        "time": ["afternoon"],
        "description": "Fresh vegetable maki rolls with avocado, cucumber, and pickled ginger."
    },
    {
        "name": "Chicken Shawarma Bowl",
        "calories": 500,
        "protein": 36,
        "carbs": 44,
        "fats": 20,
        "category": "lunch",
        "dietary": ["non-veg"],
        "mood": ["happy", "energetic"],
        "time": ["afternoon"],
        "description": "Spiced shawarma chicken with pickled onions, hummus, and garlic sauce over rice."
    },
    {
        "name": "Sweet Potato & Black Bean Tacos",
        "calories": 420,
        "protein": 14,
        "carbs": 58,
        "fats": 16,
        "category": "dinner",
        "dietary": ["veg", "vegan"],
        "mood": ["happy"],
        "time": ["evening"],
        "description": "Roasted sweet potato & seasoned black beans in corn tortillas with lime slaw."
    },
    {
        "name": "Grilled Fish with Mashed Potatoes",
        "calories": 440,
        "protein": 34,
        "carbs": 38,
        "fats": 18,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["tired", "stressed"],
        "time": ["evening"],
        "description": "Herb-grilled white fish fillet with creamy garlic mashed potatoes."
    },
    {
        "name": "Chole Bhature",
        "calories": 580,
        "protein": 16,
        "carbs": 72,
        "fats": 26,
        "category": "lunch",
        "dietary": ["veg"],
        "mood": ["happy", "stressed"],
        "time": ["afternoon"],
        "description": "Spicy chickpea curry served with fluffy deep-fried bread."
    },
    {
        "name": "Protein Shake – Chocolate",
        "calories": 200,
        "protein": 30,
        "carbs": 12,
        "fats": 4,
        "category": "snack",
        "dietary": ["veg"],
        "mood": ["tired", "energetic"],
        "time": ["morning", "afternoon"],
        "description": "Rich chocolate whey protein shake blended with cold milk."
    },
    {
        "name": "Mediterranean Grilled Chicken Plate",
        "calories": 470,
        "protein": 40,
        "carbs": 28,
        "fats": 22,
        "category": "dinner",
        "dietary": ["non-veg"],
        "mood": ["energetic"],
        "time": ["evening"],
        "description": "Herb-marinated grilled chicken with hummus, olives, feta, and warm pita."
    },
    {
        "name": "Veggie Wrap with Tzatziki",
        "calories": 340,
        "protein": 10,
        "carbs": 42,
        "fats": 14,
        "category": "lunch",
        "dietary": ["veg"],
        "mood": ["happy", "energetic"],
        "time": ["afternoon"],
        "description": "Grilled vegetables with cool tzatziki wrapped in a whole wheat tortilla."
    },
    {
        "name": "Egg Bhurji with Paratha",
        "calories": 440,
        "protein": 18,
        "carbs": 42,
        "fats": 24,
        "category": "breakfast",
        "dietary": ["veg"],
        "mood": ["happy", "energetic"],
        "time": ["morning"],
        "description": "Spicy scrambled eggs Indian-style served with flaky whole wheat paratha."
    },
    {
        "name": "Fruit & Nut Energy Bites (4 pcs)",
        "calories": 180,
        "protein": 5,
        "carbs": 24,
        "fats": 8,
        "category": "snack",
        "dietary": ["veg", "vegan"],
        "mood": ["tired", "stressed"],
        "time": ["morning", "afternoon", "evening"],
        "description": "Date, oat, and nut butter energy balls rolled in coconut."
    },
]


def get_meals_by_filters(dietary=None, category=None, time_of_day=None, mood=None,
                         min_calories=None, max_calories=None):
    """Filter meals based on multiple criteria."""
    results = MEALS.copy()

    if dietary:
        diet_lower = dietary.lower()
        if diet_lower == "non-veg":
            pass  # non-veg people eat everything
        else:
            results = [m for m in results if diet_lower in [d.lower() for d in m["dietary"]]]

    if category:
        results = [m for m in results if m["category"] == category.lower()]

    if time_of_day:
        time_lower = time_of_day.lower()
        results = [m for m in results if time_lower in [t.lower() for t in m["time"]]]

    if mood:
        mood_lower = mood.lower()
        results = [m for m in results if mood_lower in [mo.lower() for mo in m["mood"]]]

    if min_calories is not None:
        results = [m for m in results if m["calories"] >= min_calories]

    if max_calories is not None:
        results = [m for m in results if m["calories"] <= max_calories]

    return results
