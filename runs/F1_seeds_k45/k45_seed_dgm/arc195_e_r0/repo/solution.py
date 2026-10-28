from itertools import product

MOD = 998244353

def read_input():
    N, Q = map(int, input().split())
    A = list(map(int, input().split()))
    queries = []
    for _ in range(Q):
        u, v = map(int, input().split())
        queries.append((u - 1, v - 1))  # Convert to 0-indexed
    return N, Q, A, queries

def get_all_parent_sequences(N):
    """Generate all possible parent sequences P_2, P_3, ..., P_N"""
    ranges = [range(1, i) for i in range(2, N + 1)]
    return product(*ranges)

def get_path(u, v, parents, A):
    """Get path from u to v and compute distance"""
    # Find all ancestors of u (going towards root 0)
    ancestors_u = {}
    dist_u = {}
    curr = u
    d = 0
    while curr not in ancestors_u:
        ancestors_u[curr] = True
        dist_u[curr] = d
        if curr == 0:
            break
        curr = parents[curr]
        d += A[curr - 1] if curr > 0 else 0
    
    # Find LCA and compute distance
    curr = v
    d = 0
    while curr not in ancestors_u:
        if curr == 0:
            break
        curr = parents[curr]
        d += A[curr - 1] if curr > 0 else 0
    
    lca = curr
    distance = dist_u[lca] + d
    return distance

def solve():
    N, Q, A, queries = read_input()
    
    # For each query
    for u, v in queries:
        total_distance = 0
        
        # Enumerate all parent sequences
        for parent_seq in get_all_parent_sequences(N):
            # parents[i] is parent of i (0-indexed)
            parents = [0] + [0] + list(parent_seq)  # parents[0] unused, parents[1] = 0
            
            distance = get_path(u, v, parents, A)
            total_distance = (total_distance + distance) % MOD
        
        print(total_distance)

if __name__ == "__main__":
    solve()
