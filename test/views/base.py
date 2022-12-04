import unittest

import yaml

from app import create_app


class BaseTestView(unittest.TestCase):

    def init(self):
        with open("../test.yaml", "r") as stream:
            self.data = yaml.safe_load(stream)

        # print(self.data)
        self.app = create_app()
        self.client = self.app.test_client

    def test_get_data(self):
        res = self.client().post("/data", json={"script": self.data})
        d = res.get_json()
        self.assertEqual(d['success'], True)
        print(d)

    def test_return(self):
        print(type(self.data))
