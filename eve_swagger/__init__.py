from flask import Blueprint, jsonify, current_app as app


swagger = Blueprint('eve_swagger', __name__)


@swagger.route('/api-docs')
def index():
    return jsonify(
        {
            'info': {
                'title': 'API title',
                'description': 'API description',
                'version': '1.0.0'
            }
        }
    )
