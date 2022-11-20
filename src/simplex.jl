function detect_solution(simplex_array, solution_set; maximum=true)
    variables = Dict()
    if maximum
        for (index, variable) in enumerate(solution_set)
            variables[variable] = simplex_array[index, end]
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
function simplex(A::Matrix{Float64}; in_base=Nothing, all_base=Nothing, verbose=false, maximum=true)
    n::Int64, m::Int64 = size(A)[1] - 1, size(A)[2] - 1
    if in_base == Nothing
        in_base = ["e_$(i)" for i in 1:n]
    end
    if all_base == Nothing
        out_base::Vector{String} = ["x_$(i)" for i in 1:m-n]
        all_base = vcat(out_base, in_base)
    end
    B::Matrix{Float64} = deepcopy(A)

    while any(i -> i < 0, B[end, 1:end-1])
        verbose && @show in_base
        verbose && display(B)
        k = incoming(B)
        p = outgoing(B, k)
        in_base[p] = all_base[k]

        not_outgoing = setdiff(1:size(B)[1], [p])
        B[p, :] = B[p, :] ./ B[p, k]
        B[not_outgoing, :] = B[not_outgoing, :] - B[not_outgoing, k] * B[p, :]'

    end
    verbose && println("Final solution")
    verbose && @show in_base
    verbose && display(B)
    return detect_solution(B, maximum ? in_base : all_base, maximum=maximum)
end

function simplex_case()
    
end

function main()
    A = Float64[1 1 1 1 0 0 340
        2 3 1 0 1 0 2400
        1 2 3 0 0 1 560
        -1100 -1400 -1500 0 0 0 0]

    # in_base::Vector{String} = ["e_$(i)" for i in 1:n]
    # out_base::Vector{String} = ["x_$(i)" for i in 1:m-n]
    # all_base::Vector{String} = vcat(out_base, in_base)
    println("***Start***")
    answer = simplex(A; verbose=true)
end

main()
