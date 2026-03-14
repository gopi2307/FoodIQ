"""
Food IQ - Calorie Calculator and Customized Diet Planning Application
=====================================================================
A comprehensive application for calculating daily caloric needs,
macronutrient requirements, and generating personalized meal plans.
"""

import json
from datetime import datetime

# ===================== FOOD DATABASE =====================
class FoodDatabase:
    """Database containing Indian foods with nutritional information"""
    
    def __init__(self):
        self.foods = {
            # ===================== INDIAN PROTEINS =====================
            # Non-Veg Proteins
            "chicken breast": {"calories": 165, "protein": 31, "carbs": 0, "fats": 3.6, "fiber": 0, "iron": 1, "calcium": 15, "vitamin_a": 7, "vitamin_c": 0, "vitamin_d": 5, "sodium": 74, "potassium": 256, "zinc": 1, "serving": 100, "unit": "g"},
            "egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "fiber": 0, "iron": 1.8, "calcium": 50, "vitamin_a": 160, "vitamin_c": 0, "vitamin_d": 87, "sodium": 124, "potassium": 126, "zinc": 1.3, "serving": 100, "unit": "g"},
            "boiled egg": {"calories": 155, "protein": 13, "carbs": 1.1, "fats": 11, "fiber": 0, "iron": 1.8, "calcium": 50, "vitamin_a": 160, "vitamin_c": 0, "vitamin_d": 87, "sodium": 124, "potassium": 126, "zinc": 1.3, "serving": 100, "unit": "g"},
            "fish": {"calories": 136, "protein": 20, "carbs": 0, "fats": 6, "fiber": 0, "iron": 1.6, "calcium": 38, "vitamin_a": 50, "vitamin_c": 0, "vitamin_d": 152, "sodium": 50, "potassium": 300, "zinc": 0.6, "serving": 100, "unit": "g"},
            "paneer": {"calories": 265, "protein": 18, "carbs": 1.2, "fats": 20, "fiber": 0.5, "iron": 1.5, "calcium": 500, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 20, "potassium": 80, "zinc": 2, "serving": 100, "unit": "g"},
            
            # Veg Proteins
            "dal (lentils)": {"calories": 116, "protein": 9, "carbs": 20, "fats": 0.4, "fiber": 8, "iron": 1.9, "calcium": 19, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 2, "potassium": 190, "zinc": 1, "serving": 100, "unit": "g"},
            "moong dal": {"calories": 105, "protein": 7, "carbs": 19, "fats": 0.4, "fiber": 7, "iron": 1.4, "calcium": 22, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 1, "potassium": 180, "zinc": 0.8, "serving": 100, "unit": "g"},
            "toor dal": {"calories": 116, "protein": 8, "carbs": 20, "fats": 0.5, "fiber": 7, "iron": 1.5, "calcium": 28, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 2, "potassium": 200, "zinc": 1, "serving": 100, "unit": "g"},
            "urad dal": {"calories": 105, "protein": 9, "carbs": 18, "fats": 0.4, "fiber": 6, "iron": 1.7, "calcium": 25, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 2, "potassium": 170, "zinc": 1.1, "serving": 100, "unit": "g"},
            "chana dal": {"calories": 164, "protein": 9, "carbs": 27, "fats": 3, "fiber": 9, "iron": 2.7, "calcium": 30, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 3, "potassium": 230, "zinc": 1.5, "serving": 100, "unit": "g"},
            "soya chunks": {"calories": 345, "protein": 52, "carbs": 34, "fats": 1, "fiber": 12, "iron": 8, "calcium": 350, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 15, "potassium": 350, "zinc": 4, "serving": 100, "unit": "g"},
            "rajma": {"calories": 119, "protein": 8, "carbs": 21, "fats": 0.5, "fiber": 7, "iron": 2.1, "calcium": 21, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 1, "potassium": 250, "zinc": 1, "serving": 100, "unit": "g"},
            
            # ===================== INDIAN CARBOHYDRATES =====================
            "white rice (cooked)": {"calories": 130, "protein": 2.7, "carbs": 28, "fats": 0.3, "fiber": 0.4, "iron": 0.2, "calcium": 5, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 1, "potassium": 35, "zinc": 0.5, "serving": 100, "unit": "g"},
            "brown rice": {"calories": 112, "protein": 2.6, "carbs": 24, "fats": 0.9, "fiber": 1.8, "iron": 0.4, "calcium": 10, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 1, "potassium": 79, "zinc": 0.6, "serving": 100, "unit": "g"},
            "rolled oats": {"calories": 379, "protein": 13, "carbs": 68, "fats": 7, "fiber": 10, "iron": 4.3, "calcium": 52, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 6, "potassium": 362, "zinc": 3.6, "serving": 100, "unit": "g"},
            "chapati": {"calories": 264, "protein": 9, "carbs": 52, "fats": 3, "fiber": 3, "iron": 1.9, "calcium": 20, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 38, "potassium": 150, "zinc": 1.5, "serving": 100, "unit": "g"},
            "roti": {"calories": 264, "protein": 9, "carbs": 52, "fats": 3, "fiber": 3, "iron": 1.9, "calcium": 20, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 38, "potassium": 150, "zinc": 1.5, "serving": 100, "unit": "g"},
            "paratha": {"calories": 306, "protein": 7, "carbs": 43, "fats": 11, "fiber": 2, "iron": 1.5, "calcium": 25, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 45, "potassium": 120, "zinc": 1, "serving": 100, "unit": "g"},
            "poha": {"calories": 130, "protein": 2.2, "carbs": 28, "fats": 0.4, "fiber": 1, "iron": 0.6, "calcium": 10, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 9, "potassium": 50, "zinc": 0.4, "serving": 100, "unit": "g"},
            "idli": {"calories": 104, "protein": 3, "carbs": 22, "fats": 0.2, "fiber": 1, "iron": 0.4, "calcium": 10, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 4, "potassium": 35, "zinc": 0.3, "serving": 100, "unit": "g"},
            "dosa": {"calories": 133, "protein": 3, "carbs": 26, "fats": 1.5, "fiber": 1, "iron": 0.5, "calcium": 15, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 7, "potassium": 45, "zinc": 0.4, "serving": 100, "unit": "g"},
            
            # ===================== INDIAN VEGETABLES =====================
            "onion": {"calories": 40, "protein": 1.1, "carbs": 9, "fats": 0.1, "fiber": 1.4, "iron": 0.2, "calcium": 10, "vitamin_a": 0, "vitamin_c": 2.4, "vitamin_d": 0, "sodium": 1, "potassium": 120, "zinc": 0.2, "serving": 100, "unit": "g"},
            "tomato": {"calories": 18, "protein": 0.9, "carbs": 3.9, "fats": 0.2, "fiber": 1.2, "iron": 0.3, "calcium": 5, "vitamin_a": 42, "vitamin_c": 14, "vitamin_d": 0, "sodium": 3, "potassium": 180, "zinc": 0.2, "serving": 100, "unit": "g"},
            "potato": {"calories": 77, "protein": 2, "carbs": 17, "fats": 0.1, "fiber": 2.2, "iron": 0.8, "calcium": 12, "vitamin_a": 0, "vitamin_c": 20, "vitamin_d": 0, "sodium": 6, "potassium": 421, "zinc": 0.3, "serving": 100, "unit": "g"},
            "carrot": {"calories": 41, "protein": 0.9, "carbs": 10, "fats": 0.2, "fiber": 2.8, "iron": 0.3, "calcium": 33, "vitamin_a": 835, "vitamin_c": 6, "vitamin_d": 0, "sodium": 69, "potassium": 320, "zinc": 0.2, "serving": 100, "unit": "g"},
            "cabbage": {"calories": 25, "protein": 1.3, "carbs": 6, "fats": 0.1, "fiber": 2.5, "iron": 0.5, "calcium": 40, "vitamin_a": 3, "vitamin_c": 37, "vitamin_d": 0, "sodium": 18, "potassium": 170, "zinc": 0.2, "serving": 100, "unit": "g"},
            "cauliflower": {"calories": 25, "protein": 2, "carbs": 5, "fats": 0.3, "fiber": 2, "iron": 0.4, "calcium": 22, "vitamin_a": 0, "vitamin_c": 48, "vitamin_d": 0, "sodium": 30, "potassium": 299, "zinc": 0.3, "serving": 100, "unit": "g"},
            "spinach": {"calories": 23, "protein": 2.9, "carbs": 3.6, "fats": 0.4, "fiber": 2.2, "iron": 2.7, "calcium": 99, "vitamin_a": 469, "vitamin_c": 28, "vitamin_d": 0, "sodium": 79, "potassium": 558, "zinc": 0.5, "serving": 100, "unit": "g"},
            "ladies finger": {"calories": 33, "protein": 1.9, "carbs": 7, "fats": 0.2, "fiber": 3.2, "iron": 0.6, "calcium": 50, "vitamin_a": 25, "vitamin_c": 16, "vitamin_d": 0, "sodium": 7, "potassium": 140, "zinc": 0.4, "serving": 100, "unit": "g"},
            "brinjal": {"calories": 25, "protein": 1, "carbs": 6, "fats": 0.2, "fiber": 3, "iron": 0.2, "calcium": 10, "vitamin_a": 1, "vitamin_c": 2, "vitamin_d": 0, "sodium": 2, "potassium": 120, "zinc": 0.2, "serving": 100, "unit": "g"},
            "lauki": {"calories": 15, "protein": 0.6, "carbs": 3.4, "fats": 0.1, "fiber": 0.5, "iron": 0.2, "calcium": 20, "vitamin_a": 0, "vitamin_c": 4, "vitamin_d": 0, "sodium": 2, "potassium": 80, "zinc": 0.2, "serving": 100, "unit": "g"},
            "tinda": {"calories": 12, "protein": 0.5, "carbs": 2.5, "fats": 0.1, "fiber": 0.6, "iron": 0.2, "calcium": 15, "vitamin_a": 0, "vitamin_c": 1, "vitamin_d": 0, "sodium": 2, "potassium": 50, "zinc": 0.2, "serving": 100, "unit": "g"},
            "capsicum": {"calories": 20, "protein": 0.9, "carbs": 4.6, "fats": 0.2, "fiber": 1.7, "iron": 0.3, "calcium": 7, "vitamin_a": 157, "vitamin_c": 128, "vitamin_d": 0, "sodium": 3, "potassium": 175, "zinc": 0.2, "serving": 100, "unit": "g"},
            "beans": {"calories": 31, "protein": 1.8, "carbs": 7, "fats": 0.1, "fiber": 3.4, "iron": 1, "calcium": 35, "vitamin_a": 14, "vitamin_c": 12, "vitamin_d": 0, "sodium": 6, "potassium": 200, "zinc": 0.2, "serving": 100, "unit": "g"},
            "peas": {"calories": 81, "protein": 5.4, "carbs": 14, "fats": 0.4, "fiber": 5.7, "iron": 1.5, "calcium": 25, "vitamin_a": 38, "vitamin_c": 40, "vitamin_d": 0, "sodium": 5, "potassium": 244, "zinc": 1.2, "serving": 100, "unit": "g"},
            "corn": {"calories": 86, "protein": 3.3, "carbs": 19, "fats": 1.4, "fiber": 2.7, "iron": 0.5, "calcium": 2, "vitamin_a": 9, "vitamin_c": 6, "vitamin_d": 0, "sodium": 15, "potassium": 270, "zinc": 0.5, "serving": 100, "unit": "g"},
            "mixed vegetables": {"calories": 35, "protein": 2, "carbs": 7, "fats": 0.3, "fiber": 2.5, "iron": 0.6, "calcium": 25, "vitamin_a": 100, "vitamin_c": 15, "vitamin_d": 0, "sodium": 40, "potassium": 150, "zinc": 0.4, "serving": 100, "unit": "g"},
            
            # ===================== INDIAN DAIRY =====================
            "milk": {"calories": 61, "protein": 3.2, "carbs": 4.8, "fats": 3.3, "fiber": 0, "iron": 0.05, "calcium": 125, "vitamin_a": 46, "vitamin_c": 0, "vitamin_d": 40, "sodium": 44, "potassium": 150, "zinc": 0.4, "serving": 100, "unit": "ml"},
            "curd": {"calories": 98, "protein": 5, "carbs": 4, "fats": 7, "fiber": 0, "iron": 0.1, "calcium": 110, "vitamin_a": 25, "vitamin_c": 0, "vitamin_d": 5, "sodium": 36, "potassium": 104, "zinc": 0.6, "serving": 100, "unit": "g"},
            "butter": {"calories": 717, "protein": 0.9, "carbs": 0.1, "fats": 81, "fiber": 0, "iron": 0.02, "calcium": 24, "vitamin_a": 684, "vitamin_c": 0, "vitamin_d": 60, "sodium": 576, "potassium": 24, "zinc": 0.1, "serving": 100, "unit": "g"},
            "ghee": {"calories": 900, "protein": 0, "carbs": 0, "fats": 100, "fiber": 0, "iron": 0, "calcium": 0, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 0, "potassium": 0, "zinc": 0, "serving": 100, "unit": "ml"},
            "cream": {"calories": 340, "protein": 2, "carbs": 3, "fats": 36, "fiber": 0, "iron": 0.1, "calcium": 80, "vitamin_a": 150, "vitamin_c": 0, "vitamin_d": 20, "sodium": 35, "potassium": 75, "zinc": 0.3, "serving": 100, "unit": "g"},
            
            # ===================== INDIAN SNACKS =====================
            "banana": {"calories": 89, "protein": 1.1, "carbs": 23, "fats": 0.3, "fiber": 2.6, "iron": 0.3, "calcium": 5, "vitamin_a": 3, "vitamin_c": 9, "vitamin_d": 0, "sodium": 1, "potassium": 358, "zinc": 0.2, "serving": 100, "unit": "g"},
            "apple": {"calories": 52, "protein": 0.3, "carbs": 14, "fats": 0.2, "fiber": 2.4, "iron": 0.1, "calcium": 6, "vitamin_a": 3, "vitamin_c": 5, "vitamin_d": 0, "sodium": 1, "potassium": 107, "zinc": 0.04, "serving": 100, "unit": "g"},
            "peanut": {"calories": 567, "protein": 26, "carbs": 16, "fats": 49, "fiber": 9, "iron": 4.6, "calcium": 92, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 18, "potassium": 705, "zinc": 3.3, "serving": 100, "unit": "g"},
            "roasted chana": {"calories": 162, "protein": 7, "carbs": 14, "fats": 5, "fiber": 5, "iron": 2.5, "calcium": 45, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 20, "potassium": 175, "zinc": 1.5, "serving": 100, "unit": "g"},
            "moong dal namkeen": {"calories": 148, "protein": 5, "carbs": 20, "fats": 5, "fiber": 4, "iron": 1.5, "calcium": 20, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 150, "potassium": 100, "zinc": 0.8, "serving": 100, "unit": "g"},
            "biscuit": {"calories": 443, "protein": 7, "carbs": 70, "fats": 15, "fiber": 2, "iron": 2.5, "calcium": 30, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 200, "potassium": 80, "zinc": 0.8, "serving": 100, "unit": "g"},
            "murukku": {"calories": 433, "protein": 8, "carbs": 68, "fats": 14, "fiber": 3, "iron": 3, "calcium": 40, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 180, "potassium": 100, "zinc": 1, "serving": 100, "unit": "g"},
            "namkeen": {"calories": 536, "protein": 10, "carbs": 56, "fats": 30, "fiber": 2, "iron": 3, "calcium": 25, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 250, "potassium": 85, "zinc": 1, "serving": 100, "unit": "g"},
        }
    
    def search(self, query):
        """Search for foods matching the query"""
        query = query.lower()
        results = {}
        for food, info in self.foods.items():
            if query in food:
                results[food] = info
        return results
    
    def get_food(self, name):
        """Get nutritional info for a specific food"""
        name = name.lower()
        return self.foods.get(name)


# ===================== USER PROFILE =====================
class UserProfile:
    """User profile for diet planning"""
    
    ACTIVITY_LEVELS = {
        "1": {"name": "Sedentary", "multiplier": 1.2, 
              "description": "Little or no exercise, desk job"},
        "2": {"name": "Lightly Active", "multiplier": 1.375, 
              "description": "Light exercise 1-3 days/week"},
        "3": {"name": "Moderately Active", "multiplier": 1.55, 
              "description": "Moderate exercise 3-5 days/week"},
        "4": {"name": "Very Active", "multiplier": 1.725, 
              "description": "Hard exercise 6-7 days/week"},
        "5": {"name": "Extra Active", "multiplier": 1.9, 
              "description": "Very hard exercise, physical job"},
    }
    
    GOALS = {
        "1": {"name": "Lose Weight", "calorie_adjustment": -500, 
              "description": "Lose about 0.5 kg per week"},
        "2": {"name": "Maintain Weight", "calorie_adjustment": 0, 
              "description": "Maintain current weight"},
        "3": {"name": "Gain Weight", "calorie_adjustment": 500, 
              "description": "Gain about 0.5 kg per week"},
    }
    
    DIET_PREFERENCES = {
        "1": {"name": "Vegetarian", "description": "Indian veg meals - dal, paneer, rice, chapati, vegetables"},
        "2": {"name": "Non-Vegetarian", "description": "Indian meals with egg, chicken, fish"},
    }
    
    def __init__(self):
        self.name = ""
        self.age = 0
        self.gender = ""
        self.weight = 0  # kg
        self.height = 0  # cm
        self.activity_level = ""
        self.goal = ""
        self.diet_preference = "3"  # Default to Non-Veg
    
    def input_profile(self):
        """Collect user profile information"""
        print("\n" + "="*60)
        print("🍽️  WELCOME TO FOOD IQ - Your Personal Diet Planner  🍽️")
        print("="*60)
        
        self.name = input("\n📛 Enter your name: ").strip()
        if not self.name:
            self.name = "User"
        
        # Age input with validation
        while True:
            try:
                self.age = int(input("🎂 Enter your age (years): "))
                if 15 <= self.age <= 100:
                    break
                print("⚠️  Please enter a valid age between 15 and 100")
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        # Gender input
        while True:
            self.gender = input("🚻 Enter gender (M/F): ").strip().upper()
            if self.gender in ['M', 'F']:
                break
            print("⚠️  Please enter M or F")
        
        # Weight input with validation
        while True:
            try:
                self.weight = float(input("⚖️  Enter your weight (kg): "))
                if 30 <= self.weight <= 300:
                    break
                print("⚠️  Please enter a valid weight between 30-300 kg")
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        # Height input with validation
        while True:
            try:
                self.height = float(input("📏 Enter your height (cm): "))
                if 100 <= self.height <= 250:
                    break
                print("⚠️  Please enter a valid height between 100-250 cm")
            except ValueError:
                print("⚠️  Please enter a valid number")
        
        # Activity level selection
        print("\n🏃 SELECT YOUR ACTIVITY LEVEL:")
        print("-" * 40)
        for key, level in self.ACTIVITY_LEVELS.items():
            print(f"  {key}. {level['name']}")
            print(f"     → {level['description']}")
        
        while True:
            self.activity_level = input("\n👉 Enter your choice (1-5): ").strip()
            if self.activity_level in self.ACTIVITY_LEVELS:
                break
            print("⚠️  Please enter a number between 1 and 5")
        
        # Goal selection
        print("\n🎯 SELECT YOUR FITNESS GOAL:")
        print("-" * 40)
        for key, goal in self.GOALS.items():
            print(f"  {key}. {goal['name']}")
            print(f"     → {goal['description']}")
        
        while True:
            self.goal = input("\n👉 Enter your choice (1-3): ").strip()
            if self.goal in self.GOALS:
                break
            print("⚠️  Please enter a number between 1 and 3")
        
        return self


# ===================== CALORIE CALCULATOR =====================
class CalorieCalculator:
    """Calculate BMR, TDEE, and daily calorie needs"""
    
    @staticmethod
    def calculate_bmr(age, gender, weight, height):
        """
        Calculate Basal Metabolic Rate using Mifflin-St Jeor Equation
        This is considered the most accurate formula for most people
        """
        if gender == 'M':
            bmr = (10 * weight) + (6.25 * height) - (5 * age) + 5
        else:
            bmr = (10 * weight) + (6.25 * height) - (5 * age) - 161
        return round(bmr)
    
    @staticmethod
    def calculate_tdee(bmr, activity_multiplier):
        """Calculate Total Daily Energy Expenditure"""
        return round(bmr * activity_multiplier)
    
    @staticmethod
    def calculate_daily_calories(tdee, goal_adjustment):
        """Calculate target daily calories based on goal"""
        return tdee + goal_adjustment


# ===================== MACRO NUTRIENT CALCULATOR =====================
class MacroCalculator:
    """Calculate macronutrient requirements"""
    
    # Standard macro ratios for different goals
    MACRO_RATIOS = {
        "1": {"name": "Balanced", "protein": 0.30, "carbs": 0.40, "fats": 0.30},
        "2": {"name": "Low Carb", "protein": 0.40, "carbs": 0.25, "fats": 0.35},
        "3": {"name": "High Protein", "protein": 0.40, "carbs": 0.35, "fats": 0.25},
        "4": {"name": "High Carb", "protein": 0.20, "carbs": 0.55, "fats": 0.25},
    }
    
    # Calories per gram
    CALORIES_PER_GRAM = {
        "protein": 4,
        "carbs": 4,
        "fats": 9,
    }
    
    @staticmethod
    def select_macro_plan():
        """Let user select macro ratio plan"""
        print("\n🥗 SELECT MACRO NUTRIENT RATIO:")
        print("-" * 40)
        for key, ratio in MacroCalculator.MACRO_RATIOS.items():
            print(f"  {key}. {ratio['name']}")
            print(f"     → Protein: {int(ratio['protein']*100)}% | Carbs: {int(ratio['carbs']*100)}% | Fats: {int(ratio['fats']*100)}%")
        
        while True:
            choice = input("\n👉 Enter your choice (1-4): ").strip()
            if choice in MacroCalculator.MACRO_RATIOS:
                return choice
            print("⚠️  Please enter a number between 1 and 4")
    
    @staticmethod
    def calculate_macros(daily_calories, ratio):
        """Calculate daily macro requirements in grams"""
        r = MacroCalculator.MACRO_RATIOS[ratio]
        
        protein_grams = (daily_calories * r['protein']) / MacroCalculator.CALORIES_PER_GRAM['protein']
        carbs_grams = (daily_calories * r['carbs']) / MacroCalculator.CALORIES_PER_GRAM['carbs']
        fats_grams = (daily_calories * r['fats']) / MacroCalculator.CALORIES_PER_GRAM['fats']
        
        return {
            "protein": round(protein_grams),
            "carbs": round(carbs_grams),
            "fats": round(fats_grams),
        }


# ===================== MEAL PLANNER =====================
class MealPlanner:
    """Generate personalized Indian meal plans"""
    
    MEAL_OPTIONS = {
        "breakfast": [
            # Vegetarian Indian Breakfast - More variety
            {"name": "Oats with Milk and Banana", "foods": ["rolled oats", "milk", "banana"]},
            {"name": "Masala Oats with Vegetables", "foods": ["rolled oats", "onion", "tomato", "carrot"]},
            {"name": "Poha with Peanuts", "foods": ["poha", "peanut", "onion", "tomato"]},
            {"name": "Poha with Vegetables", "foods": ["poha", "mixed vegetables"]},
            {"name": "Idli with Sambar", "foods": ["idli", "dal (lentils)"]},
            {"name": "Idli with Chutney", "foods": ["idli"]},
            {"name": "Dosa with Sambar", "foods": ["dosa", "dal (lentils)"]},
            {"name": "Dosa with Chutney", "foods": ["dosa"]},
            {"name": "Chapati with Dal", "foods": ["chapati", "dal (lentils)"]},
            {"name": "Chapati with Chana Dal", "foods": ["chapati", "chana dal"]},
            {"name": "Chapati with Paneer", "foods": ["chapati", "paneer"]},
            {"name": "Chapati with Mix Veg", "foods": ["chapati", "mixed vegetables"]},
            {"name": "Paratha with Mix Veg", "foods": ["paratha", "mixed vegetables"]},
            {"name": "Paratha with Paneer", "foods": ["paratha", "paneer"]},
            {"name": "Banana Smoothie", "foods": ["banana", "milk"]},
            {"name": "Milk with Oats", "foods": ["rolled oats", "milk"]},
            {"name": "Boiled Egg with Toast", "foods": ["boiled egg", "chapati"]},
            {"name": "Egg Omelette", "foods": ["egg"]},
            {"name": "Egg with Chapati", "foods": ["egg", "chapati"]},
            {"name": "Vegetable Poha", "foods": ["poha", "mixed vegetables"]},
            {"name": "Fruit Bowl", "foods": ["banana", "apple"]},
            {"name": "Oats Porridge", "foods": ["rolled oats", "milk"]},
            {"name": "Besan Chilla", "foods": ["moong dal"]},
            {"name": "Moong Dal Cheela", "foods": ["moong dal"]},
            {"name": "Vegetable Upma", "foods": ["poha", "mixed vegetables"]},
            {"name": "Poha with Curd", "foods": ["poha", "curd"]},
        ],
        "lunch": [
            # Vegetarian Indian Lunch - More variety
            {"name": "Rice with Dal", "foods": ["white rice (cooked)", "dal (lentils)"]},
            {"name": "Rice with Moong Dal", "foods": ["white rice (cooked)", "moong dal"]},
            {"name": "Rice with Toor Dal", "foods": ["white rice (cooked)", "toor dal"]},
            {"name": "Rice with Urad Dal", "foods": ["white rice (cooked)", "urad dal"]},
            {"name": "Rice with Rajma", "foods": ["white rice (cooked)", "rajma"]},
            {"name": "Rice with Chana Dal", "foods": ["white rice (cooked)", "chana dal"]},
            {"name": "Chapati with Dal", "foods": ["chapati", "dal (lentils)"]},
            {"name": "Chapati with Moong Dal", "foods": ["chapati", "moong dal"]},
            {"name": "Chapati with Chana Dal", "foods": ["chapati", "chana dal"]},
            {"name": "Vegetable Pulao", "foods": ["white rice (cooked)", "mixed vegetables"]},
            {"name": "Dal Khichdi", "foods": ["white rice (cooked)", "moong dal"]},
            {"name": "Rice with Sambar", "foods": ["white rice (cooked)", "dal (lentils)", "mixed vegetables"]},
            {"name": "Chapati with Mix Veg", "foods": ["chapati", "mixed vegetables"]},
            {"name": "Chapati with Paneer", "foods": ["chapati", "paneer"]},
            {"name": "Chapati with Gobi", "foods": ["chapati", "cauliflower"]},
            {"name": "Chapati with Aloo", "foods": ["chapati", "potato"]},
            {"name": "Rice with Soya Chunks", "foods": ["white rice (cooked)", "soya chunks"]},
        ],
        "dinner": [
            # Vegetarian Indian Dinner - More variety
            {"name": "Chapati with Mix Veg", "foods": ["chapati", "mixed vegetables"]},
            {"name": "Chapati with Paneer", "foods": ["chapati", "paneer"]},
            {"name": "Rice with Palak", "foods": ["white rice (cooked)", "spinach"]},
            {"name": "Rice with Aloo Gobi", "foods": ["white rice (cooked)", "potato", "cauliflower"]},
            {"name": "Rice with Ladies Finger", "foods": ["white rice (cooked)", "ladies finger"]},
            {"name": "Rice with Brinjal", "foods": ["white rice (cooked)", "brinjal"]},
            {"name": "Rice with Lauki", "foods": ["white rice (cooked)", "lauki"]},
            {"name": "Rice with Tinda", "foods": ["white rice (cooked)", "tinda"]},
            {"name": "Rice with Mix Vegetables", "foods": ["white rice (cooked)", "mixed vegetables"]},
            {"name": "Rice with Beans", "foods": ["white rice (cooked)", "beans"]},
            {"name": "Rice with Peas", "foods": ["white rice (cooked)", "peas"]},
            {"name": "Khichdi", "foods": ["white rice (cooked)", "moong dal"]},
            {"name": "Roti with Sabji", "foods": ["chapati", "mixed vegetables"]},
            {"name": "Chapati with Palak Paneer", "foods": ["chapati", "spinach", "paneer"]},
            {"name": "Chapati with Bhindi", "foods": ["chapati", "ladies finger"]},
        ],
        "snacks": [
            # Healthy Snacks - Maximum variety with salads
            {"name": "Roasted Chana", "foods": ["roasted chana"]},
            {"name": "Peanuts", "foods": ["peanut"]},
            {"name": "Fresh Banana", "foods": ["banana"]},
            {"name": "Fresh Apple", "foods": ["apple"]},
            {"name": "Boiled Egg", "foods": ["boiled egg"]},
            {"name": "Glass of Milk", "foods": ["milk"]},
            {"name": "Bowl of Curd", "foods": ["curd"]},
            {"name": "Chana with Milk", "foods": ["roasted chana", "milk"]},
            {"name": "Banana Milk Shake", "foods": ["banana", "milk"]},
            {"name": "Peanut with Fruit", "foods": ["peanut", "banana"]},
            {"name": "Moong Dal Snacks", "foods": ["moong dal namkeen"]},
            {"name": "Fruit Salad", "foods": ["banana", "apple"]},
            # Salads - more variety
            {"name": "Green Salad", "foods": ["tomato", "onion", "cucumber", "carrot"]},
            {"name": "Cucumber Salad", "foods": ["cucumber", "tomato", "onion"]},
            {"name": "Carrot Salad", "foods": ["carrot", "tomato"]},
            {"name": "Sprouts Salad", "foods": ["moong dal", "onion", "tomato"]},
            {"name": "Corn Salad", "foods": ["corn", "tomato", "onion"]},
            {"name": "Bean Salad", "foods": ["beans", "tomato", "onion"]},
            {"name": "Mixed Vegetable Salad", "foods": ["carrot", "cabbage", "tomato", "onion"]},
            {"name": "Kachumber Salad", "foods": ["tomato", "onion", "cucumber"]},
            {"name": "Coleslaw Salad", "foods": ["cabbage", "carrot"]},
            # Drinks
            {"name": "Buttermilk", "foods": ["curd", "water"]},
            {"name": "Lassi (Sweet)", "foods": ["curd", "water"]},
            {"name": "Lassi (Salt)", "foods": ["curd", "water"]},
            {"name": "Chaas", "foods": ["curd", "water"]},
            # Nuts & Seeds
            {"name": "Nuts Mix", "foods": ["peanut", "roasted chana", "almonds"]},
            {"name": "Trail Mix", "foods": ["peanut", "roasted chana"]},
            {"name": "Almonds", "foods": ["almonds"]},
            {"name": "Walnuts", "foods": ["peanut"]},
            # Fruit & Dairy
            {"name": "Curd with Fruits", "foods": ["curd", "banana"]},
            {"name": "Smoothie Bowl", "foods": ["banana", "milk"]},
            {"name": "Fruit and Nuts", "foods": ["banana", "peanut"]},
            {"name": "Apple with Peanut Butter", "foods": ["apple", "peanut"]},
            {"name": "Banana with Milk", "foods": ["banana", "milk"]},
            # Light options
            {"name": "Coconut Water", "foods": ["coconut"]},
            {"name": "Lemon Water", "foods": ["lemon", "water"]},
            {"name": "Green Tea", "foods": ["tea"]},
        ],
        
        # New brunch options - between breakfast and lunch
        "brunch": [
            {"name": "Fruit Bowl", "foods": ["banana", "apple"]},
            {"name": "Green Salad", "foods": ["tomato", "onion", "cucumber", "carrot"]},
            {"name": "Cucumber Salad", "foods": ["cucumber", "tomato"]},
            {"name": "Sprouts Salad", "foods": ["moong dal", "onion", "tomato"]},
            {"name": "Carrot Salad", "foods": ["carrot"]},
            {"name": "Corn Salad", "foods": ["corn", "tomato"]},
            {"name": "Glass of Milk", "foods": ["milk"]},
            {"name": "Bowl of Curd", "foods": ["curd"]},
            {"name": "Buttermilk", "foods": ["curd", "water"]},
            {"name": "Lassi", "foods": ["curd", "water"]},
            {"name": "Roasted Chana", "foods": ["roasted chana"]},
            {"name": "Peanuts", "foods": ["peanut"]},
            {"name": "Nuts Mix", "foods": ["peanut", "roasted chana"]},
            {"name": "Banana Milk Shake", "foods": ["banana", "milk"]},
            {"name": "Fresh Banana", "foods": ["banana"]},
            {"name": "Fresh Apple", "foods": ["apple"]},
            {"name": "Oats with Milk", "foods": ["rolled oats", "milk"]},
            {"name": "Vegetable Poha", "foods": ["poha", "mixed vegetables"]},
            {"name": "Moong Dal Snacks", "foods": ["moong dal namkeen"]},
            {"name": "Trail Mix", "foods": ["peanut", "roasted chana"]},
        ],
    }
    
    # Filter meals by diet type - includes brunch
    DIET_MEALS = {
        "1": [  # Vegetarian - More variety
            "Oats with Milk and Banana", "Masala Oats with Vegetables", "Poha with Peanuts", "Poha with Vegetables",
            "Idli with Sambar", "Idli with Chutney", "Dosa with Sambar", "Dosa with Chutney",
            "Chapati with Dal", "Chapati with Chana Dal", "Chapati with Paneer", "Chapati with Mix Veg",
            "Paratha with Mix Veg", "Paratha with Paneer",
            "Banana Smoothie", "Milk with Oats", "Vegetable Poha", "Fruit Bowl", "Oats Porridge",
            "Besan Chilla", "Moong Dal Cheela", "Vegetable Upma", "Poha with Curd",
            "Rice with Dal", "Rice with Moong Dal", "Rice with Toor Dal", "Rice with Urad Dal",
            "Rice with Rajma", "Rice with Chana Dal", "Chapati with Dal", "Chapati with Moong Dal",
            "Vegetable Pulao", "Dal Khichdi", "Rice with Sambar", "Chapati with Mix Veg",
            "Chapati with Paneer", "Chapati with Gobi", "Chapati with Aloo", "Rice with Soya Chunks",
            "Rice with Palak", "Rice with Aloo Gobi", "Rice with Ladies Finger", "Rice with Brinjal",
            "Rice with Lauki", "Rice with Tinda", "Rice with Mix Vegetables", "Rice with Beans",
            "Rice with Peas", "Khichdi", "Roti with Sabji", "Chapati with Palak Paneer", "Chapati with Bhindi",
            # Snacks
            "Roasted Chana", "Peanuts", "Fresh Banana", "Fresh Apple", "Boiled Egg",
            "Glass of Milk", "Bowl of Curd", "Chana with Milk", "Banana Milk Shake",
            "Peanut with Fruit", "Moong Dal Snacks", "Fruit Salad", "Green Salad",
            "Cucumber Salad", "Carrot Salad", "Sprouts Salad", "Buttermilk", "Lassi",
            "Nuts Mix", "Fruit and Nuts", "Vegetable Stick Salad", "Corn Salad",
            "Bean Salad", "Curd with Fruits", "Smoothie Bowl", "Trail Mix",
            # More salads
            "Mixed Vegetable Salad", "Kachumber Salad", "Coleslaw Salad",
            # Brunch items
            "Oats with Milk", "Lassi (Sweet)", "Lassi (Salt)", "Chaas",
            "Almonds", "Apple with Peanut Butter", "Banana with Milk", "Coconut Water", 
            "Lemon Water", "Green Tea",
        ],
        "2": [  # Non-Vegetarian - More variety
            "Oats with Milk and Banana", "Masala Oats with Vegetables", "Poha with Peanuts", "Poha with Vegetables",
            "Idli with Sambar", "Idli with Chutney", "Dosa with Sambar", "Dosa with Chutney",
            "Chapati with Dal", "Chapati with Chana Dal", "Chapati with Paneer", "Chapati with Mix Veg",
            "Paratha with Mix Veg", "Paratha with Paneer",
            "Banana Smoothie", "Milk with Oats", "Boiled Egg with Toast", "Egg Omelette", "Egg with Chapati",
            "Vegetable Poha", "Fruit Bowl", "Oats Porridge", "Besan Chilla",
            "Rice with Dal", "Rice with Moong Dal", "Rice with Toor Dal", "Rice with Urad Dal",
            "Rice with Rajma", "Rice with Chana Dal", "Chapati with Dal", "Chapati with Moong Dal",
            "Vegetable Pulao", "Dal Khichdi", "Rice with Sambar", "Chapati with Mix Veg",
            "Chapati with Paneer", "Chapati with Gobi", "Chapati with Aloo", "Rice with Soya Chunks",
            "Rice with Palak", "Rice with Aloo Gobi", "Rice with Ladies Finger", "Rice with Brinjal",
            "Rice with Lauki", "Rice with Tinda", "Rice with Mix Vegetables", "Rice with Beans",
            "Rice with Peas", "Khichdi", "Roti with Sabji", "Chapati with Palak Paneer", "Chapati with Bhindi",
            "Chicken Curry with Rice", "Fish Curry with Rice", "Egg Curry with Rice",
            # Snacks
            "Roasted Chana", "Peanuts", "Fresh Banana", "Fresh Apple", "Boiled Egg",
            "Glass of Milk", "Bowl of Curd", "Chana with Milk", "Banana Milk Shake",
            "Peanut with Fruit", "Moong Dal Snacks", "Fruit Salad", "Green Salad",
            "Cucumber Salad", "Carrot Salad", "Sprouts Salad", "Buttermilk", "Lassi",
            "Nuts Mix", "Fruit and Nuts", "Vegetable Stick Salad", "Corn Salad",
            "Bean Salad", "Curd with Fruits", "Smoothie Bowl", "Trail Mix",
            # More salads
            "Mixed Vegetable Salad", "Kachumber Salad", "Coleslaw Salad",
            # Brunch items
            "Oats with Milk", "Lassi (Sweet)", "Lassi (Salt)", "Chaas",
            "Almonds", "Apple with Peanut Butter", "Banana with Milk", "Coconut Water", 
            "Lemon Water", "Green Tea",
        ],
    }
    
    # Non-Veg specific meals
    NON_VEG_MEALS = {
        "breakfast": [
            {"name": "Boiled Egg with Chapati", "foods": ["boiled egg", "chapati", "onion"]},
            {"name": "Egg Omelette with Chapati", "foods": ["egg", "chapati", "onion", "tomato"]},
            {"name": "Egg Curry with Bread", "foods": ["egg", "chapati", "onion", "tomato"]},
            {"name": "Chicken Sandwich", "foods": ["chicken breast", "chapati", "onion", "tomato"]},
            {"name": "Fish Fry with Rice", "foods": ["fish", "white rice (cooked)", "onion", "tomato"]},
        ],
        "brunch": [
            {"name": "Boiled Egg", "foods": ["boiled egg"]},
            {"name": "Egg with Toast", "foods": ["boiled egg", "chapati"]},
            {"name": "Chicken Salad", "foods": ["chicken breast", "tomato", "onion", "cucumber"]},
            {"name": "Fish Salad", "foods": ["fish", "tomato", "onion", "cucumber"]},
            {"name": "Egg Salad", "foods": ["boiled egg", "tomato", "onion", "cucumber"]},
        ],
        "lunch": [
            {"name": "Chicken Curry with Rice", "foods": ["chicken breast", "white rice (cooked)", "onion", "tomato", "ghee"]},
            {"name": "Fish Curry with Rice", "foods": ["fish", "white rice (cooked)", "onion", "tomato", "ghee"]},
            {"name": "Egg Curry with Rice", "foods": ["egg", "white rice (cooked)", "onion", "tomato"]},
            {"name": "Chicken Biryani", "foods": ["chicken breast", "white rice (cooked)", "onion", "tomato", "potato"]},
            {"name": "Fish Biryani", "foods": ["fish", "white rice (cooked)", "onion", "tomato"]},
        ],
        "snacks": [
            {"name": "Boiled Egg", "foods": ["boiled egg"]},
            {"name": "Chicken Sandwich", "foods": ["chicken breast", "chapati"]},
            {"name": "Egg Sandwich", "foods": ["boiled egg", "chapati"]},
            {"name": "Chicken Salad", "foods": ["chicken breast", "tomato", "onion", "cucumber"]},
            {"name": "Fish Salad", "foods": ["fish", "tomato", "onion"]},
        ],
        "dinner": [
            {"name": "Chicken Curry with Roti", "foods": ["chicken breast", "chapati", "onion", "tomato"]},
            {"name": "Fish Curry with Roti", "foods": ["fish", "chapati", "onion", "tomato"]},
            {"name": "Egg Curry with Roti", "foods": ["egg", "chapati", "onion", "tomato"]},
            {"name": "Grilled Chicken with Salad", "foods": ["chicken breast", "onion", "tomato", "cucumber"]},
            {"name": "Fish Fry with Salad", "foods": ["fish", "onion", "tomato", "cucumber"]},
        ],
    }
    
    def __init__(self, food_db, diet_preference="1"):
        self.food_db = food_db
        self.diet_preference = diet_preference
    
    def get_filtered_meals(self, meal_type):
        """Get meal options filtered by diet preference"""
        allowed_meals = self.DIET_MEALS.get(self.diet_preference, self.DIET_MEALS["1"])
        meals = [meal for meal in self.MEAL_OPTIONS.get(meal_type, []) if meal["name"] in allowed_meals]
        
        # For non-veg, add non-veg specific meals
        if self.diet_preference == "2" and meal_type in self.NON_VEG_MEALS:
            non_veg_meals = [m for m in self.NON_VEG_MEALS[meal_type] if m["name"] in allowed_meals]
            meals.extend(non_veg_meals)
        
        return meals
    
    def calculate_meal_nutrition(self, meal_foods):
        """Calculate total nutrition for a list of foods"""
        total = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0, "fiber": 0, "iron": 0, "calcium": 0, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 0, "potassium": 0, "zinc": 0}
        
        for food_name in meal_foods:
            food_data = self.food_db.get_food(food_name)
            if food_data:
                total["calories"] += food_data.get("calories", 0)
                total["protein"] += food_data.get("protein", 0)
                total["carbs"] += food_data.get("carbs", 0)
                total["fats"] += food_data.get("fats", 0)
                total["fiber"] += food_data.get("fiber", 0)
                total["iron"] += food_data.get("iron", 0)
                total["calcium"] += food_data.get("calcium", 0)
                total["vitamin_a"] += food_data.get("vitamin_a", 0)
                total["vitamin_c"] += food_data.get("vitamin_c", 0)
                total["vitamin_d"] += food_data.get("vitamin_d", 0)
                total["sodium"] += food_data.get("sodium", 0)
                total["potassium"] += food_data.get("potassium", 0)
                total["zinc"] += food_data.get("zinc", 0)
        
        return {k: round(v, 1) for k, v in total.items()}
    
    def get_food_quantities(self, meal_foods, scale=1.0):
        """Get quantities for each food item based on scale factor with intelligent distribution"""
        
        # Define recommended max quantities for high-calorie items (in grams/ml)
        max_quantities = {
            "ghee": 10,      # Maximum 10ml ghee per meal
            "butter": 15,    # Maximum 15g butter per meal
            "oil": 15,       # Maximum 15ml oil per meal
            "cream": 30,     # Maximum 30g cream per meal
            "peanut": 30,    # Maximum 30g peanuts per snack
            "namkeen": 30,   # Maximum 30g namkeen per snack
            "biscuit": 30,   # Maximum 30g biscuit per snack
            "murukku": 30,   # Maximum 30g murukku per snack
        }
        
        # Define base quantities for different food categories (normal serving sizes)
        # Format: "food_name": (quantity, unit)
        base_quantities = {
            # Proteins
            "chicken breast": (100, "g"),
            "egg": (2, "pcs"),  # 2 eggs
            "boiled egg": (2, "pcs"),
            "fish": (100, "g"),
            "paneer": (75, "g"),
            "dal (lentils)": (100, "g"),
            "moong dal": (100, "g"),
            "toor dal": (100, "g"),
            "urad dal": (100, "g"),
            "chana dal": (100, "g"),
            "soya chunks": (50, "g"),
            "rajma": (100, "g"),
            
            # Carbs
            "white rice (cooked)": (150, "g"),
            "brown rice": (150, "g"),
            "rolled oats": (40, "g"),
            "chapati": (2, "pcs"),  # 2 rotis
            "roti": (2, "pcs"),
            "paratha": (1, "pcs"),
            "poha": (150, "g"),
            "idli": (3, "pcs"),  # 3 idlis
            "dosa": (2, "pcs"),  # 2 dosas
            
            # Vegetables - should stay at reasonable amounts
            "onion": (25, "g"),
            "tomato": (50, "g"),
            "potato": (75, "g"),
            "carrot": (50, "g"),
            "cabbage": (75, "g"),
            "cauliflower": (75, "g"),
            "spinach": (50, "g"),
            "ladies finger": (75, "g"),
            "brinjal": (75, "g"),
            "lauki": (100, "g"),
            "tinda": (100, "g"),
            "capsicum": (50, "g"),
            "beans": (75, "g"),
            "peas": (75, "g"),
            "corn": (50, "g"),
            "mixed vegetables": (100, "g"),
            
            # Dairy
            "milk": (200, "ml"),
            "curd": (100, "g"),
            "butter": (10, "g"),
            "ghee": (5, "ml"),
            "cream": (20, "g"),
            
            # Fruits/Snacks
            "banana": (1, "pcs"),
            "apple": (1, "pcs"),
            "peanut": (20, "g"),
            "roasted chana": (30, "g"),
            "moong dal namkeen": (25, "g"),
            "biscuit": (2, "pcs"),
            "murukku": (25, "g"),
            "namkeen": (25, "g"),
        }
        
        quantities = []
        
        for food_name in meal_foods:
            food_data = self.food_db.get_food(food_name)
            if food_data:
                food_key = food_name.lower()
                
                # Get base quantity from tuple format or use default
                if food_key in base_quantities:
                    base_qty, default_unit = base_quantities[food_key]
                else:
                    base_qty, default_unit = (100, "g")
                
                # Check if it's a high-calorie item with max limit
                max_qty = max_quantities.get(food_key, None)
                
                # Check if it's a main staple food that shouldn't be scaled down
                main_staples = ["chapati", "roti", "rice", "white rice", "brown rice", "paratha", 
                               "idli", "dosa", "poha", "oats", "rolled oats"]
                is_staple = any(staple in food_key for staple in main_staples)
                
                # Use the defined unit from base_quantities, or fallback to database unit
                unit = default_unit
                
                # For main staples, don't scale below base quantity
                # For other foods, apply scale but respect max limits
                if is_staple:
                    # Main staples stay at base quantity
                    quantity = int(base_qty)
                elif max_qty is not None:
                    # High-calorie items use max limit
                    quantity = int(max_qty)
                else:
                    # Scale other foods, but ensure minimum 1
                    quantity = int(base_qty * scale)
                    quantity = max(1, quantity)
                
                quantities.append({
                    "food": food_name,
                    "quantity": quantity,
                    "unit": unit
                })
        
        return quantities
    
    def calculate_nutrition_from_quantities(self, quantities):
        """Calculate nutrition based on actual food quantities"""
        total = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0, "fiber": 0, "iron": 0, "calcium": 0, "vitamin_a": 0, "vitamin_c": 0, "vitamin_d": 0, "sodium": 0, "potassium": 0, "zinc": 0}
        
        for item in quantities:
            food_data = self.food_db.get_food(item["food"])
            if food_data:
                # Get the base nutrition per serving
                base_cal = food_data.get("calories", 0)
                base_protein = food_data.get("protein", 0)
                base_carbs = food_data.get("carbs", 0)
                base_fats = food_data.get("fats", 0)
                base_fiber = food_data.get("fiber", 0)
                base_iron = food_data.get("iron", 0)
                base_calcium = food_data.get("calcium", 0)
                base_vitamin_a = food_data.get("vitamin_a", 0)
                base_vitamin_c = food_data.get("vitamin_c", 0)
                base_vitamin_d = food_data.get("vitamin_d", 0)
                base_sodium = food_data.get("sodium", 0)
                base_potassium = food_data.get("potassium", 0)
                base_zinc = food_data.get("zinc", 0)
                base_serving = food_data.get("serving", 100)
                
                # For items counted in pieces (pcs), assume each piece is ~50g for calculation
                # This is an approximation
                serving_override = None
                if item.get("unit") == "pcs":
                    # Estimate: 1 chapati/roti ~ 50g, 1 egg ~ 50g, etc.
                    food_name = item["food"].lower()
                    if "chapati" in food_name or "roti" in food_name:
                        serving_override = 50
                    elif "egg" in food_name:
                        serving_override = 50
                    elif "idli" in food_name:
                        serving_override = 35
                    elif "dosa" in food_name:
                        serving_override = 75
                    elif "paratha" in food_name:
                        serving_override = 80
                    elif "banana" in food_name:
                        serving_override = 100
                    elif "apple" in food_name:
                        serving_override = 150
                    elif "biscuit" in food_name:
                        serving_override = 15
                
                calc_serving = serving_override if serving_override else base_serving
                
                # Calculate nutrition based on quantity
                ratio = item["quantity"] / calc_serving if calc_serving > 0 else 1
                total["calories"] += base_cal * ratio
                total["protein"] += base_protein * ratio
                total["carbs"] += base_carbs * ratio
                total["fats"] += base_fats * ratio
                total["fiber"] += base_fiber * ratio
                total["iron"] += base_iron * ratio
                total["calcium"] += base_calcium * ratio
                total["vitamin_a"] += base_vitamin_a * ratio
                total["vitamin_c"] += base_vitamin_c * ratio
                total["vitamin_d"] += base_vitamin_d * ratio
                total["sodium"] += base_sodium * ratio
                total["potassium"] += base_potassium * ratio
                total["zinc"] += base_zinc * ratio
        
        return {k: round(v, 1) for k, v in total.items()}
    
    def generate_meal_plan(self, target_calories, target_macros):
        """Generate a personalized meal plan with precise calorie matching"""
        # Distribute calories: Breakfast 25%, Lunch 35%, Dinner 30%, Snacks 10%
        meal_calories = {
            "breakfast": target_calories * 0.20,
            "brunch": target_calories * 0.10,
            "lunch": target_calories * 0.30,
            "snacks": target_calories * 0.10,
            "dinner": target_calories * 0.30,
        }
        
        # Distribute macros proportionally
        meal_macros = {
            "breakfast": {"protein": target_macros['protein'] * 0.20, "carbs": target_macros['carbs'] * 0.20, "fats": target_macros['fats'] * 0.20},
            "brunch": {"protein": target_macros['protein'] * 0.10, "carbs": target_macros['carbs'] * 0.10, "fats": target_macros['fats'] * 0.10},
            "lunch": {"protein": target_macros['protein'] * 0.30, "carbs": target_macros['carbs'] * 0.30, "fats": target_macros['fats'] * 0.30},
            "snacks": {"protein": target_macros['protein'] * 0.10, "carbs": target_macros['carbs'] * 0.10, "fats": target_macros['fats'] * 0.10},
            "dinner": {"protein": target_macros['protein'] * 0.30, "carbs": target_macros['carbs'] * 0.30, "fats": target_macros['fats'] * 0.30},
        }
        
        plan = {}
        
        for meal_type in meal_calories.keys():
            target_cal = meal_calories[meal_type]
            target_protein = meal_macros[meal_type]['protein']
            target_carbs = meal_macros[meal_type]['carbs']
            target_fats = meal_macros[meal_type]['fats']
            
            # Get filtered meals based on diet preference
            meal_options = self.get_filtered_meals(meal_type)
            
            # If no filtered meals, use all meals
            if not meal_options:
                meal_options = self.MEAL_OPTIONS.get(meal_type, [])
            
            # Find the best matching meal option considering all macros
            best_meal = None
            best_score = float('inf')
            best_scale = 1.0
            
            for meal_option in meal_options:
                base_nutrition = self.calculate_meal_nutrition(meal_option["foods"])
                
                # Try different scaling factors (0.5 to 2.0 in 0.1 increments)
                for scale in [s/10 for s in range(5, 21)]:
                    scaled_nutrition = {
                        "calories": base_nutrition["calories"] * scale,
                        "protein": base_nutrition["protein"] * scale,
                        "carbs": base_nutrition["carbs"] * scale,
                        "fats": base_nutrition["fats"] * scale,
                    }
                    
                    # Calculate score based on how close we are to targets
                    # Weight: calories 50%, protein 25%, carbs 15%, fats 10%
                    cal_diff = abs(scaled_nutrition["calories"] - target_cal)
                    protein_diff = abs(scaled_nutrition["protein"] - target_protein)
                    carbs_diff = abs(scaled_nutrition["carbs"] - target_carbs)
                    fats_diff = abs(scaled_nutrition["fats"] - target_fats)
                    
                    # Normalize and weight the differences
                    score = (cal_diff * 0.5) + (protein_diff * 0.25) + (carbs_diff * 0.15) + (fats_diff * 0.10)
                    
                    if score < best_score:
                        best_score = score
                        best_scale = scale
                        # Get quantities for this meal
                        quantities = self.get_food_quantities(meal_option["foods"], scale)
                        # Calculate actual nutrition based on quantities
                        actual_nutrition = self.calculate_nutrition_from_quantities(quantities)
                        best_meal = {
                            "name": meal_option["name"],
                            "foods": meal_option["foods"],
                            "quantities": quantities,
                            "nutrition": actual_nutrition,
                            "target_calories": round(target_cal, 1),
                            "target_protein": round(target_protein, 1),
                            "target_carbs": round(target_carbs, 1),
                            "target_fats": round(target_fats, 1),
                            "scale": round(scale, 1),
                        }
            
            plan[meal_type] = best_meal
        
        return plan
    
    def generate_weekly_meal_plan(self, target_calories, target_macros):
        """Generate a personalized weekly meal plan with varied meals (no repeats)"""
        import random
        
        # Days of the week
        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        
        # Get meal types - including brunch for more variety
        meal_types = ["breakfast", "brunch", "lunch", "snacks", "dinner"]
        
        # Calorie distribution: Breakfast 20%, Brunch 10%, Lunch 30%, Snacks 10%, Dinner 30%
        calorie_distribution = {
            "breakfast": 0.20,
            "brunch": 0.10,
            "lunch": 0.30,
            "snacks": 0.10,
            "dinner": 0.30,
        }
        if self.diet_preference == "4":
            budget_meal_types = {"breakfast": "budget_breakfast", "brunch": "budget_brunch", 
                               "lunch": "budget_lunch", "snacks": "budget_snacks", "dinner": "budget_dinner"}
            all_meals = {}
            for meal_type, budget_type in budget_meal_types.items():
                all_meals[meal_type] = self.MEAL_OPTIONS.get(budget_type, [])
        else:
            all_meals = {meal_type: self.get_filtered_meals(meal_type) for meal_type in meal_types}
            
            # If no filtered meals, use all meals
            for meal_type in meal_types:
                if not all_meals[meal_type]:
                    all_meals[meal_type] = self.MEAL_OPTIONS.get(meal_type, [])
        
        weekly_plan = {}
        used_meals = {meal_type: [] for meal_type in meal_types}
        
        for day in days:
            daily_plan = {}
            
            for meal_type in meal_types:
                target_cal = target_calories * calorie_distribution[meal_type]
                target_protein = target_macros['protein'] * calorie_distribution[meal_type]
                target_carbs = target_macros['carbs'] * calorie_distribution[meal_type]
                target_fats = target_macros['fats'] * calorie_distribution[meal_type]
                
                # Get available meals (not used more than 2 times)
                available_meals = [m for m in all_meals[meal_type] if used_meals[meal_type].count(m["name"]) < 2]
                
                # If all meals used twice, reset and use any meal
                if not available_meals:
                    used_meals[meal_type] = []
                    available_meals = all_meals[meal_type]
                
                if not available_meals:
                    available_meals = all_meals[meal_type]
                
                # Find the best matching meal
                best_meal = None
                best_score = float('inf')
                best_scale = 1.0
                
                for meal_option in available_meals:
                    base_nutrition = self.calculate_meal_nutrition(meal_option["foods"])
                    
                    for scale in [s/10 for s in range(5, 21)]:
                        scaled_nutrition = {
                            "calories": base_nutrition["calories"] * scale,
                            "protein": base_nutrition["protein"] * scale,
                            "carbs": base_nutrition["carbs"] * scale,
                            "fats": base_nutrition["fats"] * scale,
                        }
                        
                        cal_diff = abs(scaled_nutrition["calories"] - target_cal)
                        protein_diff = abs(scaled_nutrition["protein"] - target_protein)
                        carbs_diff = abs(scaled_nutrition["carbs"] - target_carbs)
                        fats_diff = abs(scaled_nutrition["fats"] - target_fats)
                        
                        score = (cal_diff * 0.5) + (protein_diff * 0.25) + (carbs_diff * 0.15) + (fats_diff * 0.10)
                        
                        if score < best_score:
                            best_score = score
                            best_scale = scale
                            # Get quantities for this meal
                            quantities = self.get_food_quantities(meal_option["foods"], scale)
                            # Calculate actual nutrition based on quantities
                            actual_nutrition = self.calculate_nutrition_from_quantities(quantities)
                            best_meal = {
                                "name": meal_option["name"],
                                "foods": meal_option["foods"],
                                "quantities": quantities,
                                "nutrition": actual_nutrition,
                                "target_calories": round(target_cal, 1),
                                "target_protein": round(target_protein, 1),
                                "target_carbs": round(target_carbs, 1),
                                "target_fats": round(target_fats, 1),
                                "scale": round(scale, 1),
                            }
                
                if best_meal:
                    daily_plan[meal_type] = best_meal
                    used_meals[meal_type].append(best_meal["name"])
            
            weekly_plan[day] = daily_plan
        
        return weekly_plan


# ===================== RESULTS DISPLAY =====================
class ResultsDisplay:
    """Display calculation results and meal plans"""
    
    @staticmethod
    def display_profile(profile):
        """Display user profile summary"""
        print("\n" + "="*60)
        print("👤 USER PROFILE SUMMARY")
        print("="*60)
        print(f"  Name:           {profile.name}")
        print(f"  Age:            {profile.age} years")
        print(f"  Gender:         {'Male' if profile.gender == 'M' else 'Female'}")
        print(f"  Weight:         {profile.weight} kg")
        print(f"  Height:         {profile.height} cm")
        print(f"  Activity Level: {UserProfile.ACTIVITY_LEVELS[profile.activity_level]['name']}")
        print(f"  Goal:           {UserProfile.GOALS[profile.goal]['name']}")
    
    @staticmethod
    def display_calorie_results(bmr, tdee, daily_calories):
        """Display calorie calculation results"""
        print("\n" + "="*60)
        print("🔥 CALORIE CALCULATION RESULTS")
        print("="*60)
        print(f"  📊 Basal Metabolic Rate (BMR):     {bmr} calories/day")
        print(f"     (Calories burned at complete rest)")
        print(f"\n  ⚡ Total Daily Energy Expenditure: {tdee} calories/day")
        print(f"     (Calories burned with your activity level)")
        print(f"\n  🎯 Your Daily Calorie Target:      {daily_calories} calories/day")
        print(f"     (Based on your selected goal)")
    
    @staticmethod
    def display_macros(macros):
        """Display macro nutrient requirements"""
        print("\n" + "="*60)
        print("🥗 DAILY MACRO NUTRIENT REQUIREMENTS")
        print("="*60)
        print(f"  🥩 Protein: {macros['protein']}g")
        print(f"  🍞 Carbs:   {macros['carbs']}g")
        print(f"  🥑 Fats:    {macros['fats']}g")
        print(f"\n  💡 Note: Protein is essential for muscle building and repair")
        print(f"     Carbs provide energy for daily activities")
        print(f"     Fats are important for hormone production and nutrient absorption")
    
    @staticmethod
    def display_meal_plan(plan, target_calories):
        """Display generated meal plan"""
        print("\n" + "="*60)
        print("🍽️  YOUR PERSONALIZED MEAL PLAN")
        print("="*60)
        
        total_nutrition = {"calories": 0, "protein": 0, "carbs": 0, "fats": 0}
        
        meal_emojis = {"breakfast": "🌅", "brunch": "🕐", "lunch": "☀️", "snacks": "🍿", "dinner": "🌙"}
        
        for meal_type, meal in plan.items():
            emoji = meal_emojis.get(meal_type, "🍽️")
            print(f"\n  {emoji} {meal_type.upper()}: {meal['name']}")
            print(f"     Foods: {', '.join(meal['foods'])}")
            print(f"     Nutrition: {meal['nutrition']['calories']} cal | "
                  f"P: {meal['nutrition']['protein']}g | "
                  f"C: {meal['nutrition']['carbs']}g | "
                  f"F: {meal['nutrition']['fats']}g")
            
            for key in total_nutrition:
                total_nutrition[key] += meal['nutrition'][key]
        
        print("\n" + "-"*60)
        print(f"  📈 DAILY TOTALS:")
        print(f"     Calories: {round(total_nutrition['calories'])} | "
              f"Protein: {round(total_nutrition['protein'])}g | "
              f"Carbs: {round(total_nutrition['carbs'])}g | "
              f"Fats: {round(total_nutrition['fats'])}g")
        print(f"     Target:   {target_calories} calories")
        print("-"*60)
    
    @staticmethod
    def display_water_advice(target_calories):
        """Display water intake recommendations"""
        water_ml = target_calories * 0.5  # Approximate: 0.5ml per calorie
        water_glasses = water_ml / 250
        
        print("\n" + "="*60)
        print("💧 WATER INTAKE RECOMMENDATION")
        print("="*60)
        print(f"  🚰 Daily Water: {int(water_ml)} ml ({int(water_glasses)} glasses)")
        print(f"  💡 Tip: Drink water before meals to help with portion control")
    
    @staticmethod
    def display_tips(goal):
        """Display goal-specific tips"""
        tips = {
            "1": [  # Lose weight
                "• Eat protein-rich foods to maintain muscle mass",
                "• Include fiber in every meal for fullness",
                "• Avoid sugary drinks and processed foods",
                "• Practice portion control - use smaller plates",
                "• Get 7-8 hours of quality sleep",
            ],
            "2": [  # Maintain
                "• Maintain a balanced diet with all food groups",
                "• Continue regular physical activity",
                "• Monitor your weight weekly",
                "• Stay hydrated throughout the day",
            ],
            "3": [  # Gain
                "• Eat calorie-dense foods like nuts and avocados",
                "• Increase protein intake for muscle building",
                "• Strength training 3-4 times per week",
                "• Eat larger portions or add extra snacks",
            ],
        }
        
        print("\n" + "="*60)
        print("💡 TIPS FOR YOUR GOAL")
        print("="*60)
        for tip in tips[goal]:
            print(f"  {tip}")


# ===================== MAIN APPLICATION =====================
class FoodIQApp:
    """Main application controller"""
    
    def __init__(self):
        self.food_db = FoodDatabase()
        self.user_profile = UserProfile()
        self.calculator = CalorieCalculator()
        self.macro_calc = MacroCalculator()
        self.meal_planner = None
        self.results = {}
    
    def run(self):
        """Run the main application"""
        # Step 1: Get user profile
        self.user_profile.input_profile()
        
        # Step 2: Calculate BMR
        bmr = self.calculator.calculate_bmr(
            self.user_profile.age,
            self.user_profile.gender,
            self.user_profile.weight,
            self.user_profile.height
        )
        
        # Step 3: Calculate TDEE
        activity_multiplier = UserProfile.ACTIVITY_LEVELS[self.user_profile.activity_level]["multiplier"]
        tdee = self.calculator.calculate_tdee(bmr, activity_multiplier)
        
        # Step 4: Calculate daily calorie target
        goal_adjustment = UserProfile.GOALS[self.user_profile.goal]["calorie_adjustment"]
        daily_calories = self.calculator.calculate_daily_calories(tdee, goal_adjustment)
        
        # Step 5: Select macro plan
        macro_choice = MacroCalculator.select_macro_plan()
        
        # Step 6: Calculate macros
        macros = MacroCalculator.calculate_macros(daily_calories, macro_choice)
        
        # Step 7: Generate meal plan
        self.meal_planner = MealPlanner(self.food_db)
        meal_plan = self.meal_planner.generate_meal_plan(daily_calories, macros)
        
        # Step 8: Display results
        ResultsDisplay.display_profile(self.user_profile)
        ResultsDisplay.display_calorie_results(bmr, tdee, daily_calories)
        ResultsDisplay.display_macros(macros)
        ResultsDisplay.display_meal_plan(meal_plan, daily_calories)
        ResultsDisplay.display_water_advice(daily_calories)
        ResultsDisplay.display_tips(self.user_profile.goal)
        
        # Save results
        self.save_results(bmr, tdee, daily_calories, macros, meal_plan)
        
        print("\n" + "="*60)
        print("✅ Thank you for using FOOD IQ!")
        print("   Stay healthy, stay fit! 💪")
        print("="*60)
    
    def save_results(self, bmr, tdee, daily_calories, macros, meal_plan):
        """Save results to a text file"""
        try:
            filename = f"food_iq_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.txt"
            with open(filename, 'w', encoding='utf-8') as f:
                f.write("="*60 + "\n")
                f.write("FOOD IQ - PERSONALIZED DIET PLAN RESULTS\n")
                f.write("="*60 + "\n\n")
                
                f.write(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                f.write("USER PROFILE\n")
                f.write("-"*40 + "\n")
                f.write(f"Name: {self.user_profile.name}\n")
                f.write(f"Age: {self.user_profile.age}\n")
                f.write(f"Gender: {'Male' if self.user_profile.gender == 'M' else 'Female'}\n")
                f.write(f"Weight: {self.user_profile.weight} kg\n")
                f.write(f"Height: {self.user_profile.height} cm\n")
                f.write(f"Activity: {UserProfile.ACTIVITY_LEVELS[self.user_profile.activity_level]['name']}\n")
                f.write(f"Goal: {UserProfile.GOALS[self.user_profile.goal]['name']}\n\n")
                
                f.write("CALORIE REQUIREMENTS\n")
                f.write("-"*40 + "\n")
                f.write(f"BMR: {bmr} calories/day\n")
                f.write(f"TDEE: {tdee} calories/day\n")
                f.write(f"Daily Target: {daily_calories} calories/day\n\n")
                
                f.write("MACRO NUTRIENTS\n")
                f.write("-"*40 + "\n")
                f.write(f"Protein: {macros['protein']}g\n")
                f.write(f"Carbs: {macros['carbs']}g\n")
                f.write(f"Fats: {macros['fats']}g\n\n")
                
                f.write("MEAL PLAN\n")
                f.write("-"*40 + "\n")
                for meal_type, meal in meal_plan.items():
                    f.write(f"\n{meal_type.upper()}: {meal['name']}\n")
                    f.write(f"Foods: {', '.join(meal['foods'])}\n")
                    f.write(f"Calories: {meal['nutrition']['calories']}\n")
            
            print(f"\n📁 Results saved to: {filename}")
        except Exception as e:
            print(f"\n⚠️  Could not save results: {e}")


# ===================== RUN APPLICATION =====================
if __name__ == "__main__":
    app = FoodIQApp()
    app.run()
