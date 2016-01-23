import json
from functools import wraps
from math import ceil
from datetime import datetime

from . import api_blueprint
from ..main.models import Fridge, Unit, Item

from flask import request, Response, abort
from flask.ext.login import current_user

DEFAULT_COUNT = 5
DEFAULT_OFFSET = 10
DEFAULT_PER_PAGE = 5

def api_auth_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        if not current_user.is_authenticated:
            abort(401)
        return f(*args, **kwargs)
    return wrapper

def params_required(*params):
    def wrapper(f):
        @wraps(f)
        def decorated_view(*args, **kwargs):
            for param in params:
                if param not in request.args:
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

@api_blueprint.before_request
@api_auth_required


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
            'expiry_date': item.expiry_date
            })

    resp = {
        'items': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/fridges/<id>', methods=['PUT'])
@params_required('quantity', 'unit_id', 'item_name', 'expiry_date')
def fridge_put(id):
    item = Fridge.query.get(id)
    item.quantity = int(request.args.get('quantity'))
    item.unit_id = int(request.args.get('unit_id'))
    item.item_name = request.args.get('item_name')
    item.expiry_date = datetime.strptime(request.args.get('expiry_date'))
    return Response('successfully executed', 200)

@api_blueprint.route('/fridges/<id>', methods=['DELETE'])
def fridge_delete(id):
    item = Fridge.query.get(id)
    item.delete()
    return Response('successfully executed', 200)

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
            'expiry_date': item.expiry_date
            })

    resp = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'items': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')

@api_blueprint.route('/fridges', methods=['POST'])
@params_required('quantity', 'unit_id', 'item_name', 'expiry_date')
def fridge_post():
    quantity = int(request.args.get('quantity'))
    unit_id = int(request.args.get('unit_id'))
    item_id = int(request.args.get('item_id'))
    item_name = request.args.get('item_name')
    expiry_date = datetime.strptime(request.args.get('expiry_date'))

    current_user.add_grocery(quantity=quantity, unit_id=unit_id, item_name=item_name, expiry_date=expiry_date)
    return Response('successfully created', 201)