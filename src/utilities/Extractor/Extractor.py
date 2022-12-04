import re

import numpy as np
from src.Exception.ValidationException import ValidationException


class Extractor:

    @staticmethod
    def is_unique(l):
        try:
            float(l)
            return True
        except Exception:
            return False

    @staticmethod
    def get_constraints(data) -> list:
        return [re.split(r"=|<=|>=", x) for x in data['constraints'].strip().split('\n')]

    @staticmethod
    def extract(line, n) -> list:
        """
        Extrait les coefficients sur chaque ligne
        :param line : la ligne dont on veut extraire les coeffs(fonction objective et ligne du A)
        :param n : le nombre de variables
        :return : la liste des coeffs
        """
        try:
            if '->' in str(line):
                # Z = line.replace('{', '').replace('}', '')
                T = [l.split('->') for l in line.split()]
                Z = [float(t) for t in T[0]] * n if len(T[0]) == 1 else [0 for _ in range(n)]

                for t in T:
                    if len(t) != 1:
                        for pos in t[-1].split(','):
                            Z[int(pos) - 1] = float(t[0])
            else:
                Z = [float(line)] * n if Extractor.is_unique(line) else [float(x) for x in line.split()]
            return Z
        except Exception as e:
            raise ValidationException(e)

    @staticmethod
    def get_A(data) -> np.array:
        eq = Extractor.get_constraints(data)
        return np.array([Extractor.extract(l, data['n']) for l in [x[0] for x in eq]])

    @staticmethod
    def get_B(data) -> np.array:
        eq = Extractor.get_constraints(data)
        return np.array([int(x[-1]) for x in eq])

    @staticmethod
    def get_C(data) -> np.array:
        return np.array(Extractor.extract(data['function'], data['n']) + [0])

    @staticmethod
    def get_inequality(data) -> list:
        T = [re.split(r'\d|->|{|}|;', x) for x in data['constraints'].strip().split('\n')]
        return [''.join(t).strip() for t in T]

