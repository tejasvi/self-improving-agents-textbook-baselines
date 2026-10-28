from itertools import product

MOD = 998244353

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.rank = [0] * n
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px == py:
            return
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
    
    def count_components(self):
        return len(set(self.find(i) for i in range(len(self.parent))))

def compute_f(A):
    """Compute the number of connected components for sequence A."""
    n = len(A)
    uf = UnionFind(n)
    
    # For each pair (i, j) where i < j, if A[i] <= A[j], add an edge
    for i in range(n):
        for j in range(i + 1, n):
            if A[i] <= A[j]:
                uf.union(i, j)
    
    return uf.count_components()

def solve():
    line1 = input().split()
    N = int(line1[0])
    M = int(line1[1])
    
    B = list(map(int, input().split()))
    
    # Find positions of -1s
    wildcard_positions = [i for i, val in enumerate(B) if val == -1]
    num_wildcards = len(wildcard_positions)
    
    total = 0
    
    # Generate all possible replacements
    if num_wildcards == 0:
        # No wildcards, just compute f(B)
        total = compute_f(B)
    else:
        # Iterate through all combinations
        for replacement in product(range(1, M + 1), repeat=num_wildcards):
            # Create a copy of B and fill in the wildcards
            B_prime = B[:]
            for pos, val in zip(wildcard_positions, replacement):
                B_prime[pos] = val
            
            # Compute f(B_prime)
            f_val = compute_f(B_prime)
            total = (total + f_val) % MOD
    
    print(total)

solve()
