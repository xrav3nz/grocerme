from flask import render_template
from . import main_blueprint

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/fridge')
def my_fridge():
    return render_template('my_fridge.html')

@main_blueprint.route('/receipes')
def my_receipes():
    return render_template('my_receipes.html')

@main_blueprint.route('/grocery_cart')
def my_grocery_cart():
    return render_template('my_grocery_cart.html')

@main_blueprint.route('/nutrition')
def my_nutrition():
    return render_template('my_nutrition.html')