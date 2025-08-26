from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

class User(UserMixin, db.Model):
    """User model for authentication and user management."""
    __tablename__ = 'users'
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    meals = db.relationship('Meal', backref='user', lazy=True)
    symptoms = db.relationship('Symptom', backref='user', lazy=True)
    
    def set_password(self, password):
        """Hash and set the user's password."""
        self.password_hash = generate_password_hash(password)
    
    def check_password(self, password):
        """Check if the provided password matches the hash."""
        return check_password_hash(self.password_hash, password)
    
    def __repr__(self):
        return f'<User {self.username}>'


class Food(db.Model):
    """Food model for storing food information and categories."""
    __tablename__ = 'foods'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    category = db.Column(db.String(100))  # spicy, dairy, gluten, etc.
    ingredients = db.Column(db.Text)  # JSON string of ingredients
    allergens = db.Column(db.Text)  # JSON string of allergens
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    meals = db.relationship('Meal', backref='food', lazy=True)
    
    def __repr__(self):
        return f'<Food {self.name}>'


class Meal(db.Model):
    """Meal model for tracking food consumption."""
    __tablename__ = 'meals'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    food_id = db.Column(db.Integer, db.ForeignKey('foods.id'), nullable=False)
    quantity = db.Column(db.Float)  # Amount consumed
    meal_time = db.Column(db.DateTime, nullable=False)  # When the meal was eaten
    notes = db.Column(db.Text)  # Additional notes about the meal
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    symptoms = db.relationship('Symptom', backref='meal', lazy=True)
    
    def __repr__(self):
        return f'<Meal {self.id} - {self.food.name} at {self.meal_time}>'


class Symptom(db.Model):
    """Symptom model for tracking digestive symptoms."""
    __tablename__ = 'symptoms'
    
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    meal_id = db.Column(db.Integer, db.ForeignKey('meals.id'), nullable=False)
    symptom_type = db.Column(db.String(100), nullable=False)  # nausea, bloating, etc.
    severity = db.Column(db.Integer, nullable=False)  # 1-5 scale
    onset_time = db.Column(db.DateTime, nullable=False)  # When symptoms started
    duration = db.Column(db.Integer)  # Duration in minutes
    notes = db.Column(db.Text)  # Additional symptom notes
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<Symptom {self.symptom_type} (severity: {self.severity})>'


class FoodCategory(db.Model):
    """Predefined food categories for consistent classification."""
    __tablename__ = 'food_categories'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    risk_level = db.Column(db.Integer)  # 1-5 scale for general risk assessment
    
    def __repr__(self):
        return f'<FoodCategory {self.name}>'


class SymptomType(db.Model):
    """Predefined symptom types for consistent tracking."""
    __tablename__ = 'symptom_types'
    
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    description = db.Column(db.Text)
    severity_scale = db.Column(db.Text)  # JSON string describing severity levels
    
    def __repr__(self):
        return f'<SymptomType {self.name}>'
