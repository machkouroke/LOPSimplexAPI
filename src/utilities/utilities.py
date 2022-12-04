from src.computer.init import main_jl


def to_vec(vec):
    return main_jl.vec(main_jl.convert(main_jl.seval("Vector{Float64}"), vec))


def get_type(type_user: str, inequality: list):
    if type_user == 'max':
        if all(x == '<=' for x in inequality):
            return 'max_base'
        elif all(x == '>=' for x in inequality):
            return 'max_min'
        else:
            return 'max_mixed'
    elif all(x == '>=' for x in inequality):
        return 'min_base'
    elif all(x == '<=' for x in inequality):
        return 'min_max'
    return 'min_mixed'




