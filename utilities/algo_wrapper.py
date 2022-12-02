from computer.Simplex import simplex_case
from computer.init import main_jl


def simplex_case_py(A, b, c, inequality, type="max_base", verbose=False):
    """
    :param A::Matrix{Float64}
    :param b::Vector{Float64}
    :param c::Vector{Float64}
    :param inequality::::Vector{String}
    :return:
    """
    matrix_float64 = main_jl.seval('Main.Matrix{Float64}')
    vector_float64 = main_jl.seval('Main.Matrix{Float64}')
    return simplex_case(main_jl.convert(matrix_float64, A), main_jl.convert(vector_float64, b),
                        main_jl.convert(vector_float64, c))
