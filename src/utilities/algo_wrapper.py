from src.computer.Simplex import py_simplex
from src.computer.init import main_jl
from src.utilities.utilities import to_vec
import numpy as np


def simplex_case_py(A: np.array, b: np.array, c: np.array, inequality: list,
                    type_simplexe: str = "max_base") -> tuple:
    """
    :param type_simplexe:
    :param A::Matrix{Float64}
    :param b::Vector{Float64}
    :param c::Vector{Float64}
    :param inequality::::Vector{String}
    :return:
    """
    matrix_float64 = main_jl.seval('Main.Matrix{Float64}')
    return py_simplex(main_jl.convert(matrix_float64, A), to_vec(b),
                        to_vec(c), inequality, type_simplexe)
