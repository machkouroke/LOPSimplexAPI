using LOPSimplex: simplex,
    add_artificial_variable,
    add_slack_variable,
    add_artificial_variable,
    in_base_finder,
    variable_name_builder,
    simplex_matrix_builder,
    function_by_artificial,
    remove_artificial_column,
    replace_artificial_function_by_original
using Test

include("simplex.jl")
include("utilities.jl")