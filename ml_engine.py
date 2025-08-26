"""
Machine Learning Engine for Tummy Tracker
This module provides ML functionality for analyzing food-symptom patterns.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.metrics import accuracy_score, classification_report
import joblib
import os
from datetime import datetime, timedelta

class TummyTrackerML:
    """Machine learning engine for food intolerance prediction."""
    
    def __init__(self, model_path='data/models/'):
        self.model_path = model_path
        self.models = {}
        self.label_encoders = {}
        self.scaler = StandardScaler()
        self.is_trained = False
        
        # Ensure model directory exists
        os.makedirs(model_path, exist_ok=True)
        
    def prepare_features(self, meals_data, symptoms_data):
        """
        Prepare features for machine learning from meals and symptoms data.
        
        Args:
            meals_data: List of meal objects with food information
            symptoms_data: List of symptom objects
            
        Returns:
            X: Feature matrix
            y: Target variable (1 if symptoms occurred, 0 if not)
        """
        if not meals_data:
            return None, None
            
        # Create a mapping of meal_id to symptoms
        meal_symptoms = {}
        for symptom in symptoms_data:
            if symptom.meal_id not in meal_symptoms:
                meal_symptoms[symptom.meal_id] = []
            meal_symptoms[symptom.meal_id].append(symptom)
        
        features = []
        targets = []
        
        for meal in meals_data:
            # Basic meal features
            meal_features = {
                'food_category': meal.food.category,
                'meal_hour': meal.meal_time.hour,
                'meal_day_of_week': meal.meal_time.weekday(),
                'has_quantity': 1 if meal.quantity else 0,
                'quantity': meal.quantity if meal.quantity else 0,
                'has_notes': 1 if meal.notes else 0
            }
            
            # Food-specific features
            if meal.food.ingredients:
                meal_features['has_ingredients'] = 1
                # Count common problematic ingredients
                ingredients_lower = meal.food.ingredients.lower()
                meal_features['has_dairy'] = 1 if any(word in ingredients_lower for word in ['milk', 'cheese', 'yogurt', 'butter', 'cream']) else 0
                meal_features['has_gluten'] = 1 if any(word in ingredients_lower for word in ['wheat', 'flour', 'bread', 'pasta']) else 0
                meal_features['has_spicy'] = 1 if any(word in ingredients_lower for word in ['pepper', 'chili', 'hot', 'spicy']) else 0
            else:
                meal_features['has_ingredients'] = 0
                meal_features['has_dairy'] = 0
                meal_features['has_gluten'] = 0
                meal_features['has_spicy'] = 0
            
            # Allergen features
            if meal.food.allergens:
                meal_features['has_allergens'] = 1
                allergens_lower = meal.food.allergens.lower()
                meal_features['allergen_count'] = len([a for a in ['dairy', 'nuts', 'gluten', 'soy', 'fish'] if a in allergens_lower])
            else:
                meal_features['has_allergens'] = 0
                meal_features['allergen_count'] = 0
            
            # Temporal features
            meal_features['days_since_epoch'] = (meal.meal_time - datetime(1970, 1, 1)).days
            
            # Target: Did this meal cause symptoms?
            meal_features['caused_symptoms'] = 1 if meal.id in meal_symptoms else 0
            
            features.append(meal_features)
            targets.append(meal_features['caused_symptoms'])
        
        # Convert to DataFrame
        df = pd.DataFrame(features)
        
        # Encode categorical variables
        categorical_cols = ['food_category']
        for col in categorical_cols:
            if col in df.columns:
                le = LabelEncoder()
                df[col] = le.fit_transform(df[col].astype(str))
                self.label_encoders[col] = le
        
        # Remove target column from features
        X = df.drop('caused_symptoms', axis=1)
        y = df['caused_symptoms']
        
        return X, y
    
    def train_models(self, X, y):
        """
        Train multiple machine learning models.
        
        Args:
            X: Feature matrix
            y: Target variable
        """
        if X is None or y is None or len(X) < 10:
            print("Not enough data to train models. Need at least 10 meals.")
            return False
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale features
        X_train_scaled = self.scaler.fit_transform(X_train)
        X_test_scaled = self.scaler.transform(X_test)
        
        # Train Random Forest
        rf_model = RandomForestClassifier(n_estimators=100, random_state=42)
        rf_model.fit(X_train_scaled, y_train)
        rf_score = accuracy_score(y_test, rf_model.predict(X_test_scaled))
        
        # Train Logistic Regression
        lr_model = LogisticRegression(random_state=42, max_iter=1000)
        lr_model.fit(X_train_scaled, y_train)
        lr_score = accuracy_score(y_test, lr_model.predict(X_test_scaled))
        
        # Store models
        self.models['random_forest'] = {
            'model': rf_model,
            'accuracy': rf_score,
            'type': 'Random Forest'
        }
        
        self.models['logistic_regression'] = {
            'model': lr_model,
            'accuracy': lr_score,
            'type': 'Logistic Regression'
        }
        
        self.is_trained = True
        
        print(f"Models trained successfully!")
        print(f"Random Forest Accuracy: {rf_score:.3f}")
        print(f"Logistic Regression Accuracy: {lr_score:.3f}")
        
        # Save models
        self.save_models()
        
        return True
    
    def predict_symptoms(self, meal_features):
        """
        Predict whether a meal might cause symptoms.
        
        Args:
            meal_features: Dictionary of meal features
            
        Returns:
            dict: Prediction results with confidence scores
        """
        if not self.is_trained:
            return {
                'prediction': 'Model not trained',
                'confidence': 0,
                'recommendation': 'Need more data to make predictions'
            }
        
        # Prepare features
        df = pd.DataFrame([meal_features])
        
        # Encode categorical variables
        for col, le in self.label_encoders.items():
            if col in df.columns:
                df[col] = le.transform(df[col].astype(str))
        
        # Scale features
        X_scaled = self.scaler.transform(df)
        
        # Make predictions with both models
        rf_pred = self.models['random_forest']['model'].predict_proba(X_scaled)[0]
        lr_pred = self.models['logistic_regression']['model'].predict_proba(X_scaled)[0]
        
        # Ensemble prediction (average of both models)
        ensemble_prob = (rf_pred + lr_pred) / 2
        prediction = 1 if ensemble_prob[1] > 0.5 else 0
        confidence = max(ensemble_prob)
        
        # Generate recommendations
        recommendation = self._generate_recommendation(meal_features, prediction, confidence)
        
        return {
            'prediction': 'Likely to cause symptoms' if prediction == 1 else 'Unlikely to cause symptoms',
            'confidence': confidence,
            'recommendation': recommendation,
            'model_details': {
                'random_forest': {
                    'prediction': 'Likely' if rf_pred[1] > 0.5 else 'Unlikely',
                    'confidence': max(rf_pred)
                },
                'logistic_regression': {
                    'prediction': 'Likely' if lr_pred[1] > 0.5 else 'Unlikely',
                    'confidence': max(lr_pred)
                }
            }
        }
    
    def _generate_recommendation(self, meal_features, prediction, confidence):
        """Generate personalized recommendations based on prediction."""
        if prediction == 1:  # Likely to cause symptoms
            if meal_features.get('food_category') == 'dairy':
                return "Consider dairy alternatives like almond milk or coconut yogurt."
            elif meal_features.get('food_category') == 'gluten':
                return "Try gluten-free alternatives like quinoa or rice."
            elif meal_features.get('food_category') == 'spicy':
                return "Consider milder versions or reduce spice levels."
            else:
                return "Monitor your symptoms and consider avoiding this food category temporarily."
        else:  # Unlikely to cause symptoms
            return "This food appears safe for you based on current data."
    
    def get_feature_importance(self):
        """Get feature importance from the Random Forest model."""
        if not self.is_trained or 'random_forest' not in self.models:
            return None
        
        rf_model = self.models['random_forest']['model']
        feature_names = ['food_category', 'meal_hour', 'meal_day_of_week', 'has_quantity', 
                        'quantity', 'has_notes', 'has_ingredients', 'has_dairy', 'has_gluten', 
                        'has_spicy', 'has_allergens', 'allergen_count', 'days_since_epoch']
        
        importance = rf_model.feature_importances_
        feature_importance = list(zip(feature_names, importance))
        feature_importance.sort(key=lambda x: x[1], reverse=True)
        
        return feature_importance
    
    def save_models(self):
        """Save trained models to disk."""
        if not self.is_trained:
            return
        
        for name, model_info in self.models.items():
            model_path = os.path.join(self.model_path, f'{name}.pkl')
            joblib.dump(model_info['model'], model_path)
        
        # Save scaler and encoders
        joblib.dump(self.scaler, os.path.join(self.model_path, 'scaler.pkl'))
        joblib.dump(self.label_encoders, os.path.join(self.model_path, 'encoders.pkl'))
        
        print("Models saved successfully!")
    
    def load_models(self):
        """Load trained models from disk."""
        try:
            for name in ['random_forest', 'logistic_regression']:
                model_path = os.path.join(self.model_path, f'{name}.pkl')
                if os.path.exists(model_path):
                    model = joblib.load(model_path)
                    self.models[name] = {
                        'model': model,
                        'type': name.replace('_', ' ').title()
                    }
            
            # Load scaler and encoders
            scaler_path = os.path.join(self.model_path, 'scaler.pkl')
            encoders_path = os.path.join(self.model_path, 'encoders.pkl')
            
            if os.path.exists(scaler_path) and os.path.exists(encoders_path):
                self.scaler = joblib.load(scaler_path)
                self.label_encoders = joblib.load(encoders_path)
                self.is_trained = True
                print("Models loaded successfully!")
                return True
            
        except Exception as e:
            print(f"Error loading models: {e}")
        
        return False
    
    def get_model_status(self):
        """Get current status of the ML system."""
        return {
            'is_trained': self.is_trained,
            'models_available': list(self.models.keys()),
            'total_models': len(self.models)
        }
