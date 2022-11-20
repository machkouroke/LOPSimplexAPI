
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
    @testset "All is greater than" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = in_base_finder([">=" for i in 1:size(A)[1]])
        true_answer = ["a_1", "a_2", "a_3"]
        @test answer == true_answer
    end
    @testset "All is equal to" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = in_base_finder(["=" for i in 1:size(A)[1]])
        true_answer = ["a_1", "a_2", "a_3"]
        @test answer == true_answer
    end
    @testset "Mixed" begin
        A = Float64[-1 1 1
            1 1 0
            2 5 0]
        answer = in_base_finder(["=", "<=", ">="])
        true_answer = ["a_1", "e_2", "a_3"]
        @test answer == true_answer
    end
end

@testset "simplex_matrix_builder" begin
    @testset "All is less than" begin
        A = Float64[1 2 3
            15 21 30
            1 1 1]
        b = Float64[90; 1260; 84]
        c = Float64[87; 147; 258; 0]
        answer = simplex_matrix_builder(A, b, c)


        true_answer = Float64[1 2 3 1 0 0 90
            15 21 30 0 1 0 1260
            1 1 1 0 0 1 84
            87 147 258 0 0 0 0]
        true_in_base = ["e_1", "e_2", "e_3"]
        true_variable_names = ["x_1", "x_2", "x_3", "e_1", "e_2", "e_3"]
        @test answer[1] == true_answer
        @test answer[2] == true_variable_names
        @test answer[3] == true_in_base
    end
    @testset "All is greater than" begin
        A = Float64[1 2 3
            15 21 30
            1 1 1]
        b = Float64[90; 1260; 84]
        c = Float64[87; 147; 258; 0]
        answer = simplex_matrix_builder(A, b, c, inequality=[">=" for i in 1:size(A)[1]])
        true_answer = Float64[1 2 3 -1 0 0 1 0 0 90
            15 21 30 0 -1 0 0 1 0 1260
            1 1 1 0 0 -1 0 0 1 84
            87 147 258 0 0 0 0 0 0 0]
        true_in_base = ["a_1", "a_2", "a_3"]
        true_variable_names = ["x_1", "x_2", "x_3", "e_1", "e_2", "e_3", "a_1", "a_2", "a_3"]
        @test answer[1] == true_answer
        @test answer[2] == true_variable_names
        @test answer[3] == true_in_base
    end
    @testset "All is equal to" begin
        A = Float64[1 2 3
            15 21 30
            1 1 1]
        b = Float64[90; 1260; 84]
        c = Float64[87; 147; 258; 0]
        answer = simplex_matrix_builder(A, b, c, inequality=["=" for i in 1:size(A)[1]])
        true_answer = Float64[1 2 3 1 0 0 90
            15 21 30 0 1 0 1260
            1 1 1 0 0 1 84
            87 147 258 0 0 0 0]
        true_in_base = ["a_1", "a_2", "a_3"]
        true_variable_names = ["x_1", "x_2", "x_3", "a_1", "a_2", "a_3"]
        @test answer[1] == true_answer
        @test answer[2] == true_variable_names
        @test answer[3] == true_in_base
    end

    @testset "Mixed" begin
        @testset "First Matrix" begin
            A = Float64[1 2 3
                15 21 30
                1 1 1]
            b = Float64[90; 1260; 84]
            c = Float64[87; 147; 258; 0]
            answer = simplex_matrix_builder(A, b, c, inequality=["=", "<=", ">="])
            true_answer = Float64[1 2 3 0 0 1 0 90
                15 21 30 1 0 0 0 1260
                1 1 1 0 -1 0 1 84
                87 147 258 0 0 0 0 0]
            true_in_base = ["a_1", "e_2", "a_3"]
            true_variable_names = ["x_1", "x_2", "x_3", "e_2", "e_3", "a_1", "a_3"]
            @test answer[1] == true_answer
            @test answer[2] == true_variable_names
            @test answer[3] == true_in_base
        end
        @testset "Second Matrix" begin
            A = Float64[10 5
                2 3
                1 0
                0 1]
            b = Float64[200; 60; 12; 6]
            c = Float64[2000; 1000; 0]
            answer = simplex_matrix_builder(A, b, c, inequality=["<=", "=", "<=", ">="])
            true_answer = Float64[10 5 1 0 0 0 0 200
                2 3 0 0 0 1 0 60
                1 0 0 1 0 0 0 12
                0 1 0 0 -1 0 1 6
                2000 1000 0 0 0 0 0 0]
            true_in_base = ["e_1", "a_2", "e_3", "a_4"]
            true_variable_names = ["x_1", "x_2", "e_1", "e_3", "e_4", "a_2", "a_4"]
            @test answer[1] == true_answer
            @test answer[2] == true_variable_names
            @test answer[3] == true_in_base
        end
    end
end

@testset "function_by_artificial" begin

    A = Float64[10 5 1 0 0 0 0 200
        2 3 0 0 0 1 0 60
        1 0 0 1 0 0 0 12
        0 1 0 0 -1 0 1 6
        2000 1000 0 0 0 0 0 0]

    in_base = ["e_1", "a_2", "e_3", "a_4"]
    variable_names = ["x_1", "x_2", "e_1", "e_3", "e_4", "a_2", "a_4"]
    answer = function_by_artificial(A, in_base, variable_names)
    true_answer = Float64[10 5 1 0 0 0 0 200
        2 3 0 0 0 1 0 60
        1 0 0 1 0 0 0 12
        0 1 0 0 -1 0 1 6
        2 4 0 0 -1 0 0 66]
    @test answer == true_answer
end