from flask import render_template
from flask.ext.login import login_required
from . import main_blueprint

@main_blueprint.route('/')
def index():
    return render_template('index.html')

@main_blueprint.route('/fridge')
@login_required
def my_fridge():
    return render_template('my_fridge.html')

@main_blueprint.route('/receipes')
@login_required
def my_receipes():
    return render_template('my_receipes.html')

@main_blueprint.route('/grocery_cart')
@login_required
def my_grocery_cart():
    return render_template('my_grocery_cart.html')

@main_blueprint.route('/nutrition')
@login_required
def my_nutrition():
    return render_template('my_nutrition.html')