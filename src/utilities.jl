using Match
function add_slack_variable(A::Matrix{Float64}; inequality=["<=" for i in 1:size(A)[1]])
    n::Int64, m::Int64 = size(A)[1], size(A)[2]
    slack_variable::Matrix{Float64} = zeros(n, n)
    for (index, inequality) in enumerate(inequality)
        slack_variable[index, index] =  @match inequality begin
            "<=" => 1
            ">=" => -1
            "=" => 0
        end
    end
    return hcat(A, slack_variable)
end
