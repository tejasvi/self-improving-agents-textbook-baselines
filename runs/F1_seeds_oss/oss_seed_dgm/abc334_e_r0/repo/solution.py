import sys
sys.setrecursionlimit(1 << 25)

def solve():
    data = sys.stdin.buffer.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    grid = [list(next(it).decode()) for _ in range(H)]
    N = H * W
    parent = [-1] * N
    size = [1] * N
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(a, b):
        ra = find(a)
        rb = find(b)
        if ra == rb:
            return
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
    # initialize green cells
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#':
                idx = i * W + j
                parent[idx] = idx
    # union adjacent greens (right and down to avoid double)
    for i in range(H):
        for j in range(W):
            if grid[i][j] != '#':
                continue
            idx = i * W + j
            if i + 1 < H and grid[i+1][j] == '#':
                union(idx, (i+1) * W + j)
            if j + 1 < W and grid[i][j+1] == '#':
                union(idx, i * W + (j+1))
    # count components C
    C = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#':
                idx = i * W + j
                if parent[idx] == idx:
                    C += 1
    MOD = 998244353
    R = 0  # number of red cells
    sum_k = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                R += 1
                neigh = set()
                if i > 0 and grid[i-1][j] == '#':
                    neigh.add(find((i-1) * W + j))
                if i + 1 < H and grid[i+1][j] == '#':
                    neigh.add(find((i+1) * W + j))
                if j > 0 and grid[i][j-1] == '#':
                    neigh.add(find(i * W + (j-1)))
                if j + 1 < W and grid[i][j+1] == '#':
                    neigh.add(find(i * W + (j+1)))
                sum_k += len(neigh)
    # Compute expected value = (R*(C+1) - sum_k) / R
    # numerator modulo MOD
    numerator = (R * (C + 1) - sum_k) % MOD
    inv_R = pow(R, MOD-2, MOD)
    ans = numerator * inv_R % MOD
    print(ans)

if __name__ == "__main__":
    solve()
