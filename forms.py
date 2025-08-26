from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, TextAreaField, SelectField, FloatField, DateTimeField, IntegerField
from wtforms.validators import DataRequired, Email, Length, EqualTo, NumberRange, Optional
from datetime import datetime

class RegistrationForm(FlaskForm):
    """Form for user registration."""
    username = StringField('Username', validators=[DataRequired(), Length(min=3, max=80)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired(), Length(min=6)])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class LoginForm(FlaskForm):
    """Form for user login."""
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class FoodForm(FlaskForm):
    """Form for adding new foods."""
    name = StringField('Food Name', validators=[DataRequired(), Length(max=200)])
    category = SelectField('Category', choices=[
        ('', 'Select Category'),
        ('dairy', 'Dairy'),
        ('gluten', 'Gluten'),
        ('spicy', 'Spicy'),
        ('processed', 'Processed'),
        ('raw', 'Raw'),
        ('fermented', 'Fermented'),
        ('high_fiber', 'High Fiber'),
        ('high_fat', 'High Fat'),
        ('sugary', 'Sugary'),
        ('acidic', 'Acidic'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    ingredients = TextAreaField('Ingredients (optional)', validators=[Optional()])
    allergens = TextAreaField('Allergens (optional)', validators=[Optional()])
    submit = SubmitField('Add Food')


class MealLogForm(FlaskForm):
    """Form for logging meals."""
    food_id = SelectField('Food', coerce=int, validators=[DataRequired()])
    quantity = FloatField('Quantity (optional)', validators=[Optional(), NumberRange(min=0)])
    meal_time = DateTimeField('Meal Time', validators=[DataRequired()], default=datetime.utcnow)
    notes = TextAreaField('Notes (optional)', validators=[Optional()])
    submit = SubmitField('Log Meal')


class SymptomForm(FlaskForm):
    """Form for logging symptoms."""
    meal_id = SelectField('Related Meal', coerce=int, validators=[DataRequired()])
    symptom_type = SelectField('Symptom Type', choices=[
        ('', 'Select Symptom'),
        ('nausea', 'Nausea'),
        ('bloating', 'Bloating'),
        ('abdominal_pain', 'Abdominal Pain'),
        ('diarrhea', 'Diarrhea'),
        ('constipation', 'Constipation'),
        ('heartburn', 'Heartburn'),
        ('gas', 'Gas'),
        ('indigestion', 'Indigestion'),
        ('vomiting', 'Vomiting'),
        ('other', 'Other')
    ], validators=[DataRequired()])
    severity = SelectField('Severity', choices=[
        (1, '1 - Very Mild'),
        (2, '2 - Mild'),
        (3, '3 - Moderate'),
        (4, '4 - Severe'),
        (5, '5 - Very Severe')
    ], coerce=int, validators=[DataRequired()])
    onset_time = DateTimeField('Onset Time', validators=[DataRequired()], default=datetime.utcnow)
    duration = IntegerField('Duration (minutes, optional)', validators=[Optional(), NumberRange(min=0)])
    notes = TextAreaField('Notes (optional)', validators=[Optional()])
    submit = SubmitField('Log Symptom')


class SearchForm(FlaskForm):
    """Form for searching food and symptom history."""
    search_term = StringField('Search', validators=[Optional()])
    date_from = DateTimeField('From Date', validators=[Optional()])
    date_to = DateTimeField('To Date', validators=[Optional()])
    category = SelectField('Food Category', choices=[
        ('', 'All Categories'),
        ('dairy', 'Dairy'),
        ('gluten', 'Gluten'),
        ('spicy', 'Spicy'),
        ('processed', 'Processed'),
        ('raw', 'Raw'),
        ('fermented', 'Fermented'),
        ('high_fiber', 'High Fiber'),
        ('high_fat', 'High Fat'),
        ('sugary', 'Sugary'),
        ('acidic', 'Acidic'),
        ('other', 'Other')
    ], validators=[Optional()])
    submit = SubmitField('Search')
