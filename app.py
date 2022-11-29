from flask import Flask, request
import yaml
import numpy as np

app = Flask(__name__)


def get_constraints(data):
    return np.array([[float(y) for y in x.strip().split()] for x in data['constraints'].split('\n') if x])


def get_A(data):
    eq = get_constraints(data)
    return eq[:, :-1]


def get_B(data):
    eq = get_constraints(data)
    return eq[:, -1]


@app.route('/test', methods=['POST'])
def get_data():
    data = request.form['data']
    data = yaml.safe_load(data)
    eq = np.array([[float(y) for y in x.strip().split()] for x in data['constraints'].split('\n') if x])
    A = eq[:, :-1]
    B = eq[:, -1]
    # la matrice de la fonction cout
    C = [float(x) for x in data['function'].split() if x]
    if len(C) == data['n']:
        C.append(0)
    C = np.array(C)
    # les inegalites
    inequality = ['<=' for i in range(data['p'])]
    others = ['=', '>=']
    for t in data['inequality'].replace('{', '').replace('}', ''):
        for a in others:
            if a in t:
                for pos in t[-1].split():
                    inequality[int(pos) - 1] = a
    return A, B, C, inequality


@app.route('/')
def hello_world():  # put application's code here
    return 'hello.py'


if __name__ == '__main__':
    app.run()
