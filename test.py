import yaml
import numpy as np
import re
# import pandas as pd

from julia import LOPSimplex, Main


def get_constraints(data):
    return [re.split(r"=|<=|>=", x) for x in data['constraints'].strip().split('\n')]


def get_A(data):
    eq = get_constraints(data)
    return np.array([sparse(l, data['n']) for l in [x[0] for x in eq]])


def get_B(data):
    eq = get_constraints(data)
    return np.array([int(x[-1]) for x in eq])


def get_C(data):
    return np.array(sparse(data['function'], data['n']) + [0])


def get_inequality(data):
    T = [re.split(r'\d|->|{|}|;',x) for x in data['constraints'].strip().split('\n')]
    inequality = [''.join(t).strip() for t in T]

    return inequality


def is_num(l):
    try:
        float(l)
        return True
    except Exception:
        return False


def sparse(line, n):
    if '{' in str(line) and '}' in str(line):
        Z = line.replace('{', '').replace('}', '')
        T = [l.split('->') for l in Z.split(';')]
        C = [float(t) for t in T[0]] * n if len(T[0]) == 1 else [0 for i in range(n)]

        for t in T:
            if len(t) != 1:
                for pos in t[-1].split(','):
                    C[int(pos) - 1] = float(t[0])
    else:
        C = [float(line)] * n if is_num(line) else [float(x) for x in line.split()]
    return C


def get_type(type_user, inequality):
    if type_user == 'max':
        if all(x == '<=' for x in inequality):
            tp = 'max-base'
        elif all(x == '>=' for x in inequality):
            tp = 'min-max'
        else:
            tp = 'max-mixed'
    else:
        if all(x == '>=' for x in inequality):
            tp = 'min-base'
        elif all(x == '<=' for x in inequality):
            tp = 'min-max'
        else:
            tp = 'min-mixed'
    return tp


def get_data():
    with open("test/test.yaml", "r") as stream:
        data = yaml.safe_load(stream)
    print(data)

    return get_A(data), get_B(data), get_C(data), get_inequality(data), data['type']


if __name__ == '__main__':
    A, B, C, ine, type_user = get_data()
    print(ine)
    # p = get_type(type_user, ine)
    # D = get_data()[4]
    # print(A, B, C, ine, type_user, p)
    # print('D', D)
    # simplex = Main.eval('LOPSimplex.simplex_case')
    # answer = simplex(A, B, C)
    # end = {'Simplex array': answer[0], 'in_base': answer[2]}
    # tables = {}
    # for k in sorted(answer[-1].keys()):
    #     tables[k] = answer[-1][k]
    # tables['end'] = end
    #
    # # print(tables[1])
    # # print(table)
    #
    # D = {}
    # for k in tables.keys():
    #     liste = []
    #     line = (tables[k]['in_base']) + ['Cj']
    #     for i in range(len(line)):
    #         liste.append([line[i]] + (tables[k]['Simplex array'].tolist())[i])
    #     D[k] = liste
    # print(D)
    #
    # print("Answer-1", answer[-1])
    # print("Answer1", answer[1])
    # print("Answer2", answer[2])
    # print("Answer3", answer[3])
