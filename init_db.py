#!/usr/bin/env python3
"""
Database initialization script for Tummy Tracker.
This script creates the database tables and populates them with sample data.
"""

from app import app, db
from models import User, Food, FoodCategory, SymptomType
from werkzeug.security import generate_password_hash
from datetime import datetime

def init_database():
    """Initialize the database with tables and sample data."""
    with app.app_context():
        # Create all tables
        print("Creating database tables...")
        db.create_all()
        print("✓ Database tables created successfully!")
        
        # Check if sample data already exists
        if User.query.first():
            print("Sample data already exists. Skipping data population.")
            return
        
        print("Populating database with sample data...")
        
        # Create sample food categories
        categories = [
            {'name': 'dairy', 'description': 'Milk and dairy products', 'risk_level': 3},
            {'name': 'gluten', 'description': 'Wheat, barley, and rye products', 'risk_level': 4},
            {'name': 'spicy', 'description': 'Hot peppers and spicy foods', 'risk_level': 2},
            {'name': 'processed', 'description': 'Packaged and processed foods', 'risk_level': 3},
            {'name': 'raw', 'description': 'Uncooked vegetables and fruits', 'risk_level': 2},
            {'name': 'fermented', 'description': 'Fermented foods like kimchi, sauerkraut', 'risk_level': 2},
            {'name': 'high_fiber', 'description': 'High fiber foods', 'risk_level': 1},
            {'name': 'high_fat', 'description': 'High fat foods', 'risk_level': 2},
            {'name': 'sugary', 'description': 'High sugar foods', 'risk_level': 2},
            {'name': 'acidic', 'description': 'Acidic foods and beverages', 'risk_level': 3},
            {'name': 'other', 'description': 'Other food categories', 'risk_level': 1}
        ]
        
        for cat_data in categories:
            category = FoodCategory(**cat_data)
            db.session.add(category)
        
        # Create sample symptom types
        symptom_types = [
            {'name': 'nausea', 'description': 'Feeling sick to the stomach', 'severity_scale': '1-5 scale'},
            {'name': 'bloating', 'description': 'Abdominal swelling and discomfort', 'severity_scale': '1-5 scale'},
            {'name': 'abdominal_pain', 'description': 'Pain in the stomach area', 'severity_scale': '1-5 scale'},
            {'name': 'diarrhea', 'description': 'Loose, watery stools', 'severity_scale': '1-5 scale'},
            {'name': 'constipation', 'description': 'Difficulty passing stools', 'severity_scale': '1-5 scale'},
            {'name': 'heartburn', 'description': 'Burning sensation in chest', 'severity_scale': '1-5 scale'},
            {'name': 'gas', 'description': 'Excessive flatulence', 'severity_scale': '1-5 scale'},
            {'name': 'indigestion', 'description': 'General digestive discomfort', 'severity_scale': '1-5 scale'},
            {'name': 'vomiting', 'description': 'Throwing up', 'severity_scale': '1-5 scale'},
            {'name': 'other', 'description': 'Other digestive symptoms', 'severity_scale': '1-5 scale'}
        ]
        
        for symp_data in symptom_types:
            symptom_type = SymptomType(**symp_data)
            db.session.add(symptom_type)
        
        # Create sample foods
        sample_foods = [
            {
                'name': 'Spicy Chicken Tacos',
                'category': 'spicy',
                'ingredients': 'Chicken, tortillas, hot sauce, onions, cilantro',
                'allergens': 'Gluten (tortillas)'
            },
            {
                'name': 'Greek Yogurt with Berries',
                'category': 'dairy',
                'ingredients': 'Greek yogurt, strawberries, blueberries, honey',
                'allergens': 'Dairy'
            },
            {
                'name': 'Whole Wheat Bread',
                'category': 'gluten',
                'ingredients': 'Whole wheat flour, water, yeast, salt',
                'allergens': 'Gluten'
            },
            {
                'name': 'Grilled Salmon',
                'category': 'other',
                'ingredients': 'Salmon fillet, olive oil, lemon, herbs',
                'allergens': 'Fish'
            },
            {
                'name': 'Kimchi',
                'category': 'fermented',
                'ingredients': 'Napa cabbage, chili peppers, garlic, ginger',
                'allergens': 'None'
            },
            {
                'name': 'Pizza',
                'category': 'gluten',
                'ingredients': 'Pizza dough, tomato sauce, cheese, toppings',
                'allergens': 'Gluten, Dairy'
            },
            {
                'name': 'Ice Cream',
                'category': 'dairy',
                'ingredients': 'Milk, cream, sugar, vanilla',
                'allergens': 'Dairy'
            },
            {
                'name': 'Sushi',
                'category': 'raw',
                'ingredients': 'Rice, fish, seaweed, vegetables',
                'allergens': 'Fish, Soy'
            }
        ]
        
        for food_data in sample_foods:
            food = Food(**food_data)
            db.session.add(food)
        
        # Commit all changes
        db.session.commit()
        print("✓ Sample data populated successfully!")
        
        print("\nDatabase initialization complete!")
        print("You can now run the application with: python app.py")

if __name__ == '__main__':
    init_database()
