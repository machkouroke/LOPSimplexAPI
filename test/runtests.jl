using LopShelve
using Test
using SQLite: DB
using DataFrames
using DBInterface

# Test of version 0.1.0
@testset "LopShelve.jl" begin
    test_Shelve = LopShelve.open!("test")
    @test test_Shelve.data == Dict()
    test_Shelve["hello"] = "world"
    @test test_Shelve["hello"] == "world"
    test_Shelve["complex_data"] = Dict(["a" => "1", "b" => "2"])
    @test test_Shelve["complex_data"] == Dict(["a" => "1", "b" => "2"])
    
    # After Insertion
    full_Shelve = LopShelve.open!("test")
    @test full_Shelve["hello"] == "world"
    @test full_Shelve["complex_data"] == Dict(["a" => "1", "b" => "2"])
    delete!(test_Shelve)
    delete!(full_Shelve)
end

# Test of version 0.1.1: add of composante verification
@testset "LopShelve.jl" begin
    config = LopShelve.open!("../config")
    config.data = Dict{Any, Any}("best_word" => "jeton", "dico" => "src/lop.com", "hello" => "world")
    @test config.data == Dict{Any, Any}("best_word" => "jeton", "dico" => "src/lop.com", "hello" => "world")
    @test ("best" in config) == false
    @test ("best_word" in config) == true
    delete!(config)
end

# Test of version 1.0.0: add of Sqlite Shelf 
@testset "ShelfSql.jl" begin
    filename = "../src/ShelfSql/test_data/card.s3db"
    table = "card"
    @test_throws ErrorException open!(filename, "places")
    db = open!(filename, table)
    for i in 1:3
        query = "select * from $table where id = $i"
        row = DBInterface.execute(DB(filename), query) |> DataFrame
        @test db[i][:number] == row.number
    end
end
@testset "ShelfSql.jl" begin
    filename = "../src/ShelfSql/test_data/chinook.db"
    table = "playlist_track"
    @test_throws ErrorException open!(filename, "places")
    db = open!(filename, table)
    @test length(db) == 8715
    @test ((1, 3) in db) == true
    @test ((10000, 10000) in db) == false
    @test length(keys(db)) == 8715
end