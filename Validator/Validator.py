import re


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
        return all(x.isdigit() for x in {n, p})

    @staticmethod
    def validate_symbole_func(line: str):
        pattern = r'^(\d.?\d|->|,|\s)+$'
        return re.match(pattern, line)



