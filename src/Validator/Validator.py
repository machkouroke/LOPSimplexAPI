import re

from src.Exception.ValidationException import ValidationException


class Validator:
    @staticmethod
    def validate_key(data: dict):
        valid_keys = {'n', 'p', 'type', 'constraints', 'function'}
        return not (valid_keys - set(data.keys()))

    @staticmethod
    def validate_operation_type(data: str):
        return data in {'min', 'max'}

    @staticmethod
    def validate_n_p(n, p):
        return all(str(x).isdigit() for x in {n, p})

    @staticmethod
    def validate_symbole_func(line: str):
        pattern = r'^(\d*.?\d|->|,|\s)+$'
        return re.match(pattern, line)

    @staticmethod
    def run(data: dict) -> None:
        lines = [data['function']] + [
            re.split(r"=|<=|>=", x)[0] for x in data['constraints'].strip().split('\n')]
        validators = {'valid_key': {'function': Validator.validate_key, 'argument': [data],
                                    'msg': 'Veuillez verifier le nom de vos clés'},
                      'valid_type': {'function': Validator.validate_operation_type,
                                     'argument': [data['type']],
                                     'msg': 'Veuillez saisir min ou max pour le type'},
                      'valid_n_p': {'function': Validator.validate_n_p, 'argument': [data['n'], data['p']],
                                    'msg': 'Veuillez saisir des entiers pour n et p'}
                      }
        for validator, operation in validators.items():
            if not operation['function'](*operation['argument']):
                raise ValidationException(operation['msg'])

        if not (all(Validator.validate_symbole_func(line) for line in lines)):
            raise ValidationException('Syntaxe de fonctions ou de contraintes incorrectes')
