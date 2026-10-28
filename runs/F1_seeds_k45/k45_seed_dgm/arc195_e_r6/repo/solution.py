from itertools import product
from collections import deque

MOD = 998244353

def solve():
    N, Q = map(int, input().split())
    A = [0, 0] + list(map(int, input().split()))  # A[i] for i >= 2
    
    # Generate all possible P sequences
    def generate_all_P():
        ranges = [range(1, i) for i in range(2, N+1)]
        for p_values in product(*ranges):
            P = [0, 0] + list(p_values)  # P[i] for i >= 2
            yield P
    
    def find_distance(P, u, v):
        # Build adjacency list for the tree
        tree = [[] for _ in range(N+1)]
        for i in range(2, N+1):
            tree[P[i]].append((i, A[i]))
            tree[i].append((P[i], A[i]))
        
        # BFS to find distance from u to v
        queue = deque([(u, 0)])
        visited = set([u])
        
        while queue:
            node, dist = queue.popleft()
            if node == v:
                return dist
            for neighbor, weight in tree[node]:
                if neighbor not in visited:
                    visited.add(neighbor)
                    queue.append((neighbor, dist + weight))
        
        return 0
    
    for _ in range(Q):
        u, v = map(int, input().split())
        total = 0
        for P in generate_all_P():
            dist = find_distance(P, u, v)
            total = (total + dist) % MOD
        print(total)

solve()
