MONGO_HOST = 'localhost'
MONGO_PORT = 27017
MONGO_USERNAME = 'test_user'
MONGO_PASSWORD = 'test_pw'
MONGO_DBNAME = 'eve_swagger_test'

TRANSPARENT_SCHEMA_RULES = True
RESOURCE_METHODS = ['GET', 'POST', 'DELETE']
ITEM_METHODS = ['GET', 'PATCH', 'PUT', 'DELETE']

DOMAIN = {
    'people': {
        'description': 'the people resource',
        'schema': {
            'name': {
                'type': 'string',
                'required': True,
                'unique': True,
                'description': 'the last name of the person'
            },
        }
    }
}
