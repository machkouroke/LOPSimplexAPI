ENV["PYTHON"] = "/usr/local/bin/python"
using Pkg
println("Add of PyCall")
Pkg.add("PyCall")
println("Add of LOPSimplex")
Pkg.add(url="https://github.com/machkouroke/LOPSimplex.jl.git")