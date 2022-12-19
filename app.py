import yaml
from flask import Flask, request, jsonify, abort
from flask_cors import CORS
import numpy as np
from src.Error.error import setup_error_template
import os

from src.Exception.ValidationException import ValidationException
from src.utilities.algo_wrapper import simplex_case_py
from src.Validator.Validator import Validator
from src.utilities.Extractor.Extractor import Extractor
from src.utilities.utilities import get_type


def create_app():
    app = Flask(__name__)

    def get_data(req) -> tuple[np.array, np.array, np.array, list, str]:
        """
        Recuperer les parametres de la fonctions de Simplex
        :param req: La requete
        :return:
        """
        data: str = req.get_json()['script']
        print(data)
        data: dict = yaml.safe_load(data)
        Validator.run(data)
        return Extractor.get_A(data), \
               Extractor.get_B(data), \
               Extractor.get_C(data), \
               Extractor.get_inequality(data), \
               data['type']

    @app.route('/solve', methods=['POST'])
    def solver():
        try:

            A, B, C, inequality, type_user = get_data(request)
            type_simplex = get_type(type_user, inequality)
            answer = simplex_case_py(A, B, C, inequality, type_simplex)

            final_tab = {'Simplex array': np.array(answer[0]), 'in_base': list(answer[2])}

            tables = {k: dict(answer[-1][k]) for k in sorted(dict(answer[-1]).keys())}
            tables['end'] = final_tab
            D = []
            for k in tables:
                line = (list(tables[k]['in_base'])) + ['Cj']

                liste = [[line[i]] + (np.array(tables[k]['Simplex array']).tolist())[i] for i in range(len(line))]
                D.append(liste)
            return jsonify({
                'success': True,
                'allVariables': list(answer[3]) + ['B'],
                'data': D,
                'answer': dict(answer[1])
            })
        except ValidationException as e:
            abort(400, f'{e}')
        except Exception as e:
            # abort(500, f'{type(e)}: {e}')
            raise e

    @app.route('/')
    def hello_world(): 
        return 'Simplex API v6.0'

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
