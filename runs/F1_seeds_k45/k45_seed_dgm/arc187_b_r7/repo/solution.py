import sys
from functools import lru_cache

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

def count_components(A):
    """Count connected components in the graph defined by A"""
    N = len(A)
    uf = UnionFind(N)
    
    for i in range(N):
        for j in range(i + 1, N):
            if A[i] <= A[j]:
                uf.union(i, j)
    
    return uf.count_components()

def solve():
    line1 = input().split()
    N = int(line1[0])
    M = int(line1[1])
    
    B = list(map(int, input().split()))
    
    # Find positions of -1
    minus_one_positions = [i for i, x in enumerate(B) if x == -1]
    q = len(minus_one_positions)
    
    # If no -1s, just compute f(B) and return it
    if q == 0:
        return count_components(B)
    
    # For -1 cases, use recursive enumeration with memoization
    memo = {}
    
    def get_components_memo(seq_tuple):
        """Get component count, using memo"""
        if seq_tuple not in memo:
            memo[seq_tuple] = count_components(list(seq_tuple))
        return memo[seq_tuple]
    
    # Generate all sequences and sum components
    total_sum = 0
    
    def generate_all_sequences(idx, current_seq):
        nonlocal total_sum
        
        if idx == q:
            # Compute components for this sequence
            seq_tuple = tuple(current_seq)
            comp_count = get_components_memo(seq_tuple)
            total_sum = (total_sum + comp_count) % MOD
            return
        
        pos = minus_one_positions[idx]
        for val in range(1, M + 1):
            current_seq[pos] = val
            generate_all_sequences(idx + 1, current_seq)
    
    generate_all_sequences(0, B)
    
    return total_sum

print(solve())
