import os
import unittest

from app import create_app


class BaseTest(unittest.TestCase):

    def setUp(self) -> None:
        with open("test.yaml", "r") as stream:
            self.data = stream.read()
        # print(self.data)
        self.app = create_app()
        self.client = self.app.test_client

    def test_compute(self):
        res = self.client().post("/test", json={"script": self.data})
        d = res.get_json()
        print(d)
        # self.assertEqual(d['success'],True)

    def test_return(self):
        print(self.data)

