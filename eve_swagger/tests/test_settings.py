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
        'type': 'dict',
        'schema': {
            'name': {
                'type': 'string',
                'required': True,
                'unique': True,
                'description': 'the last name of the person'
            },
            'job': {
                'type': 'string',
                'required': True,
                'unique': True,
                'description': 'the job of the person'
            }
        }
    },
    'disabled_resource': {
        'disable_documentation': True,
        'type': 'dict',
        'schema': {
            'field_1': {'type': 'string'}
        }
    },
    'dr_resource_1': {
        'type': 'dict',
        'item_lookup_field': 'copied_field_with_description',
        'schema': {
            'copied_field_with_description': {
                'type': 'string',
                'description': 'foobar copied_field',
                'data_relation': {
                    'resource': 'people',
                    'field': 'job'
                }
            },
        }
    },
    'dr_resource_2': {
        'type': 'dict',
        'item_lookup_field': 'copied_field_without_description',
        'schema': {
            'copied_field_without_description': {
                'type': 'string',
                'data_relation': {
                    'resource': 'people',
                    'field': 'job'
                }
            }
        }
    }
}
