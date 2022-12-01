import itertools
from flask import Flask, request, abort, jsonify
import yaml
import numpy as np
from computer.Simplex import simplex_case
from numpy import array
from error import setup_error_template

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
    inequality = ['<=' for _ in range(data['p'])]
    others = ['=', '>=']
    for t, a in itertools.product(
            [l.split('->') for l in data['inequality'].replace('{', '').replace('}', '').split(',')], others):
        if a in t:
            for pos in t[-1].split():
                inequality[int(pos) - 1] = a
    return inequality


def validate_nb(n):
    return str(n).isdigit()


# def validate_cons(cons):
#     return all(x for x in cons)


def val_cons_nb(A: array, p):
    return A.shape[0] == p


def val_var_nb(A: array, n):
    return A.shape[1] == n


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
    elif all(x == '>=' for x in inequality):
        tp = 'min_base'
    elif all(x == '<=' for x in inequality):
        tp = 'min_max'
    else:
        tp = 'min_mixed'
    return tp


def get_data(request):
    print(request.get_json())
    data = request.get_json()['script']
    data = yaml.safe_load(data)
    A = get_A(data)
    if val_cons_nb(A, data['p']) and val_var_nb(A, data['n']):
        return A, get_B(data), get_C(data), get_inequality(data), data['type']


@app.route('/test', methods=['POST'])
def get_solution():
    try:
        print(request.get_json())
        A, B, C, inequality, tp = get_data(request)
        simplex = simplex_case
        answer = simplex(A, B, C)
        end = {'Simplex array': answer[0], 'in_base': answer[2]}
        tables = {k: answer[-1][k] for k in sorted(answer[-1].keys())}
        tables['end'] = end

        D = {}
        for k in tables:
            line = (tables[k]['in_base']) + ['Cj']
            liste = [[line[i]] + (tables[1]['Simplex array'].tolist())[i] for i in range(len(line))]

            D[k] = liste

        return jsonify({
            'success': True,
            'allVariables': answer[3],
            'data': D,
            'answer': answer[1]
        })
    except Exception as e:
        abort(500, f'{type(e)}: {e}')


@app.route('/')
def hello_world():  # put application's code here
    return 'hello.py'


def create_app():
    setup_error_template(app)
    return app


if __name__ == '__main__':
    app.run(debug=True)
