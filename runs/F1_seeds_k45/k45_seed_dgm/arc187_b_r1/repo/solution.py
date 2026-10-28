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
            return False
        if self.rank[px] < self.rank[py]:
            px, py = py, px
        self.parent[py] = px
        if self.rank[px] == self.rank[py]:
            self.rank[px] += 1
        return True
    
    def count_components(self):
        return len(set(self.find(i) for i in range(len(self.parent))))

def compute_f(sequence):
    """Compute f(A) for a given sequence"""
    n = len(sequence)
    uf = UnionFind(n)
    
    # Draw edges: for i < j, if A[i] <= A[j], connect i and j
    for i in range(n):
        for j in range(i + 1, n):
            if sequence[i] <= sequence[j]:
                uf.union(i, j)
    
    return uf.count_components()

def solve():
    # Read input
    n, m = map(int, input().split())
    b = list(map(int, input().split()))
    
    # Find positions of -1 and their count
    unknown_positions = [i for i, x in enumerate(b) if x == -1]
    q = len(unknown_positions)
    
    # If no unknowns, just compute f(b)
    if q == 0:
        result = compute_f(b)
        print(result % MOD)
        return
    
    # Generate all possible replacements and sum f values
    total = 0
    
    # Generate all combinations of 1 to m for each unknown position
    for replacement in product(range(1, m + 1), repeat=q):
        # Create the sequence with replacements
        sequence = b.copy()
        for pos_idx, value in enumerate(replacement):
            sequence[unknown_positions[pos_idx]] = value
        
        # Compute f for this sequence
        f_val = compute_f(sequence)
        total += f_val
        total %= MOD
    
    print(total)

if __name__ == "__main__":
    solve()
