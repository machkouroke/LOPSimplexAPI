from computer.init import jl
def to_vec(vec):
    return jl.vec(jl.convert(jl.seval("Vector{Float64}"), vec))

