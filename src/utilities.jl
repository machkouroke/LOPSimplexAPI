using Match
function add_slack_variable(A::Matrix{Float64}; inequality=["<=" for i in 1:size(A)[1]])
    n::Int64, m::Int64 = size(A)[1], size(A)[2]
    slack_variable::Matrix{Float64} = zeros(n, n)
    for (index, inequality) in enumerate(inequality)
        slack_variable[index, index] = @match inequality begin
            "<=" => 1
            ">=" => -1
            "=" => 0
        end
    end
    return hcat(A, slack_variable)
end

function add_artificial_variable(A::Matrix{Float64}; inequality=["<=" for i in 1:size(A)[1]])
    n::Int64, m::Int64 = size(A)[1], size(A)[2]
    slack_variable::Matrix{Float64} = zeros(n, n)
    for (index, inequality) in enumerate(inequality)
        slack_variable[index, index] = inequality in ["=", ">="]
    end
    return hcat(A, slack_variable)
end


function variable_name_builder(A::Matrix{Float64})
    variable_name::Vector{String} = ["x_$i" for i in 1:size(A)[2]]
    slack_variable_name::Vector{String} = ["e_$i" for i in 1:size(A)[1]]
    artificial_variable::Vector{String} = ["a_$i" for i in 1:size(A)[1]]
    return [variable_name; slack_variable_name; artificial_variable]
end

function in_base_finder(inequality)
    in_base::Vector{String} = []
    for (index, inequality) in enumerate(inequality)
        variable = @match inequality begin
            "<=" => "e_$index"
            ">=" => "a_$index"
            "=" => "e_$index"
        end
        push!(in_base, variable)
    end
    return in_base
end

function simplex_matrix_builder(A::Matrix{Float64}, b::Vector{Float64}, c::Vector{Float64}; inequality=["<=" for i in 1:size(A)[1]])
    n::Int64, m::Int64 = size(A)[1], size(A)[2]
    variable_name = variable_name_builder(A)
    in_base = in_base_finder(A, inequality=inequality)
    A = A |>
        x -> add_slack_variable(x; inequality=inequality) |>
             x -> add_artificial_variable(x; inequality=inequality) |>
                  x -> x[:, findall(x -> x != 0, sum(x, dims=1)[1, :])] # remove zero columns

    c = vcat(c[1:end-1], zeros(n), c[end])
    b = vcat(b, zeros(n))
    simplex_array = vcat(hcat(A, b), c)
    return simplex_array, variable_name, in_base
end