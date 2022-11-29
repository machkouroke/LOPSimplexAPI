from flask import Flask, request, abort, jsonify
import yaml
import numpy as np
from julia import LOPSimplex, Main

app = Flask(__name__)


def get_constraints(data):
    return np.array([[float(y) for y in x.strip().split()] for x in data['constraints'].split('\n') if x])


def get_A(data):
    eq = get_constraints(data)
    return eq[:, :-1]


def get_B(data):
    eq = get_constraints(data)
    return eq[:, -1]


def get_C(data):
    C = [float(x) for x in data['function'].split() if x]
    if len(C) == data['n']:
        C.append(0)
    return np.array(C)


def get_inequality(data):
    inequality = ['<=' for i in range(data['p'])]
    others = ['=', '>=']
    for t in [l.split('->') for l in data['inequality'].replace('{', '').replace('}', '').split(',')]:
        for a in others:
            if a in t:
                for pos in t[-1].split():
                    inequality[int(pos) - 1] = a
    return inequality


def validation_data(data):
    pass


def get_type(type_user, inequality):

    if type_user == 'max':
        if all(x == '<=' for x in inequality):
            tp = 'max_base'
        elif all(x == '>=' for x in inequality):
            tp = 'min_max'
        else:
            tp = 'max_mixed'
    else:
        if all(x == '>=' for x in inequality):
            tp = 'min_base'
        elif all(x == '<=' for x in inequality):
            tp = 'min_max'
        else:
            tp = 'min_mixed'
    return tp


def get_solution():
    A, B, C, inequality = get_data()
    simplex = Main.eval('LOPSimplex.simplex_case')
    answer = simplex(A, B, C)


@app.route('/test', methods=['POST'])
def get_data():
    data = request.form['data']
    data = yaml.safe_load(data)
    return get_A(data), get_B(data), get_C(data), get_inequality(data)


@app.route('/')
def hello_world():  # put application's code here
    return 'hello.py'


if __name__ == '__main__':
    app.run()
