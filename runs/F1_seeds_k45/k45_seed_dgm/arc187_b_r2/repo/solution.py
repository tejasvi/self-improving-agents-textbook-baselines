import sys

MOD = 998244353

def read_input():
    line1 = input().split()
    N, M = int(line1[0]), int(line1[1])
    B = list(map(int, input().split()))
    return N, M, B

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
    
    def copy(self):
        new_uf = UnionFind(len(self.parent))
        new_uf.parent = self.parent[:]
        return new_uf

def solve():
    N, M, B = read_input()
    
    # Find positions with -1
    unknown_pos = [i for i in range(N) if B[i] == -1]
    q = len(unknown_pos)
    
    # Assignment for unknown positions
    values = [0] * q  # values[i] = value assigned to unknown_pos[i]
    
    cache = {}
    
    def uf_to_tuple(uf):
        """Convert UF to canonical tuple form"""
        mapping = {}
        next_id = 0
        result = []
        for i in range(len(uf.parent)):
            root = uf.find(i)
            if root not in mapping:
                mapping[root] = next_id
                next_id += 1
            result.append(mapping[root])
        return tuple(result)
    
    def tuple_to_uf(tup, n):
        """Convert tuple back to UF"""
        uf = UnionFind(n)
        for i in range(n):
            for j in range(i + 1, n):
                if tup[i] == tup[j]:
                    uf.union(i, j)
        return uf
    
    def dp(idx, uf_state):
        """
        idx: index into unknown_pos
        uf_state: canonical tuple representation of current union-find state
        Returns: (count, sum_of_components) for all ways forward
        """
        if idx == q:
            # All unknowns assigned, compute components
            uf = tuple_to_uf(uf_state, N)
            num_components = uf.count_components()
            return (1, num_components)
        
        key = (idx, uf_state)
        if key in cache:
            return cache[key]
        
        pos = unknown_pos[idx]
        uf = tuple_to_uf(uf_state, N)
        
        total_ways = 0
        total_sum = 0
        
        # Try each value 1 to M
        for val in range(1, M + 1):
            new_uf = uf.copy()
            
            # Add edges from position 'pos' with value 'val'
            
            # Edge to i < pos if B[i] <= val
            for i in range(pos):
                if B[i] != -1 and B[i] <= val:
                    new_uf.union(i, pos)
                elif B[i] == -1:
                    # B[i] is unknown, find which one it is
                    for k in range(idx):
                        if unknown_pos[k] == i:
                            # values[k] is already assigned
                            if values[k] <= val:
                                new_uf.union(i, pos)
                            break
            
            # Edge to j > pos if val <= B[j]
            for j in range(pos + 1, N):
                if B[j] != -1 and val <= B[j]:
                    new_uf.union(pos, j)
                # If B[j] == -1, we'll handle it when processing j
            
            new_uf_state = uf_to_tuple(new_uf)
            values[idx] = val
            ways, comp_sum = dp(idx + 1, new_uf_state)
            values[idx] = 0
            
            total_ways = (total_ways + ways) % MOD
            total_sum = (total_sum + comp_sum) % MOD
        
        cache[key] = (total_ways, total_sum)
        return (total_ways, total_sum)
    
    # Initialize UF with connections between known values
    initial_uf = UnionFind(N)
    for i in range(N):
        for j in range(i + 1, N):
            if B[i] != -1 and B[j] != -1 and B[i] <= B[j]:
                initial_uf.union(i, j)
    
    initial_state = uf_to_tuple(initial_uf)
    _, result = dp(0, initial_state)
    print(result)

solve()
