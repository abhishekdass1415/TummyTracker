from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
from flask_login import LoginManager, login_user, logout_user, login_required, current_user
from urllib.parse import urlparse
import os
from datetime import datetime, timedelta

from models import db, User, Food, Meal, Symptom, FoodCategory, SymptomType
from forms import RegistrationForm, LoginForm, FoodForm, MealLogForm, SymptomForm, SearchForm

# Initialize Flask app
app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'dev-secret-key-change-in-production')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///tummy_tracker.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def index():
    """Home page with overview and quick actions."""
    if current_user.is_authenticated:
        # Get recent meals and symptoms for dashboard
        recent_meals = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.meal_time.desc()).limit(5).all()
        recent_symptoms = Symptom.query.filter_by(user_id=current_user.id).order_by(Symptom.onset_time.desc()).limit(5).all()
        
        # Get basic stats
        total_meals = Meal.query.filter_by(user_id=current_user.id).count()
        total_symptoms = Symptom.query.filter_by(user_id=current_user.id).count()
        
        return render_template('dashboard.html', 
                             recent_meals=recent_meals, 
                             recent_symptoms=recent_symptoms,
                             total_meals=total_meals,
                             total_symptoms=total_symptoms)
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    """User registration page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = RegistrationForm()
    if form.validate_on_submit():
        # Check if username or email already exists
        if User.query.filter_by(username=form.username.data).first():
            flash('Username already exists. Please choose a different one.', 'error')
            return render_template('register.html', form=form)
        
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered. Please use a different email.', 'error')
            return render_template('register.html', form=form)
        
        # Create new user
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """User login page."""
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and user.check_password(form.password.data):
            login_user(user)
            next_page = request.args.get('next')
            if not next_page or urlparse(next_page).netloc != '':
                next_page = url_for('index')
            return redirect(next_page)
        else:
            flash('Invalid username or password.', 'error')
    
    return render_template('login.html', form=form)

@app.route('/logout')
@login_required
def logout():
    """User logout."""
    logout_user()
    return redirect(url_for('index'))

@app.route('/foods', methods=['GET', 'POST'])
@login_required
def foods():
    """Food management page."""
    form = FoodForm()
    if form.validate_on_submit():
        food = Food(
            name=form.name.data,
            category=form.category.data,
            ingredients=form.ingredients.data,
            allergens=form.allergens.data
        )
        db.session.add(food)
        db.session.commit()
        flash('Food added successfully!', 'success')
        return redirect(url_for('foods'))
    
    # Get all foods
    foods_list = Food.query.order_by(Food.name).all()
    return render_template('foods.html', form=form, foods=foods_list)

@app.route('/meals', methods=['GET', 'POST'])
@login_required
def meals():
    """Meal logging page."""
    form = MealLogForm()
    
    # Populate food choices
    form.food_id.choices = [(f.id, f.name) for f in Food.query.order_by(Food.name).all()]
    
    if form.validate_on_submit():
        meal = Meal(
            user_id=current_user.id,
            food_id=form.food_id.data,
            quantity=form.quantity.data,
            meal_time=form.meal_time.data,
            notes=form.notes.data
        )
        db.session.add(meal)
        db.session.commit()
        flash('Meal logged successfully!', 'success')
        return redirect(url_for('meals'))
    
    # Get user's meals
    meals_list = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.meal_time.desc()).all()
    return render_template('meals.html', form=form, meals=meals_list)

@app.route('/symptoms', methods=['GET', 'POST'])
@login_required
def symptoms():
    """Symptom logging page."""
    form = SymptomForm()
    
    # Populate meal choices (only meals from the last 24 hours)
    yesterday = datetime.utcnow() - timedelta(days=1)
    recent_meals = Meal.query.filter(
        Meal.user_id == current_user.id,
        Meal.meal_time >= yesterday
    ).order_by(Meal.meal_time.desc()).all()
    form.meal_id.choices = [(m.id, f"{m.food.name} at {m.meal_time.strftime('%Y-%m-%d %H:%M')}") for m in recent_meals]
    
    if form.validate_on_submit():
        symptom = Symptom(
            user_id=current_user.id,
            meal_id=form.meal_id.data,
            symptom_type=form.symptom_type.data,
            severity=form.severity.data,
            onset_time=form.onset_time.data,
            duration=form.duration.data,
            notes=form.notes.data
        )
        db.session.add(symptom)
        db.session.commit()
        flash('Symptom logged successfully!', 'success')
        return redirect(url_for('symptoms'))
    
    # Get user's symptoms
    symptoms_list = Symptom.query.filter_by(user_id=current_user.id).order_by(Symptom.onset_time.desc()).all()
    return render_template('symptoms.html', form=form, symptoms=symptoms_list)

@app.route('/history')
@login_required
def history():
    """Food and symptom history page."""
    form = SearchForm()
    
    # Get search parameters
    search_term = request.args.get('search_term', '')
    date_from = request.args.get('date_from', '')
    date_to = request.args.get('date_to', '')
    category = request.args.get('category', '')
    
    # Build query for meals
    meals_query = Meal.query.filter_by(user_id=current_user.id)
    if search_term:
        meals_query = meals_query.join(Food).filter(Food.name.ilike(f'%{search_term}%'))
    if category:
        meals_query = meals_query.join(Food).filter(Food.category == category)
    if date_from:
        meals_query = meals_query.filter(Meal.meal_time >= datetime.fromisoformat(date_from))
    if date_to:
        meals_query = meals_query.filter(Meal.meal_time <= datetime.fromisoformat(date_to))
    
    meals_list = meals_query.order_by(Meal.meal_time.desc()).all()
    
    return render_template('history.html', form=form, meals=meals_list)

@app.route('/analytics')
@login_required
def analytics():
    """Analytics and pattern analysis page."""
    # Get basic statistics
    total_meals = Meal.query.filter_by(user_id=current_user.id).count()
    total_symptoms = Symptom.query.filter_by(user_id=current_user.id).count()
    
    if total_meals == 0:
        return render_template('analytics.html', 
                             total_meals=total_meals, 
                             total_symptoms=total_symptoms,
                             show_analytics=False)
    
    # Get food category breakdown
    from sqlalchemy import func
    category_stats = db.session.query(
        Food.category,
        func.count(Meal.id).label('meal_count'),
        func.avg(Symptom.severity).label('avg_severity')
    ).join(Meal).outerjoin(Symptom).filter(
        Meal.user_id == current_user.id
    ).group_by(Food.category).all()
    
    # Get symptom type breakdown
    symptom_stats = db.session.query(
        Symptom.symptom_type,
        func.count(Symptom.id).label('count'),
        func.avg(Symptom.severity).label('avg_severity')
    ).filter(
        Symptom.user_id == current_user.id
    ).group_by(Symptom.symptom_type).all()
    
    return render_template('analytics.html',
                         total_meals=total_meals,
                         total_symptoms=total_symptoms,
                         category_stats=category_stats,
                         symptom_stats=symptom_stats,
                         show_analytics=True)

@app.route('/api/foods')
@login_required
def api_foods():
    """API endpoint for getting foods (for AJAX requests)."""
    foods = Food.query.order_by(Food.name).all()
    return jsonify([{'id': f.id, 'name': f.name, 'category': f.category} for f in foods])

@app.route('/api/meals')
@login_required
def api_meals():
    """API endpoint for getting user's meals."""
    meals = Meal.query.filter_by(user_id=current_user.id).order_by(Meal.meal_time.desc()).all()
    return jsonify([{
        'id': m.id,
        'food_name': m.food.name,
        'meal_time': m.meal_time.isoformat(),
        'quantity': m.quantity,
        'notes': m.notes
    } for m in meals])

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
