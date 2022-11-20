
@testset "Two Variable" begin
    A = Float64[-1 1 1 0 0 11
        1 1 0 1 0 27
        2 5 0 0 1 90
        -4 -6 0 0 0 0]
    answer = simplex(A)
    true_answer = Dict{Any,Any}("x_1" => 15, "x_2" => 12)
    for (key, value) in true_answer
        @test answer[key] ≈ value
    end
end

@testset "Three Variable" begin
    A = Float64[1 2 3/2 1 0 0 12
        2/3 2/3 1 0 1 0 4.6
        1/2 1/3 1/2 0 0 1 2.4
        -11 -16 -15 0 0 0 0]
    B = Float64[4 1 1 1 0 0 30
        2 3 1 0 1 0 60
        1 2 3 0 0 1 40
        -3 -2 -1 0 0 0 0]
    data = Dict{Any,Any}("A" => A, "B" => B)
    true_answer = Dict{Any,Any}(
        "A" => Dict{Any,Any}("x_1" => 0.6, "x_2" => 5.1, "x_3" => 0.8),
        "B" => Dict{Any,Any}("x_1" => 3, "x_2" => 18)
    )
    for (name, array) in data
        ans = simplex(array)
        for (key, answer) in true_answer[name]
            @test ans[key] ≈ answer
        end
    end
end

"Done"