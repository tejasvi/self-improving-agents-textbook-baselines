import sys
sys.setrecursionlimit(1 << 25)

def solve():
    import sys
    MOD = 998244353
    data = sys.stdin.read().split()
    if not data:
        return
    it = iter(data)
    H = int(next(it))
    W = int(next(it))
    grid = [list(next(it).strip()) for _ in range(H)]
    N_red = 0
    # DSU for green cells (#)
    size = H * W
    parent = list(range(size))
    rank = [0] * size
    def find(x):
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x
    def union(x, y):
        x = find(x)
        y = find(y)
        if x == y:
            return
        if rank[x] < rank[y]:
            x, y = y, x
        parent[y] = x
        if rank[x] == rank[y]:
            rank[x] += 1
    # Index conversion
    def idx(i, j):
        return i * W + j
    # First, union adjacent green cells
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#':
                if i + 1 < H and grid[i+1][j] == '#':
                    union(idx(i,j), idx(i+1,j))
                if j + 1 < W and grid[i][j+1] == '#':
                    union(idx(i,j), idx(i,j+1))
    # Determine component roots for green cells
    root_set = set()
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '#':
                root_set.add(find(idx(i,j)))
    C0 = len(root_set)
    # Count red cells and sum of distinct neighbor component counts
    total_t = 0
    for i in range(H):
        for j in range(W):
            if grid[i][j] == '.':
                N_red += 1
                # collect distinct neighbor roots
                neigh = []
                # up
                if i > 0 and grid[i-1][j] == '#':
                    neigh.append(find(idx(i-1,j)))
                # down
                if i + 1 < H and grid[i+1][j] == '#':
                    neigh.append(find(idx(i+1,j)))
                # left
                if j > 0 and grid[i][j-1] == '#':
                    neigh.append(find(idx(i,j-1)))
                # right
                if j + 1 < W and grid[i][j+1] == '#':
                    neigh.append(find(idx(i,j+1)))
                # deduplicate small list
                if not neigh:
                    t = 0
                else:
                    # at most 4 elements
                    uniq = []
                    for r in neigh:
                        if r not in uniq:
                            uniq.append(r)
                    t = len(uniq)
                total_t += t
    # Compute answer: (C0 + 1) - total_t / N_red
    N = N_red
    numerator = (C0 + 1) * N - total_t
    numerator %= MOD
    invN = pow(N, MOD-2, MOD)
    ans = numerator * invN % MOD
    print(ans)

if __name__ == "__main__":
    solve()
