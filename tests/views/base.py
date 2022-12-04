import unittest

import yaml
import os
from app import create_app


class BaseTestView(unittest.TestCase):

    def init(self):
        with open( "test.yaml", "r") as stream:
            self.data = stream.read()

        # print(self.data)
        self.app = create_app()
        self.client = self.app.test_client
