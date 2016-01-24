import json
from functools import wraps
from math import ceil
from datetime import datetime

import requests

from . import api_blueprint
from ..main.models import Fridge, Unit, Item

from flask import request, Response, abort, current_app
from flask.ext.login import current_user

DEFAULT_COUNT = 5
DEFAULT_OFFSET = 10
DEFAULT_PER_PAGE = 5

def api_auth_required():
    if not current_user.is_authenticated:
        abort(401)

def params_required(*params):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            for param in params:
                if not request.args.get(param) and not request.form.get(param):
                    abort(400)
            return f(*args, **kwargs)
        return decorated_view
    return wrapper

@api_blueprint.errorhandler(401)
def custom_401(error):
    return Response('access denied', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})

@api_blueprint.errorhandler(400)
def custom_400(error):
    return Response('bad request', 400)

api_blueprint.before_request(api_auth_required)

@api_blueprint.route('/fridges/<int:id>', methods=['DELETE'])
def fridge_delete(id):
    item = Fridge.query.get(id)
    item.delete()
    return Response("successfully executed", 200)

@api_blueprint.route('/fridges/<int:id>', methods=['PUT'])
@params_required('quantity', 'unit_id', 'item_name', 'expiry_date')
def fridge_put(id):
    item = Fridge.query.get(id)
    item.quantity = int(request.args.get('quantity'))
    item.unit_id = int(request.args.get('unit_id'))
    item.item_name = request.args.get('item_name')
    item.expiry_date = datetime.strptime(request.args.get('expiry_date'))
    return Response('successfully executed', 200)


@api_blueprint.route('/fridges/all', methods=['GET'])
def fridge_all():
    items = current_user.groceries.all()
    result = []
    for item in items:
        result.append({
            'id': item.id,
            'quantity': item.quantity,
            'unit': item.unit.abbr,
            'name': item.detail.name,
            'expiry_date': str(item.expiry_date)
            })

    resp = {
        'items': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/fridges', methods=['GET'])
def fridge_get():

    per_page = int(request.args.get('per_page') or DEFAULT_PER_PAGE)
    page = int(request.args.get('page') or 1)
    offset = (page - 1) * per_page

    q = request.args.get('q')
    if q:
        total = current_user.groceries.filter(Item.name.ilike('%' + q + '%')).count()
        items = current_user.groceries.filter(Item.name.ilike('%' + q + '%')).limit(per_page).offset(offset).all()
    else:
        total = current_user.groceries.count()
        items = current_user.groceries.limit(per_page).offset(offset).all()

    total_pages = int(ceil(total / per_page))

    result = []
    for item in items:
        result.append({
            'id': item.id,
            'quantity': item.quantity,
            'unit': item.unit.abbr,
            'name': item.detail.name,
            'expiry_date': str(item.expiry_date)
            })

    resp = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'items': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/fridges', methods=['POST'])
# @params_required('quantity', 'unit_id', 'item_name', 'expiry_date')
def fridge_post():
    quantity = float(request.form.get('quantity'))
    unit_id = int(request.form.get('unit_id'))
    item_name = request.form.get('item_name')
    expiry_date = datetime.strptime(request.form.get('expiry_date'), '%Y-%m-%d %H:%M:%S')

    # current_user.add_grocery(quantity=quantity, unit_id=unit_id, item_name=item_name, expiry_date=expiry_date)
    new_item = Fridge(user_id=current_user.id, quantity=quantity, unit_id=unit_id, expiry_date=expiry_date)
    new_item.item_name = item_name
    new_item.save()
    response = {
        'id': new_item.id,
        'quantity': new_item.quantity,
        'unit': new_item.unit.abbr,
        'name': new_item.detail.name,
        'expiry_date': str(new_item.expiry_date)
    }
    return Response(json.dumps(response), 201)

@api_blueprint.route('/units', methods=['GET'])
def units_get():
    units = Unit.query.all()
    response = []
    for unit in units:
        response.append({
            'id': unit.id,
            'name': unit.name,
            'abbr': unit.abbr
            })
    return Response(json.dumps(response), mimetype='application/json')

@api_blueprint.route('/recipes/<int:id>', methods=['GET'])
def recipes_get_by(id):
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/%s/information' % str(id)
    headers = {'X-Mashape-Key': current_app.config['MASHAPE_KEY']}
    r = requests.get(url, headers=headers)
    recipe = json.loads(r.text)

    result = []
    if 'results' in recipes:
        for recipe in recipes['results']:
            result.append({
                'id': recipe['id'],
                'img_url': recipes['baseUri'] + recipe['image'],
                'title': recipe['title']
                })

    resp = {
        'results': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/recipes', methods=['GET'])
def recipes_get():
    per_page = int(request.args.get('per_page') or DEFAULT_PER_PAGE)
    page = int(request.args.get('page') or 1)
    offset = (page - 1) * per_page if page else 0
    offset += 10

    q = request.args.get('q') or 'meat'

    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/search'
    params = {'query': q, 'number': per_page, 'offset': offset, 'limitLicense': 'false'}
    headers = {'X-Mashape-Key': current_app.config['MASHAPE_KEY']}
    r = requests.get(url, headers=headers, params=params)
    recipes = json.loads(r.text)

    result = []
    if 'results' in recipes:
        for recipe in recipes['results']:
            result.append({
                'id': recipe['id'],
                'img_url': recipes['baseUri'] + recipe['image'],
                'title': recipe['title']
                })

    resp = {
        'results': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/recipes/recommend', methods=['GET'])
def recipes_recommend():
    url = 'https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients'
    all_groceries = current_user.groceries.all()
    ingredients = []
    for grocery in all_groceries:
        ingredients.append(grocery.detail.name)
    params = {'limitLicense': 'false', 'number': 4, 'ranking': 2,
                'ingredients': ','.join(ingredients).lower()}
    headers = {'X-Mashape-Key': current_app.config['MASHAPE_KEY']}
    r = requests.get(url, headers=headers, params=params)
    recipes = json.loads(r.text)

    result = []
    for recipe in recipes:
        result.append({
            'id': recipe['id'],
            'img_url': recipe['image'],
            'title': recipe['title']
            })

    resp = {
        'results': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')