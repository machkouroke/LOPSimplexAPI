import unittest

from tests.views.base import BaseTestView


class TestSolver(BaseTestView):
    def setUp(self) -> None:
        self.init()

    def test_compute(self):

        res = self.client().post("/solve", json={"script": self.data})
        d = res.get_json()
        print(d)
        # self.assertEqual(d['success'],True)

if __name__ == "__main__":
    unittest.main()