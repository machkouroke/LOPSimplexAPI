import yaml
import numpy as np
# import pandas as pd

from julia import LOPSimplex, Main


def get_constraints(data):
    return [x for x in data['constraints'].split('\n') if x]


def get_A(data):
    eq = get_constraints(data)

    return np.array([sparse(l, data['n']) for l in [x.split('=')[0] for x in eq]])


def get_B(data):
    eq = get_constraints(data)
    return np.array([int(x.split('=')[-1]) for x in eq])


def get_C(data):
    C = [float(x) for x in data['function'].split() if x]
    if len(C) == data['n']:
        C.append(0)
    return np.array(C)


def get_inequality(data):
    inequality = ['<=' for i in range(data['p'])]
    others = ['=', '>=']

    for t in [l.split('->') for l in data['inequality'].replace('{', '').replace('}', '').split(';')]:
        for a in others:
            if a in t:
                for pos in t[-1].split(','):
                    inequality[int(pos) - 1] = a
    return inequality


def sparse(line, n):
    if '{' in line and '}' in line:
        Z = line.replace('{', '').replace('}', '')
        C = [0 for i in range(n)]
        T = [l.split('->') for l in Z.split(';')]
        for t in T:
            for pos in t[-1].split(','):
                C[int(pos) - 1] = int(t[0])
    else:
        C = [int(x) for x in line.split()]
    return np.array(C)


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

    C = get_C(data) if data['mode'] == 'full' else sparse(data['function'], data['n'])
    return get_A(data), get_B(data), C, get_inequality(data), data['type']


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
