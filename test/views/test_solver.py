from test.views.base import BaseTestView


class TestSolver(BaseTestView):
    def setUp(self) -> None:
        self.init()
    def test_compute(self):
        res = self.client().post("/solve", json={"script": self.data})
        d = res.get_json()
        print(d)
        # self.assertEqual(d['success'],True)
