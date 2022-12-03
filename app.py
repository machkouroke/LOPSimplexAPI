import itertools
from flask import Flask, request, abort, jsonify
from flask_cors import CORS
import yaml
import numpy as np
from utilities.algo_wrapper import simplex_case_py
from numpy import array
from error import setup_error_template
import os


def create_app():
    app = Flask(__name__)

    def get_constraints(data):
        return [x for x in data['constraints'].split('\n') if x]

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

    def get_A(data):
        eq = get_constraints(data)
        return np.array([sparse(l, data['n']) for l in [x.split('=')[0] for x in eq]])

    def get_B(data):
        eq = get_constraints(data)
        return np.array([int(x.split('=')[-1]) for x in eq])

    def get_C(data):
        return np.array(sparse(data['function'], data['n']) + [0])

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
            A, B, C, inequality, tp = get_data(request)

            answer = simplex_case_py(A, B, C, inequality)

            end = {'Simplex array': np.array(answer[0]), 'in_base': list(answer[2])}

            tables = {k: dict(answer[-1][k]) for k in sorted(dict(answer[-1]).keys())}
            tables['end'] = end
            D = []
            for k in tables:
                line = (list(tables[k]['in_base'])) + ['Cj']

                liste = [[line[i]] + (np.array(tables[k]['Simplex array']).tolist())[i] for i in range(len(line))]
                D.append(liste)
            return jsonify({
                'success': True,
                'allVariables': list(answer[3])+['B'],
                'data': D,
                'answer': dict(answer[1])
            })

        except Exception as e:
            # abort(500, f'{type(e)}: {e}')
            raise e

    @app.route('/')
    def hello_world():  # put application's code here
        return 'Simplex API v2.0'
    setup_error_template(app)

    CORS(app, resources={r"/*": {"origins": "*"}})

    @app.after_request
    def after_request(response):
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,true')
        response.headers.add('Access-Control-Allow-Methods', 'GET,PATCH,POST,DELETE,OPTIONS')
        return response

    return app


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app = create_app()
    app.run(debug=True, host='0.0.0.0', port=port)
