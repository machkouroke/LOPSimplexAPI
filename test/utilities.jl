
@testset "Add slack variable" begin
    @testset "All is less than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_slack_variable(A)
        true_answer = Float64[-1 1 1 1 0 0
            1 1 0 0 1 0
            2 5 0 0 0 1]
        @test answer == true_answer
    end
    @testset "All is greater than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_slack_variable(A, inequality=[">=" for i in 1:size(A)[1]])
        true_answer = Float64[-1 1 1 -1 0 0
            1 1 0 0 -1 0
            2 5 0 0 0 -1]
        @test answer == true_answer
    end
    @testset "All is equal to" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_slack_variable(A, inequality=["=" for i in 1:size(A)[1]])
        true_answer = Float64[-1 1 1 0 0 0
            1 1 0 0 0 0
            2 5 0 0 0 0]
        @test answer == true_answer
    end

    @testset "Mixed" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_slack_variable(A, inequality=["=", "<=", ">="])
        true_answer = Float64[-1 1 1 0 0 0
            1 1 0 0 1 0
            2 5 0 0 0 -1]

        @test answer == true_answer
    end
end

@testset "add_artificial_variable" begin
    @testset "All is less than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_artificial_variable(A)
        true_answer = Float64[-1 1 1 0 0 0
            1 1 0 0 0 0
            2 5 0 0 0 0]
        @test answer == true_answer
    end
    @testset "All is greater than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_artificial_variable(A, inequality=[">=" for i in 1:size(A)[1]])
        true_answer = Float64[-1 1 1 1 0 0
            1 1 0 0 1 0
            2 5 0 0 0 1]
        @test answer == true_answer
    end
    @testset "Mixed" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = add_artificial_variable(A, inequality=["=", "<=", ">="])
        true_answer = Float64[-1 1 1 1 0 0
            1 1 0 0 0 0
            2 5 0 0 0 1]
        @test answer == true_answer
    end
end

@testset "variable_name_builder" begin
    A = Float64[-1 1 1
            1 1 0
            2 5 0]
    answer = variable_name_builder(A)
    true_answer = ["x_1", "x_2", "x_3", "e_1", "e_2", "e_3", "a_1", "a_2", "a_3"]
    @test answer == true_answer
end

@testset "in_base_finder" begin
    @testset "All is less than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = in_base_finder(["<=" for i in 1:size(A)[1]])
        true_answer = ["e_1", "e_2", "e_3"]
        @test answer == true_answer
    end
end