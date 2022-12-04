from src.Validator.Validator import Validator
from test.base import BaseTest


class TestValidator(BaseTest):
    def test_run(self):
        Validator.run(self.data)

    def test_data(self):
        print(type(self.data))
        self.assertEqual(type(self.data),dict)
