#!/usr/bin/env python3
"""
Simple test script to verify Tummy Tracker application setup.
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported."""
    print("Testing imports...")
    
    try:
        from flask import Flask
        print("✓ Flask imported successfully")
    except ImportError as e:
        print(f"✗ Flask import failed: {e}")
        return False
    
    try:
        from flask_sqlalchemy import SQLAlchemy
        print("✓ Flask-SQLAlchemy imported successfully")
    except ImportError as e:
        print(f"✗ Flask-SQLAlchemy import failed: {e}")
        return False
    
    try:
        from flask_login import LoginManager
        print("✓ Flask-Login imported successfully")
    except ImportError as e:
        print(f"✗ Flask-Login import failed: {e}")
        return False
    
    try:
        import pandas as pd
        print("✓ Pandas imported successfully")
    except ImportError as e:
        print(f"✗ Pandas import failed: {e}")
        return False
    
    try:
        import numpy as np
        print("✓ NumPy imported successfully")
    except ImportError as e:
        print(f"✗ NumPy import failed: {e}")
        return False
    
    try:
        from sklearn.ensemble import RandomForestClassifier
        print("✓ Scikit-learn imported successfully")
    except ImportError as e:
        print(f"✗ Scikit-learn import failed: {e}")
        return False
    
    return True

def test_app_creation():
    """Test if the Flask app can be created."""
    print("\nTesting app creation...")
    
    try:
        from app import app
        print("✓ Flask app created successfully")
        return True
    except Exception as e:
        print(f"✗ Flask app creation failed: {e}")
        return False

def test_database_models():
    """Test if database models can be imported."""
    print("\nTesting database models...")
    
    try:
        from models import User, Food, Meal, Symptom
        print("✓ Database models imported successfully")
        return True
    except Exception as e:
        print(f"✗ Database models import failed: {e}")
        return False

def test_ml_engine():
    """Test if ML engine can be imported."""
    print("\nTesting ML engine...")
    
    try:
        from ml_engine import TummyTrackerML
        print("✓ ML engine imported successfully")
        return True
    except Exception as e:
        print(f"✗ ML engine import failed: {e}")
        return False

def test_forms():
    """Test if forms can be imported."""
    print("\nTesting forms...")
    
    try:
        from forms import RegistrationForm, LoginForm, FoodForm
        print("✓ Forms imported successfully")
        return True
    except Exception as e:
        print(f"✗ Forms import failed: {e}")
        return False

def main():
    """Run all tests."""
    print("=" * 50)
    print("Tummy Tracker Application Test")
    print("=" * 50)
    
    tests = [
        test_imports,
        test_app_creation,
        test_database_models,
        test_ml_engine,
        test_forms
    ]
    
    passed = 0
    total = len(tests)
    
    for test in tests:
        if test():
            passed += 1
    
    print("\n" + "=" * 50)
    print(f"Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All tests passed! Your application is ready to run.")
        print("\nNext steps:")
        print("1. Run: python init_db.py")
        print("2. Run: python app.py")
        print("3. Open: http://localhost:5000")
    else:
        print("❌ Some tests failed. Please check the errors above.")
        print("\nCommon solutions:")
        print("1. Install missing packages: pip install -r requirements.txt")
        print("2. Check Python version (3.8+ required)")
        print("3. Verify all files are in the correct directory")
    
    print("=" * 50)
    
    return passed == total

if __name__ == '__main__':
    success = main()
    sys.exit(0 if success else 1)
