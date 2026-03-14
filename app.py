"""
Food IQ - Web Application
=========================
Flask web interface for the Food IQ Diet Planning Application
"""

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import sys
import os

# Add current directory to path to import food_iq module
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Import from food_iq
from food_iq import FoodDatabase, UserProfile, CalorieCalculator, MacroCalculator, MealPlanner

app = Flask(__name__, template_folder='templates')
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.secret_key = 'food_iq_secret_key_2024'

# Enable CORS for cross-origin requests
CORS(app)

# Configure UTF-8 encoding
import sys
import io
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

# Store results in session

# Disease-specific diet configurations
DISEASE_CONFIG = {
    "diabetes": {
        "name": "Diabetes / Sugar (Type 1 & Type 2)",
        "description": "A diet plan designed to help manage blood sugar levels through controlled carbohydrate intake and balanced meals.",
        "macro_type": "low_carb",
        "calorie_adjustment": -300,
        "foods_to_avoid": ["Sugar", "Jaggery", "Honey", "White bread", "Rice", "Potato", "Sweet fruits", "Soda", "Fried foods", "Processed snacks"],
        "foods_to_include": ["Whole grains", "Leafy vegetables", "Non-starchy vegetables", "Legumes", "Nuts", "Seeds", "Eggs", "Fish", "Low-glycemic fruits"],
        "special_instructions": "Focus on low glycemic index foods. Eat small, frequent meals to avoid blood sugar spikes."
    },
    "pcos": {
        "name": "PCOS (Polycystic Ovary Syndrome)",
        "description": "A balanced diet to help manage insulin resistance, hormone balance, and weight management.",
        "macro_type": "balanced",
        "calorie_adjustment": -200,
        "foods_to_avoid": ["Sugar", "Processed foods", "Refined carbs", "Fried foods", "Dairy (excess)", "Red meat"],
        "foods_to_include": ["Whole grains", "Fiber-rich vegetables", "Lean protein", "Healthy fats", "Flaxseeds", "Cinnamon", "Green tea"],
        "special_instructions": "Focus on anti-inflammatory foods and maintaining stable blood sugar levels."
    },
    "pcod": {
        "name": "PCOD (Polycystic Ovarian Disease)",
        "description": "A diet plan to support hormonal balance and ovarian health.",
        "macro_type": "balanced",
        "calorie_adjustment": -150,
        "foods_to_avoid": ["Sugar", "Caffeine", "Alcohol", "Processed foods", "Trans fats"],
        "foods_to_include": ["Fresh vegetables", "Fruits", "Whole grains", "Lean proteins", "Healthy fats", "Vitamin D rich foods"],
        "special_instructions": "Maintain regular meal timings and avoid skipping meals."
    },
    "hypertension": {
        "name": "High Blood Pressure (Hypertension)",
        "description": "A heart-healthy diet low in sodium to help control blood pressure.",
        "macro_type": "heart_healthy",
        "calorie_adjustment": 0,
        "foods_to_avoid": ["Salt", "Soy sauce", "Processed foods", "Canned foods", "Pickles", "Fried foods", "Red meat"],
        "foods_to_include": ["Potassium-rich foods", "Leafy greens", "Bananas", "Beetroot", "Oats", "Fish", "Berries", "Garlic"],
        "special_instructions": "Limit sodium intake to less than 2300mg per day. Use herbs and spices instead of salt."
    },
    "hypothyroid": {
        "name": "Hypothyroid / Thyroid",
        "description": "A diet to support thyroid function with iodine, selenium, and zinc.",
        "macro_type": "balanced",
        "calorie_adjustment": -100,
        "foods_to_avoid": ["Goitrogenic foods (raw cabbage, broccoli, cauliflower)", "Soy products", "Gluten", "Processed foods"],
        "foods_to_include": ["Iodine-rich foods", "Selenium-rich foods", "Zinc-rich foods", "Lean proteins", "Fruits", "Vegetables"],
        "special_instructions": "Take thyroid medication on empty stomach and wait 30-60 minutes before eating."
    },
    "hyperthyroid": {
        "name": "Hyperthyroid",
        "description": "A diet to manage increased metabolism and support overall health.",
        "macro_type": "high_protein",
        "calorie_adjustment": 300,
        "foods_to_avoid": ["Caffeine", "Sugar", "Iodine-rich foods (excess)", "Spicy foods"],
        "foods_to_include": ["High-calorie healthy foods", "Protein-rich foods", "Complex carbs", "Calcium-rich foods", "Vitamin D sources"],
        "special_instructions": "Eat frequent, nutritious meals to meet increased caloric needs."
    },
    "anemia": {
        "name": "Anemia (Iron Deficiency)",
        "description": "An iron-rich diet to boost hemoglobin and energy levels.",
        "macro_type": "iron_rich",
        "calorie_adjustment": 100,
        "foods_to_avoid": ["Tea", "Coffee", "Calcium-rich foods with iron meals", "Processed foods"],
        "foods_to_include": ["Iron-rich foods", "Vitamin C sources", "Folate-rich foods", "Lean meats", "Spinach", "Lentils", "Beans"],
        "special_instructions": "Combine iron-rich foods with vitamin C for better absorption. Avoid tea/coffee with meals."
    },
    "obesity": {
        "name": "Obesity / Weight Management",
        "description": "A calorie-controlled diet for healthy weight loss and sustainable results.",
        "macro_type": "low_calorie",
        "calorie_adjustment": -500,
        "foods_to_avoid": ["Sugar", "Fried foods", "Processed snacks", "Soda", "Alcohol", "White bread"],
        "foods_to_include": ["High-fiber foods", "Lean proteins", "Vegetables", "Fruits", "Whole grains", "Water"],
        "special_instructions": "Create a calorie deficit through diet and exercise. Focus on portion control."
    },
    "heart_disease": {
        "name": "Heart Disease / High Cholesterol",
        "description": "A heart-healthy diet low in saturated fats and cholesterol.",
        "macro_type": "heart_healthy",
        "calorie_adjustment": -200,
        "foods_to_avoid": ["Saturated fats", "Trans fats", "Fried foods", "Red meat", "Full-fat dairy", "Egg yolks", "Processed meats"],
        "foods_to_include": ["Oats", "Barley", "Beans", "Eggplant", "Fatty fish", "Nuts", "Olive oil", "Fruits", "Vegetables"],
        "special_instructions": "Focus on omega-3 fatty acids and fiber. Limit sodium for blood pressure control."
    },
    "kidney_disease": {
        "name": "Kidney Disease",
        "description": "A kidney-friendly diet to reduce waste buildup and protect kidney function.",
        "macro_type": "kidney_friendly",
        "calorie_adjustment": 0,
        "foods_to_avoid": ["High-sodium foods", "Potassium-rich foods (bananas, oranges)", "Phosphorus-rich foods", "Protein (excess)", "Dairy (excess)"],
        "foods_to_include": ["Low-potassium fruits", "Low-phosphorus foods", "Lean proteins (controlled)", "Rice", "Cauliflower", "Bell peppers"],
        "special_instructions": "Limit sodium, potassium, and phosphorus. Consult a nephrologist for personalized advice."
    },
    "acid_reflux": {
        "name": "Acid Reflux / GERD",
        "description": "A diet to reduce acid production and prevent heartburn.",
        "macro_type": "low_acid",
        "calorie_adjustment": 0,
        "foods_to_avoid": ["Citrus fruits", "Tomatoes", "Spicy foods", "Caffeine", "Chocolate", "Mint", "Fried foods", "Carbonated drinks"],
        "foods_to_include": ["Oatmeal", "Ginger", "Lean proteins", "Non-citrus fruits", "Vegetables", "Alkaline foods"],
        "special_instructions": "Eat smaller meals, avoid eating 2-3 hours before bedtime. Stay upright after meals."
    },
    "arthritis": {
        "name": "Arthritis / Joint Pain",
        "description": "An anti-inflammatory diet to reduce joint pain and stiffness.",
        "macro_type": "anti_inflammatory",
        "calorie_adjustment": 0,
        "foods_to_avoid": ["Processed foods", "Sugar", "Refined carbs", "Trans fats", "Red meat", "Alcohol", "Nightshades"],
        "foods_to_include": ["Fatty fish", "Olive oil", "Turmeric", "Ginger", "Berries", "Leafy greens", "Nuts", "Seeds"],
        "special_instructions": "Focus on omega-3 fatty acids and antioxidants. Maintain healthy weight to reduce joint stress."
    },
    "asthma": {
        "name": "Asthma / Respiratory Issues",
        "description": "An anti-inflammatory diet to support lung health and reduce asthma triggers.",
        "macro_type": "anti_inflammatory",
        "calorie_adjustment": 0,
        "foods_to_avoid": ["Sulfites", "Processed foods", "Food preservatives", "Dairy (if sensitive)", "Fried foods"],
        "foods_to_include": ["Fruits rich in vitamin C", "Vegetables", "Omega-3 rich foods", "Whole grains", "Turmeric", "Ginger"],
        "special_instructions": "Stay hydrated. Include anti-inflammatory foods. Avoid known food triggers."
    },
    "skin_issues": {
        "name": "Skin Issues / Acne",
        "description": "A skin-friendly diet to reduce inflammation and promote clear skin.",
        "macro_type": "low_glycemic",
        "calorie_adjustment": -100,
        "foods_to_avoid": ["Sugar", "Dairy", "Processed foods", "Fried foods", "Refined carbs", "Chocolate", "Fast food"],
        "foods_to_include": ["Water", "Leafy greens", "Colorful vegetables", "Lean proteins", "Omega-3 rich foods", "Probiotic foods"],
        "special_instructions": "Stay hydrated and eat a low-glycemic diet. Limit dairy and sugar intake."
    }
}

# Macro configurations for different diet types
MACRO_CONFIGS = {
    "balanced": {"protein_ratio": 0.20, "carbs_ratio": 0.50, "fats_ratio": 0.30},
    "low_carb": {"protein_ratio": 0.30, "carbs_ratio": 0.30, "fats_ratio": 0.40},
    "high_protein": {"protein_ratio": 0.25, "carbs_ratio": 0.40, "fats_ratio": 0.35},
    "heart_healthy": {"protein_ratio": 0.20, "carbs_ratio": 0.55, "fats_ratio": 0.25},
    "low_calorie": {"protein_ratio": 0.25, "carbs_ratio": 0.45, "fats_ratio": 0.30},
    "iron_rich": {"protein_ratio": 0.25, "carbs_ratio": 0.50, "fats_ratio": 0.25},
    "kidney_friendly": {"protein_ratio": 0.15, "carbs_ratio": 0.60, "fats_ratio": 0.25},
    "low_acid": {"protein_ratio": 0.20, "carbs_ratio": 0.55, "fats_ratio": 0.25},
    "anti_inflammatory": {"protein_ratio": 0.20, "carbs_ratio": 0.50, "fats_ratio": 0.30},
    "low_glycemic": {"protein_ratio": 0.25, "carbs_ratio": 0.40, "fats_ratio": 0.35},
}

# Exercise recommendations based on goal
EXERCISE_PLANS = {
    "1": {  # Lose Weight - Cardio + Strength
        "title": "Weight Loss Exercise Plan",
        "description": "A combination of cardio and strength training to maximize fat burning while preserving muscle mass.",
        "weekly_schedule": {
            "Monday": {
                "type": "Cardio + Core",
                "exercises": [
                    "30 min brisk walking or jogging",
                    "15 min jumping jacks",
                    "3 sets of 15 planks",
                    "3 sets of 20 mountain climbers",
                    "15 min HIIT intervals"
                ],
                "duration": "45-60 minutes",
                "calories_burn": "400-500"
            },
            "Tuesday": {
                "type": "Strength Training - Upper Body",
                "exercises": [
                    "3 sets of 12 push-ups",
                    "3 sets of 15 dumbbell rows",
                    "3 sets of 10 shoulder press",
                    "3 sets of 15 bicep curls",
                    "3 sets of 12 tricep dips"
                ],
                "duration": "45 minutes",
                "calories_burn": "250-300"
            },
            "Wednesday": {
                "type": "Cardio",
                "exercises": [
                    "20 min jogging",
                    "20 min cycling",
                    "10 min jumping rope",
                    "15 min burpees"
                ],
                "duration": "60 minutes",
                "calories_burn": "450-550"
            },
            "Thursday": {
                "type": "Strength Training - Lower Body",
                "exercises": [
                    "3 sets of 15 squats",
                    "3 sets of 12 lunges",
                    "3 sets of 20 calf raises",
                    "3 sets of 15 glute bridges",
                    "3 sets of 30 seconds wall sit"
                ],
                "duration": "45 minutes",
                "calories_burn": "250-300"
            },
            "Friday": {
                "type": "Cardio + Full Body",
                "exercises": [
                    "25 min running",
                    "3 sets of 10 burpees",
                    "3 sets of 20 high knees",
                    "15 min battle ropes",
                    "10 min stretching"
                ],
                "duration": "55 minutes",
                "calories_burn": "400-500"
            },
            "Saturday": {
                "type": "Active Recovery",
                "exercises": [
                    "30 min brisk walking",
                    "20 min yoga",
                    "15 min stretching",
                    "Light swimming optional"
                ],
                "duration": "30-45 minutes",
                "calories_burn": "150-200"
            },
            "Sunday": {
                "type": "Rest Day",
                "exercises": [
                    "Light stretching",
                    "15 min meditation",
                    "Optional: 20 min leisure walk"
                ],
                "duration": "20-30 minutes",
                "calories_burn": "50-100"
            }
        },
        "tips": [
            "Stay hydrated - drink water before, during, and after exercise",
            "Do 5-10 minute warm-up before each session",
            "Include protein within 30 minutes after workout",
            "Gradually increase intensity over weeks",
            "Get 7-8 hours of sleep for recovery"
        ]
    },
    "2": {  # Maintain Weight - Cardio + Strength
        "title": "Weight Maintenance Exercise Plan",
        "description": "A balanced exercise routine combining cardio and strength training to maintain your current weight and fitness level.",
        "weekly_schedule": {
            "Monday": {
                "type": "Cardio",
                "exercises": [
                    "25 min jogging",
                    "15 min cycling",
                    "10 min jumping rope",
                    "10 min hill sprints"
                ],
                "duration": "50 minutes",
                "calories_burn": "350-450"
            },
            "Tuesday": {
                "type": "Strength Training - Full Body",
                "exercises": [
                    "3 sets of 12 push-ups",
                    "3 sets of 15 squats",
                    "3 sets of 10 lunges",
                    "3 sets of 12 dumbbell rows",
                    "3 sets of 30 seconds plank"
                ],
                "duration": "45 minutes",
                "calories_burn": "200-250"
            },
            "Wednesday": {
                "type": "Cardio + HIIT",
                "exercises": [
                    "20 min brisk walking",
                    "15 min HIIT intervals",
                    "10 min jump rope",
                    "5 min cool down walk"
                ],
                "duration": "45 minutes",
                "calories_burn": "300-400"
            },
            "Thursday": {
                "type": "Strength Training - Upper Body",
                "exercises": [
                    "3 sets of 15 shoulder press",
                    "3 sets of 12 bicep curls",
                    "3 sets of 12 tricep dips",
                    "3 sets of 10 lat pull-downs",
                    "3 sets of 15 front raises"
                ],
                "duration": "40 minutes",
                "calories_burn": "180-220"
            },
            "Friday": {
                "type": "Cardio",
                "exercises": [
                    "30 min running",
                    "15 min swimming",
                    "10 min cycling",
                    "5 min stretching"
                ],
                "duration": "55 minutes",
                "calories_burn": "400-500"
            },
            "Saturday": {
                "type": "Strength + Flexibility",
                "exercises": [
                    "3 sets of 12 glute bridges",
                    "3 sets of 15 calf raises",
                    "3 sets of 20 mountain climbers",
                    "20 min yoga",
                    "10 min stretching"
                ],
                "duration": "45 minutes",
                "calories_burn": "200-250"
            },
            "Sunday": {
                "type": "Rest Day",
                "exercises": [
                    "20 min light stretching",
                    "15 min yoga",
                    "Optional: 30 min leisure walk"
                ],
                "duration": "20-30 minutes",
                "calories_burn": "50-100"
            }
        },
        "tips": [
            "Maintain consistency with your workout schedule",
            "Mix up exercises to prevent boredom",
            "Include protein in post-workout meals",
            "Stay active throughout the day",
            "Get adequate sleep for muscle recovery"
        ]
    },
    "3": {  # Gain Weight - Strength Training Focus
        "title": "Weight Gain Exercise Plan",
        "description": "A strength-focused exercise program to build muscle mass and increase strength. Minimal cardio to preserve calories.",
        "weekly_schedule": {
            "Monday": {
                "type": "Strength - Chest & Triceps",
                "exercises": [
                    "4 sets of 8-10 bench press",
                    "4 sets of 10 push-ups",
                    "3 sets of 12 incline dumbbell press",
                    "3 sets of 15 tricep dips",
                    "3 sets of 12 cable flyes",
                    "3 sets of 15 skull crushers"
                ],
                "duration": "60 minutes",
                "calories_burn": "250-300"
            },
            "Tuesday": {
                "type": "Strength - Back & Biceps",
                "exercises": [
                    "4 sets of 8 pull-ups or lat pulldowns",
                    "3 sets of 12 barbell rows",
                    "3 sets of 12 dumbbell rows",
                    "3 sets of 15 bicep curls",
                    "3 sets of 12 hammer curls",
                    "3 sets of 10 back extensions"
                ],
                "duration": "60 minutes",
                "calories_burn": "250-300"
            },
            "Wednesday": {
                "type": "Light Cardio + Stretching",
                "exercises": [
                    "20 min light cycling",
                    "15 min brisk walking",
                    "20 min full body stretching",
                    "15 min yoga for recovery"
                ],
                "duration": "60 minutes",
                "calories_burn": "150-200"
            },
            "Thursday": {
                "type": "Strength - Legs & Glutes",
                "exercises": [
                    "4 sets of 8-10 barbell squats",
                    "3 sets of 12 leg press",
                    "3 sets of 12 lunges",
                    "3 sets of 15 leg curls",
                    "3 sets of 20 calf raises",
                    "3 sets of 15 glute bridges"
                ],
                "duration": "60 minutes",
                "calories_burn": "300-350"
            },
            "Friday": {
                "type": "Strength - Shoulders & Arms",
                "exercises": [
                    "4 sets of 8 overhead press",
                    "3 sets of 12 lateral raises",
                    "3 sets of 12 front raises",
                    "3 sets of 15 face pulls",
                    "3 sets of 12 preacher curls",
                    "3 sets of 12 tricep pushdowns"
                ],
                "duration": "55 minutes",
                "calories_burn": "220-280"
            },
            "Saturday": {
                "type": "Strength - Full Body Compound",
                "exercises": [
                    "4 sets of 6 deadlifts",
                    "3 sets of 10 bench press",
                    "3 sets of 10 barbell rows",
                    "3 sets of 12 squats",
                    "3 sets of 8 overhead press",
                    "3 sets of 15 pull-ups"
                ],
                "duration": "70 minutes",
                "calories_burn": "350-400"
            },
            "Sunday": {
                "type": "Rest Day",
                "exercises": [
                    "20 min light stretching",
                    "15 min foam rolling",
                    "10 min meditation",
                    "Optional: 20 min leisure walk"
                ],
                "duration": "30-45 minutes",
                "calories_burn": "50-100"
            }
        },
        "tips": [
            "Consume 300-500 extra calories daily for muscle gain",
            "Eat protein within 30 minutes after workout",
            "Get 8-9 hours of sleep for optimal recovery",
            "Use progressive overload - increase weight gradually",
            "Rest muscles 48 hours between heavy sessions"
        ]
    }
}

@app.route('/dashboard')
def dashboard():
    """Dashboard page showing analytics and history"""
    return render_template('dashboard.html')

@app.route('/auth')
def auth():
    """Login/Register page"""
    return render_template('auth.html')

@app.route('/home')
def home():
    """Home/Landing page"""
    return render_template('home.html')

@app.route('/plan')
def plan():
    """Diet plan form page"""
    return render_template('index.html')

@app.route('/')
def index():
    """Main page - redirect to home"""
    return render_template('home.html')

@app.route('/calculate', methods=['POST'])
def calculate():
    """Process user input and calculate results"""
    try:
        # Validate and get form data
        try:
            age = int(request.form.get('age', 25))
            weight = float(request.form.get('weight', 70))
            height = float(request.form.get('height', 170))
        except ValueError as ve:
            return render_template('index.html', error="Please enter valid numbers for age, weight, and height.")
        
        # Validate input ranges
        if age < 1 or age > 120:
            return render_template('index.html', error="Please enter a valid age between 1 and 120.")
        if weight < 20 or weight > 500:
            return render_template('index.html', error="Please enter a valid weight between 20 and 500 kg.")
        if height < 50 or height > 300:
            return render_template('index.html', error="Please enter a valid height between 50 and 300 cm.")
        
        # Create instances
        food_db = FoodDatabase()
        
        # Get form data
        profile = UserProfile()
        profile.name = request.form.get('name', 'User')
        profile.age = age
        profile.gender = request.form.get('gender', 'M')
        profile.weight = weight
        profile.height = height
        profile.activity_level = request.form.get('activity_level', '3')
        profile.goal = request.form.get('goal', '2')
        profile.diet_preference = request.form.get('diet_preference', '1')
        
        # Get health condition if selected
        health_condition = request.form.get('health_condition', '')
        disease_info = None
        if health_condition and health_condition in DISEASE_CONFIG:
            disease_info = DISEASE_CONFIG[health_condition]
        
        # Calculate BMR
        calculator = CalorieCalculator()
        bmr = calculator.calculate_bmr(
            profile.age,
            profile.gender,
            profile.weight,
            profile.height
        )
        
        # Calculate TDEE
        activity_multiplier = UserProfile.ACTIVITY_LEVELS[profile.activity_level]['multiplier']
        tdee = calculator.calculate_tdee(bmr, activity_multiplier)
        
        # Calculate daily calories based on goal
        goal_adjustment = UserProfile.GOALS[profile.goal]['calorie_adjustment']
        daily_calories = calculator.calculate_daily_calories(tdee, goal_adjustment)
        
        # Apply disease-specific calorie adjustment
        if disease_info:
            disease_calorie_adjustment = disease_info.get('calorie_adjustment', 0)
            daily_calories = max(1200, daily_calories + disease_calorie_adjustment)  # Ensure minimum 1200 cal
        
        # Calculate macros (using balanced ratio as default)
        macro_calc = MacroCalculator()
        macro_type = 'balanced'
        if disease_info:
            macro_type = disease_info.get('macro_type', 'balanced')
        
        # Map our macro types to the app's macro ratios
        macro_config = MACRO_CONFIGS.get(macro_type, MACRO_CONFIGS['balanced'])
        
        # Calculate macros using custom ratios
        protein = int(daily_calories * macro_config['protein_ratio'] / 4)  # 4 cal per gram
        carbs = int(daily_calories * macro_config['carbs_ratio'] / 4)  # 4 cal per gram
        fats = int(daily_calories * macro_config['fats_ratio'] / 9)  # 9 cal per gram
        
        macros = {
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
        }
        
        # Generate weekly meal plan (varied, no repeats)
        meal_planner = MealPlanner(food_db, profile.diet_preference)
        meal_plan = meal_planner.generate_weekly_meal_plan(daily_calories, macros)
        
        # Calculate water intake based on weight and protein intake
        # Base: 40ml per kg body weight (increased for better hydration)
        # Additional: 15ml per gram of protein (protein metabolism requires more water)
        base_water = int(profile.weight * 40)
        protein_extra = max(0, (macros['protein'] - 100) * 15)
        water_ml = base_water + protein_extra
        water_glasses = int(water_ml / 250)
        
        # Get tips based on goal and disease
        tips = get_tips(profile.goal, health_condition)
        
        # Prepare results data
        results = {
            'profile': {
                'name': profile.name,
                'age': profile.age,
                'gender': 'Male' if profile.gender == 'M' else 'Female',
                'weight': profile.weight,
                'height': profile.height,
                'activity': UserProfile.ACTIVITY_LEVELS[profile.activity_level]['name'],
                'goal': UserProfile.GOALS[profile.goal]['name'],
                'diet': UserProfile.DIET_PREFERENCES[profile.diet_preference]['name'],
            },
            'calories': {
                'bmr': bmr,
                'tdee': tdee,
                'daily_target': daily_calories,
            },
            'macros': macros,
            'meal_plan': meal_plan,
            'water': {
                'ml': water_ml,
                'glasses': water_glasses,
            },
            'tips': tips,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Add disease information if selected
        if disease_info:
            results['disease'] = {
                'name': disease_info['name'],
                'description': disease_info['description'],
                'foods_to_avoid': disease_info['foods_to_avoid'],
                'foods_to_include': disease_info['foods_to_include'],
                'special_instructions': disease_info['special_instructions'],
                'macro_type': macro_type,
            }
        
        # Add exercise plan based on goal
        exercise_plan = EXERCISE_PLANS.get(profile.goal)
        if exercise_plan:
            results['exercise'] = exercise_plan
        
        # Save results to file (try without failing)
        try:
            save_results(results)
        except Exception as save_error:
            pass  # Ignore save errors
        
        return render_template('results.html', results=results)
        
    except Exception as e:
        return render_template('index.html', error=f"An error occurred while generating your diet plan. Please try again.")

def get_tips(goal, health_condition=''):
    """Get tips based on user's goal and health condition"""
    # Base tips by goal
    base_tips = {
        "1": [  # Lose weight
            "Eat protein-rich foods to maintain muscle mass",
            "Include fiber in every meal for fullness",
            "Avoid sugary drinks and processed foods",
            "Practice portion control - use smaller plates",
            "Get 7-8 hours of quality sleep",
        ],
        "2": [  # Maintain
            "Maintain a balanced diet with all food groups",
            "Continue regular physical activity",
            "Monitor your weight weekly",
            "Stay hydrated throughout the day",
        ],
        "3": [  # Gain
            "Eat calorie-dense foods like nuts and avocados",
            "Increase protein intake for muscle building",
            "Strength training 3-4 times per week",
            "Eat larger portions or add extra snacks",
        ],
    }
    
    tips = base_tips.get(goal, base_tips["2"])
    
    # Add disease-specific tips
    if health_condition and health_condition in DISEASE_CONFIG:
        disease_tips = {
            "diabetes": [
                "Monitor your blood sugar levels regularly",
                "Eat small, frequent meals to avoid spikes",
                "Choose low glycemic index foods",
                "Include protein with every meal",
                "Stay physically active",
            ],
            "pcos": [
                "Focus on low glycemic index foods",
                "Include anti-inflammatory foods",
                "Maintain regular meal timings",
                "Exercise regularly to improve insulin sensitivity",
                "Consider spearmint tea for hormone balance",
            ],
            "pcod": [
                "Eat a balanced diet with all nutrients",
                "Limit processed foods and sugar",
                "Include omega-3 fatty acids",
                "Stay active with regular exercise",
                "Manage stress through yoga or meditation",
            ],
            "hypertension": [
                "Reduce sodium intake significantly",
                "Eat potassium-rich foods",
                "Limit alcohol consumption",
                "Exercise regularly for heart health",
                "Monitor blood pressure at home",
            ],
            "hypothyroid": [
                "Include iodine-rich foods in your diet",
                "Eat selenium-rich foods like Brazil nuts",
                "Avoid goitrogenic foods in excess",
                "Take medication on empty stomach",
                "Get regular thyroid function tests",
            ],
            "hyperthyroid": [
                "Eat calorie-dense nutritious foods",
                "Include calcium and vitamin D rich foods",
                "Avoid caffeine and stimulants",
                "Rest adequately between activities",
                "Consult your endocrinologist regularly",
            ],
            "anemia": [
                "Eat iron-rich foods with vitamin C",
                "Include leafy greens and legumes",
                "Avoid tea/coffee with iron-rich meals",
                "Consider iron supplements if prescribed",
                "Get regular blood tests to monitor levels",
            ],
            "obesity": [
                "Create a sustainable calorie deficit",
                "Eat high-volume low-calorie foods",
                "Practice mindful eating",
                "Stay hydrated before meals",
                "Aim for gradual, sustainable weight loss",
            ],
            "heart_disease": [
                "Choose heart-healthy fats",
                "Eat plenty of fiber-rich foods",
                "Limit saturated and trans fats",
                "Exercise as recommended by your doctor",
                "Take medications as prescribed",
            ],
            "kidney_disease": [
                "Follow your nephrologist's dietary advice",
                "Monitor potassium and phosphorus intake",
                "Choose low-sodium options",
                "Stay hydrated appropriately",
                "Get regular kidney function tests",
            ],
            "acid_reflux": [
                "Eat smaller, more frequent meals",
                "Avoid eating 2-3 hours before bedtime",
                "Stay upright after meals",
                "Identify and avoid trigger foods",
                "Maintain a healthy weight",
            ],
            "arthritis": [
                "Include anti-inflammatory omega-3 foods",
                "Eat colorful fruits and vegetables",
                "Maintain a healthy weight",
                "Stay active with low-impact exercises",
                "Consider turmeric and ginger",
            ],
            "asthma": [
                "Eat anti-inflammatory foods",
                "Stay hydrated for better lung function",
                "Avoid known food triggers",
                "Include vitamin C rich foods",
                "Exercise appropriately for your condition",
            ],
            "skin_issues": [
                "Stay hydrated with plenty of water",
                "Eat antioxidant-rich foods",
                "Limit dairy and sugar intake",
                "Include omega-3 fatty acids",
                "Get adequate sleep for skin repair",
            ],
        }
        
        if health_condition in disease_tips:
            tips = tips + disease_tips[health_condition]
    
    return tips

def save_results(results):
    """Save results to a text file"""
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    filename = f"food_iq_results_{timestamp}.txt"
    
    with open(filename, 'w') as f:
        f.write("=" * 60 + "\n")
        f.write("FOOD IQ - PERSONALIZED DIET PLAN RESULTS\n")
        f.write("=" * 60 + "\n\n")
        f.write(f"Generated: {results['timestamp']}\n\n")
        
        f.write("USER PROFILE\n")
        f.write("-" * 40 + "\n")
        f.write(f"Name: {results['profile']['name']}\n")
        f.write(f"Age: {results['profile']['age']}\n")
        f.write(f"Gender: {results['profile']['gender']}\n")
        f.write(f"Weight: {results['profile']['weight']} kg\n")
        f.write(f"Height: {results['profile']['height']} cm\n")
        f.write(f"Activity: {results['profile']['activity']}\n")
        f.write(f"Goal: {results['profile']['goal']}\n\n")
        
        f.write("CALORIE REQUIREMENTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"BMR: {results['calories']['bmr']} calories/day\n")
        f.write(f"TDEE: {results['calories']['tdee']} calories/day\n")
        f.write(f"Daily Target: {results['calories']['daily_target']} calories/day\n\n")
        
        f.write("MACRO NUTRIENTS\n")
        f.write("-" * 40 + "\n")
        f.write(f"Protein: {results['macros']['protein']}g\n")
        f.write(f"Carbs: {results['macros']['carbs']}g\n")
        f.write(f"Fats: {results['macros']['fats']}g\n\n")
        
        f.write("MEAL PLAN\n")
        f.write("-" * 40 + "\n\n")
        
        meal_types = {"breakfast": "BREAKFAST", "brunch": "BRUNCH", "lunch": "LUNCH", "snacks": "SNACKS", "dinner": "DINNER"}
        
        for meal_type, meal in results['meal_plan'].items():
            meal_label = meal_types.get(meal_type, meal_type.upper())
            f.write(f"{meal_label}: {meal['name']}\n")
            f.write(f"   Foods: {', '.join(meal['foods'])}\n")
            f.write(f"   Calories: {meal['nutrition']['calories']}\n\n")

@app.route('/api/diet-plan', methods=['POST'])
def api_diet_plan():
    """API endpoint that returns diet plan as JSON"""
    try:
        # Accept JSON or form data
        if request.is_json:
            data = request.get_json()
        else:
            data = request.form
        
        # Validate and get data
        try:
            age = int(data.get('age', 25))
            weight = float(data.get('weight', 70))
            height = float(data.get('height', 170))
        except (ValueError, TypeError) as ve:
            return jsonify({'status': 'error', 'message': 'Please enter valid numbers for age, weight, and height.'}), 400
        
        # Validate input ranges
        if age < 1 or age > 120:
            return jsonify({'status': 'error', 'message': 'Please enter a valid age between 1 and 120.'}), 400
        if weight < 20 or weight > 500:
            return jsonify({'status': 'error', 'message': 'Please enter a valid weight between 20 and 500 kg.'}), 400
        if height < 50 or height > 300:
            return jsonify({'status': 'error', 'message': 'Please enter a valid height between 50 and 300 cm.'}), 400
        
        # Create instances
        food_db = FoodDatabase()
        
        # Get data
        profile = UserProfile()
        profile.name = data.get('name', 'User')
        profile.age = age
        profile.gender = data.get('gender', 'M')
        profile.weight = weight
        profile.height = height
        profile.activity_level = data.get('activity_level', '3')
        profile.goal = data.get('goal', '2')
        profile.diet_preference = data.get('diet_preference', '1')
        
        # Get health condition if selected
        health_condition = data.get('health_condition', '')
        disease_info = None
        if health_condition and health_condition in DISEASE_CONFIG:
            disease_info = DISEASE_CONFIG[health_condition]
        
        # Calculate BMR
        calculator = CalorieCalculator()
        bmr = calculator.calculate_bmr(
            profile.age,
            profile.gender,
            profile.weight,
            profile.height
        )
        
        # Calculate TDEE
        activity_multiplier = UserProfile.ACTIVITY_LEVELS[profile.activity_level]['multiplier']
        tdee = calculator.calculate_tdee(bmr, activity_multiplier)
        
        # Calculate daily calories based on goal
        goal_adjustment = UserProfile.GOALS[profile.goal]['calorie_adjustment']
        daily_calories = calculator.calculate_daily_calories(tdee, goal_adjustment)
        
        # Apply disease-specific calorie adjustment
        if disease_info:
            disease_calorie_adjustment = disease_info.get('calorie_adjustment', 0)
            daily_calories = max(1200, daily_calories + disease_calorie_adjustment)
        
        # Calculate macros
        macro_calc = MacroCalculator()
        macro_type = 'balanced'
        if disease_info:
            macro_type = disease_info.get('macro_type', 'balanced')
        
        # Map our macro types to the app's macro ratios
        macro_config = MACRO_CONFIGS.get(macro_type, MACRO_CONFIGS['balanced'])
        
        # Calculate macros using custom ratios
        protein = int(daily_calories * macro_config['protein_ratio'] / 4)  # 4 cal per gram
        carbs = int(daily_calories * macro_config['carbs_ratio'] / 4)  # 4 cal per gram
        fats = int(daily_calories * macro_config['fats_ratio'] / 9)  # 9 cal per gram
        
        macros = {
            'protein': protein,
            'carbs': carbs,
            'fats': fats,
        }
        
        # Generate weekly meal plan (varied, no repeats)
        meal_planner = MealPlanner(food_db, profile.diet_preference)
        meal_plan = meal_planner.generate_weekly_meal_plan(daily_calories, macros)
        
        # Calculate water intake based on weight and protein intake
        # Base: 40ml per kg body weight (increased for better hydration)
        # Additional: 15ml per gram of protein (protein metabolism requires more water)
        base_water = int(profile.weight * 40)
        protein_extra = max(0, (macros['protein'] - 100) * 15)
        water_ml = base_water + protein_extra
        water_glasses = int(water_ml / 250)
        
        # Get tips
        tips = get_tips(profile.goal, health_condition)
        
        results = {
            'status': 'success',
            'profile': {
                'name': profile.name,
                'age': profile.age,
                'gender': 'Male' if profile.gender == 'M' else 'Female',
                'weight': profile.weight,
                'height': profile.height,
                'activity': UserProfile.ACTIVITY_LEVELS[profile.activity_level]['name'],
                'goal': UserProfile.GOALS[profile.goal]['name'],
                'diet': UserProfile.DIET_PREFERENCES[profile.diet_preference]['name'],
            },
            'calories': {
                'bmr': bmr,
                'tdee': tdee,
                'daily_target': daily_calories,
            },
            'macros': macros,
            'meal_plan': meal_plan,
            'water': {
                'ml': water_ml,
                'glasses': water_glasses,
            },
            'tips': tips,
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        }
        
        # Add disease information if selected
        if disease_info:
            results['disease'] = {
                'name': disease_info['name'],
                'description': disease_info['description'],
                'foods_to_avoid': disease_info['foods_to_avoid'],
                'foods_to_include': disease_info['foods_to_include'],
                'special_instructions': disease_info['special_instructions'],
                'macro_type': macro_type,
            }
        
        return jsonify(results)
        
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


# Meal Status & User Management
MEAL_STATUS_FILE = 'meal_status.json'
USER_DB_FILE = 'users.json'

def load_meal_status():
    """Load meal status from JSON file"""
    try:
        if os.path.exists(MEAL_STATUS_FILE):
            with open(MEAL_STATUS_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_meal_status(data):
    """Save meal status to JSON file"""
    try:
        with open(MEAL_STATUS_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def load_users():
    """Load users from JSON file"""
    try:
        if os.path.exists(USER_DB_FILE):
            with open(USER_DB_FILE, 'r') as f:
                return json.load(f)
        return {}
    except Exception:
        return {}

def save_users(data):
    """Save users to JSON file"""
    try:
        with open(USER_DB_FILE, 'w') as f:
            json.dump(data, f, indent=2)
        return True
    except Exception:
        return False

def hash_password(password):
    """Simple password hashing"""
    import hashlib
    return hashlib.sha256(password.encode()).hexdigest()

@app.route('/api/register', methods=['POST'])
def register():
    """API endpoint for user registration"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        email = data.get('email', '')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400
        
        users = load_users()
        
        if username in users:
            return jsonify({'status': 'error', 'message': 'Username already exists'}), 400
        
        users[username] = {
            'password': hash_password(password),
            'email': email,
            'created_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'profile': None,
            'meal_plan': None,
            'calories': None,
            'macros': None
        }
        
        if save_users(users):
            return jsonify({'status': 'success', 'message': 'Registration successful', 'username': username})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save user'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/login', methods=['POST'])
def login():
    """API endpoint for user login"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        username = data.get('username')
        password = data.get('password')
        
        if not username or not password:
            return jsonify({'status': 'error', 'message': 'Username and password are required'}), 400
        
        users = load_users()
        
        if username not in users or users[username]['password'] != hash_password(password):
            return jsonify({'status': 'error', 'message': 'Invalid username or password'}), 401
        
        user_data = users[username].copy()
        del user_data['password']
        
        return jsonify({'status': 'success', 'message': 'Login successful', 'user': user_data})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/profile', methods=['POST'])
def save_profile():
    """API endpoint to save user profile and generate meal plan"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        username = data.get('username')
        if not username:
            return jsonify({'status': 'error', 'message': 'Username is required'}), 400
        
        users = load_users()
        
        if username not in users:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        profile = {
            'name': data.get('name', username),
            'age': int(data.get('age', 25)),
            'gender': data.get('gender', 'M'),
            'weight': float(data.get('weight', 70)),
            'height': float(data.get('height', 170)),
            'activity_level': data.get('activity_level', '3'),
            'goal': data.get('goal', '2'),
            'diet_preference': data.get('diet_preference', '1'),
            'health_condition': data.get('health_condition', '')
        }
        
        food_db = FoodDatabase()
        calc_profile = UserProfile()
        calc_profile.name = profile['name']
        calc_profile.age = profile['age']
        calc_profile.gender = profile['gender']
        calc_profile.weight = profile['weight']
        calc_profile.height = profile['height']
        calc_profile.activity_level = profile['activity_level']
        calc_profile.goal = profile['goal']
        calc_profile.diet_preference = profile['diet_preference']
        
        calculator = CalorieCalculator()
        bmr = calculator.calculate_bmr(calc_profile.age, calc_profile.gender, calc_profile.weight, calc_profile.height)
        activity_multiplier = UserProfile.ACTIVITY_LEVELS[calc_profile.activity_level]['multiplier']
        tdee = calculator.calculate_tdee(bmr, activity_multiplier)
        goal_adjustment = UserProfile.GOALS[calc_profile.goal]['calorie_adjustment']
        daily_calories = calculator.calculate_daily_calories(tdee, goal_adjustment)
        
        health_condition = profile.get('health_condition', '')
        disease_info = None
        if health_condition and health_condition in DISEASE_CONFIG:
            disease_info = DISEASE_CONFIG[health_condition]
            disease_calorie_adjustment = disease_info.get('calorie_adjustment', 0)
            daily_calories = max(1200, daily_calories + disease_calorie_adjustment)
        
        macro_calc = MacroCalculator()
        macro_type = 'balanced'
        if disease_info:
            macro_type = disease_info.get('macro_type', 'balanced')
        
        macro_config = MACRO_CONFIGS.get(macro_type, MACRO_CONFIGS['balanced'])
        protein = int(daily_calories * macro_config['protein_ratio'] / 4)
        carbs = int(daily_calories * macro_config['carbs_ratio'] / 4)
        fats = int(daily_calories * macro_config['fats_ratio'] / 9)
        
        macros = {'protein': protein, 'carbs': carbs, 'fats': fats}
        
        meal_planner = MealPlanner(food_db, calc_profile.diet_preference)
        meal_plan = meal_planner.generate_weekly_meal_plan(daily_calories, macros)
        
        base_water = int(calc_profile.weight * 40)
        protein_extra = max(0, (macros['protein'] - 100) * 15)
        water_ml = base_water + protein_extra
        water_glasses = int(water_ml / 250)
        
        users[username]['profile'] = profile
        users[username]['meal_plan'] = meal_plan
        users[username]['calories'] = {'bmr': bmr, 'tdee': tdee, 'daily_target': daily_calories, 'water_ml': water_ml, 'water_glasses': water_glasses}
        users[username]['macros'] = macros
        users[username]['disease'] = None
        if disease_info:
            users[username]['disease'] = {'name': disease_info['name'], 'description': disease_info['description'], 'foods_to_avoid': disease_info['foods_to_avoid'], 'foods_to_include': disease_info['foods_to_include'], 'special_instructions': disease_info['special_instructions']}
        
        if save_users(users):
            return jsonify({'status': 'success', 'message': 'Profile saved successfully', 'calories': users[username]['calories'], 'macros': macros, 'meal_plan': meal_plan, 'water': {'ml': water_ml, 'glasses': water_glasses}})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save profile'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/profile/<username>', methods=['GET'])
def get_profile(username):
    """API endpoint to get user profile and meal plan"""
    try:
        users = load_users()
        
        if username not in users:
            return jsonify({'status': 'error', 'message': 'User not found'}), 404
        
        user_data = users[username].copy()
        del user_data['password']
        
        return jsonify({'status': 'success', 'user': user_data})
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/meal-status', methods=['POST'])
def update_meal_status():
    """API endpoint to update meal status (done/not done)"""
    try:
        data = request.get_json()
        if not data:
            return jsonify({'status': 'error', 'message': 'No data provided'}), 400
        
        meal_id = data.get('meal_id')
        status = data.get('status')
        
        if not meal_id or status not in ['done', 'not_done']:
            return jsonify({'status': 'error', 'message': 'Invalid meal_id or status'}), 400
        
        meal_data = load_meal_status()
        meal_data[meal_id] = {'status': status, 'updated_at': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
        
        if save_meal_status(meal_data):
            return jsonify({'status': 'success', 'meal_id': meal_id, 'status': status})
        else:
            return jsonify({'status': 'error', 'message': 'Failed to save status'}), 500
            
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/meal-status', methods=['GET'])
def get_meal_status():
    """API endpoint to get all meal statuses"""
    try:
        meal_data = load_meal_status()
        return jsonify({'status': 'success', 'data': meal_data})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/meal-status/today', methods=['GET'])
def get_today_meal_status():
    """API endpoint to get today's meal completion stats"""
    try:
        meal_data = load_meal_status()
        today = datetime.now().strftime('%Y-%m-%d')
        
        today_meals = {}
        for meal_id, info in meal_data.items():
            if info.get('updated_at', '').startswith(today):
                today_meals[meal_id] = info
        
        done_count = sum(1 for info in today_meals.values() if info.get('status') == 'done')
        total_count = len(today_meals)
        
        return jsonify({'status': 'success', 'data': today_meals, 'done_count': done_count, 'total_count': total_count})
    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500


if __name__ == '__main__':
    # Create templates directory if it doesn't exist
    if not os.path.exists('templates'):
        os.makedirs('templates')
    
    print("=" * 60)
    print("FOODIQ WEB APPLICATION")
    print("=" * 60)
    print("\nStarting server at http://127.0.0.1:5000")
    print("Press Ctrl+C to stop the server\n")
    
    app.run(debug=True, host='0.0.0.0', port=5000)
