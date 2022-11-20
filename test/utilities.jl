
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