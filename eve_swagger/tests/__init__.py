import os
import json
import unittest

import eve
import eve_swagger
from pymongo import MongoClient
from eve_swagger.tests.test_settings import (
    MONGO_HOST,
    MONGO_PORT,
    MONGO_USERNAME,
    MONGO_PASSWORD,
    MONGO_DBNAME,
)


class TestBase(unittest.TestCase):
    def setUp(self, settings=None):
        self.this_directory = os.path.dirname(os.path.realpath(__file__))
        if settings is None:
            settings = os.path.join(self.this_directory, "test_settings.py")

        self.setupDB()

        self.settings = settings
        self.app = eve.Eve(settings=self.settings)

        swagger = eve_swagger.get_swagger_blueprint()

        self.app.register_blueprint(swagger)
        self.app.config["SWAGGER_INFO"] = {
            "title": "Test eve-swagger",
            "version": "0.0.1",
        }

        self.test_client = self.app.test_client()
        self.domain = self.app.config["DOMAIN"]

        self.swagger_doc = self.get_swagger_doc()

    def tearDown(self):
        del self.app
        self.dropDB()

    def setupDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        if MONGO_USERNAME:
            self.connection[MONGO_DBNAME].command(
                "createUser", MONGO_USERNAME, pwd=MONGO_PASSWORD, roles=[]
            )

    def dropDB(self):
        self.connection = MongoClient(MONGO_HOST, MONGO_PORT)
        self.connection.drop_database(MONGO_DBNAME)
        if MONGO_USERNAME:
            self.connection[MONGO_DBNAME].command("dropUser", MONGO_USERNAME)
        self.connection.close()

    def get_swagger_doc(self):
        r = self.test_client.get("/api-docs")
        return self.parse_response(r)

    def parse_response(self, r):
        try:
            v = json.loads(r.get_data().decode("utf-8"))
        except ValueError:
            v = None
        return v
