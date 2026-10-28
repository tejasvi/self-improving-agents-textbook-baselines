#!/usr/bin/env python3

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

def compute_f(sequence):
    """Compute f(A) - number of connected components"""
    n = len(sequence)
    uf = UnionFind(n)
    
    # For every pair (i, j) where i < j, if A_i <= A_j, draw an edge
    for i in range(n):
        for j in range(i + 1, n):
            if sequence[i] <= sequence[j]:
                uf.union(i, j)
    
    return uf.count_components()

def solve():
    # Read input
    n, m = map(int, input().split())
    b = list(map(int, input().split()))
    
    # Find positions of -1 and count them
    unknown_positions = []
    for i in range(n):
        if b[i] == -1:
            unknown_positions.append(i)
    
    q = len(unknown_positions)
    
    # If no -1s, just compute f directly
    if q == 0:
        print(compute_f(b))
        return
    
    total_sum = 0
    
    # Iterate through all M^q possibilities
    # We can think of this as iterating through all base-M numbers from 0 to M^q - 1
    for mask in range(m ** q):
        # Create a copy of b
        sequence = b.copy()
        
        # Fill in the unknowns
        temp = mask
        for pos_idx in range(q):
            pos = unknown_positions[pos_idx]
            value = (temp % m) + 1  # Values range from 1 to M
            sequence[pos] = value
            temp //= m
        
        # Compute f for this sequence
        f_value = compute_f(sequence)
        total_sum = (total_sum + f_value) % MOD
    
    print(total_sum)

if __name__ == "__main__":
    solve()
