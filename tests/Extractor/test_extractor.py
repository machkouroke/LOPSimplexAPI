from tests.base import BaseTest
from src.utilities.Extractor.Extractor import *


class TestExtractor(BaseTest):
    def test_extract_A(self):
        A = Extractor.get_A(self.data)
        print(A)
        # print(A[1][1]+1)
        # self.assertTrue((A == np.array([[10., 5.], [2., 3.], [1., 0.], [0., 1.]])).all())

    def test_extract_B(self):
        B = Extractor.get_B(self.data)
        self.assertTrue((B == np.array([200, 60, 12, 6])).all())

    def test_extract_C(self):
        C = Extractor.get_C(self.data)
        self.assertTrue((C == np.array([2000, 1000, 0])).all())
