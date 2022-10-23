function detect_solution(simplex_array, solution_set; maximum=true)
    variables = Dict()
    if maximum
        for (index, variable) in enumerate(solution_set)
            if split(variable, "_")[1] == "x"
                variables[variable] = simplex_array[index, end]
            end
        end
    else
        for (index, variable) in enumerate(solution_set)
            if split(variable, "_")[1] == "e"
                variables["x_$(split(variable, "_")[2])"] = simplex_array[end, index]
            end
        end
    end

    return variables
end

"""
    incoming(x)
"""
function incoming(x)
    return findmin(x[end, 1:end-1])[2]
end
function outgoing(x, pivot)
    x_div_pivot = x[1:end-1, end] ./ x[1:end-1, pivot]
    x_div_pivot_positif = ifelse.(x_div_pivot .> 0, x_div_pivot, Inf)
    return findmin(x_div_pivot_positif)[2]
end

"""
    simplex(A::Matrix{Float64})
"""
function simplex(A::Matrix{Float64}; verbose=false, maximum=true)
    B::Matrix{Float64} = deepcopy(A)
    n::Int64, p::Int64 = size(B)[1] - 1, size(B)[2] - 1
    in_base::Vector{String} = ["e_$(i)" for i in 1:n]
    out_base::Vector{String} = ["x_$(i)" for i in 1:p-n]
    all_base::Vector{String} = vcat(out_base, in_base)
    while any(i -> i < 0, B[end, 1:end-1])
        k = incoming(B)
        p = outgoing(B, k)
        in_base[p] = all_base[k]
        verbose && @show in_base

        not_outgoing = setdiff(1:size(B)[1], [p])
        B[p, :] = B[p, :] ./ B[p, k]
        B[not_outgoing, :] = B[not_outgoing, :] - B[not_outgoing, k] * B[p, :]'
        verbose && display(B)
    end
    return detect_solution(B, maximum ? in_base : all_base, maximum=maximum)
end

function main()
    A = Float64[1 3 3 1 0 100
        2 2 1 0 1 100
        -60 -120 -90 0 0 0]
    answer = simplex(A; verbose=true, maximum=false)
end

main()
