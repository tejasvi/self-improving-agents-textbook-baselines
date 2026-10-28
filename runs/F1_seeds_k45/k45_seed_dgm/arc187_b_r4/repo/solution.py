from itertools import product
import sys

MOD = 998244353

class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
    
    def find(self, x):
        if self.parent[x] != x:
            self.parent[x] = self.find(self.parent[x])
        return self.parent[x]
    
    def union(self, x, y):
        px, py = self.find(x), self.find(y)
        if px != py:
            self.parent[py] = px
    
    def count_components(self):
        return len(set(self.find(i) for i in range(len(self.parent))))
    
    def get_state(self):
        """Get canonical state of the union-find structure"""
        return tuple(sorted((i, self.find(i)) for i in range(len(self.parent))))

def compute_f(seq):
    """Compute f(A) - the number of connected components."""
    n = len(seq)
    uf = UnionFind(n)
    
    # Add edge between i and j if seq[i] <= seq[j]
    for i in range(n):
        for j in range(i + 1, n):
            if seq[i] <= seq[j]:
                uf.union(i, j)
    
    return uf.count_components()

def solve():
    line1 = input().split()
    N = int(line1[0])
    M = int(line1[1])
    
    B = list(map(int, input().split()))
    
    # Find positions of -1 and their count
    wildcard_positions = []
    for i, val in enumerate(B):
        if val == -1:
            wildcard_positions.append(i)
    
    q = len(wildcard_positions)
    
    # If no wildcards
    if q == 0:
        return compute_f(B) % MOD
    
    total_sum = 0
    
    # Generate all M^q combinations
    for replacement in product(range(1, M + 1), repeat=q):
        # Create a copy of B with replacements
        B_prime = B[:]
        for pos_idx, pos in enumerate(wildcard_positions):
            B_prime[pos] = replacement[pos_idx]
        
        # Compute f(B') and add to sum
        total_sum = (total_sum + compute_f(B_prime)) % MOD
    
    return total_sum

print(solve())
