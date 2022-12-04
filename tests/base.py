import unittest

import yaml


class BaseTest(unittest.TestCase):
    def setUp(self) -> None:
        with open("views/test.yaml", "r") as stream:
            self.data = yaml.safe_load(stream)
