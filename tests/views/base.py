import unittest

import yaml
import os
from app import create_app


class BaseTestView(unittest.TestCase):

    def init(self):
        with open( "tests//views/test.yaml", "r") as stream:
            self.data = yaml.safe_load(stream)

        # print(self.data)
        self.app = create_app()
        self.client = self.app.test_client
