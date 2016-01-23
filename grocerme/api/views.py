import json
from functools import wraps
from math import ceil

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

@api_blueprint.errorhandler(401)
def custom_401(error):
    return Response('access denied', 401, {'WWWAuthenticate':'Basic realm="Login Required"'})

@api_blueprint.before_request
@api_auth_required

@api_blueprint.route('/fridges')
def fridge_api():

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
            'name': item.detail.name
            })

    resp = {
        'page': page,
        'per_page': per_page,
        'total_pages': total_pages,
        'items': result
    }
    return Response(json.dumps(resp),  mimetype='application/json')
