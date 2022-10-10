A = Float64[1 2 3 1 0 0 90
15 21 30 0 1 0 1260
1 1 1 0 0 1 84
87 147 258 0 0 0 0]


function simplex(A; iter=2)
    B = deepcopy(A)
    incoming(x) = findmax(x[end, 1:end-1])[2]
    outgoing(x, pivot) = findmin(x[1:end-1, end] ./ x[1:end - 1, pivot])[2]
    cat(x, y) = [x;y]
    n, p = size(A)[1] - 1, size(A)[2] - 1
    in_base = ["e_$(i)" for i in 1:n]
    out_base = ["x_$(i)" for i in 1:p-n]
    
    for i in 1:iter
        @show in_base
        k = incoming(B)
        p = outgoing(B, k)
        in_base[p], out_base[k] = out_base[k], in_base[p]
        not_outgoing = setdiff(1:size(B)[1], [p])
        B[p, :] = B[p, :] ./ B[p, k]
        B[not_outgoing, :] = B[not_outgoing, :] - B[not_outgoing, k] * B[p, :]'
        println("Itération $(i)")
        display(B)

    end
end

simplex(A)