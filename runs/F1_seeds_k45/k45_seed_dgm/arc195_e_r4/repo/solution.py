from itertools import product

MOD = 998244353

def find_distance(u, v, parent, A, N):
    """Find distance from u to v in tree with given parent assignments"""
    
    # Find path from u to root
    path_u = []
    curr = u
    while curr != 0:
        path_u.append(curr)
        curr = parent[curr] if curr > 0 and curr < len(parent) else 0
    
    # Find path from v to root
    path_v = []
    curr = v
    while curr != 0:
        path_v.append(curr)
        curr = parent[curr] if curr > 0 and curr < len(parent) else 0
    
    # Find LCA
    ancestors_u = set(path_u)
    lca = None
    for node in path_v:
        if node in ancestors_u:
            lca = node
            break
    
    # Distance from u to LCA
    dist = 0
    curr = u
    while curr != lca:
        dist = (dist + A[curr]) % MOD
        curr = parent[curr]
    
    # Distance from v to LCA
    curr = v
    while curr != lca:
        dist = (dist + A[curr]) % MOD
        curr = parent[curr]
    
    return dist

def main():
    N, Q = map(int, input().split())
    A = [0, 0] + list(map(int, input().split()))  # A[2], A[3], ..., A[N]
    
    # Generate all valid parent assignments
    def generate_parent_assignments():
        ranges = [range(1, i) for i in range(2, N + 1)]
        for assignment in product(*ranges):
            yield assignment
    
    for _ in range(Q):
        u, v = map(int, input().split())
        
        total_distance = 0
        
        for parent_assignment in generate_parent_assignments():
            # parent_assignment is (P_2, P_3, ..., P_N)
            parent = [0, 0] + list(parent_assignment)  # parent[i] is parent of i
            
            # Build tree and find path from u to v
            distance = find_distance(u, v, parent, A, N)
            total_distance = (total_distance + distance) % MOD
        
        print(total_distance)

if __name__ == "__main__":
    main()
