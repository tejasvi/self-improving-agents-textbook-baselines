MOD = 998244353

def solve():
    # Read input
    n, m = map(int, input().split())
    b = list(map(int, input().split()))
    
    # Find positions with -1
    neg_positions = []
    for i in range(n):
        if b[i] == -1:
            neg_positions.append(i)
    
    num_negatives = len(neg_positions)
    
    # Build a list of all potential edges
    all_edges = []
    has_neg1 = []
    has_neg2 = []
    
    for i in range(n):
        for j in range(i + 1, n):
            if b[i] == -1 or b[j] == -1:
                all_edges.append((i, j))
                has_neg1.append(b[i] == -1)
                has_neg2.append(b[j] == -1)
            elif b[i] <= b[j]:
                # This edge always exists
                all_edges.append((i, j))
                has_neg1.append(False)
                has_neg2.append(False)
    
    total_sum = 0
    
    # Brute force through all assignments
    def generate_assignments(idx=0, assignment_map=None):
        nonlocal total_sum
        
        if assignment_map is None:
            assignment_map = {}
        
        if idx == num_negatives:
            # Now we know all values, check which edges exist
            seq = b[:]
            for pos, val in assignment_map.items():
                seq[pos] = val
            
            # Compute connected components using union-find
            parent = list(range(n))
            
            def find(x):
                if parent[x] != x:
                    parent[x] = find(parent[x])
                return parent[x]
            
            # Add edges that exist in this assignment
            for k, (i, j) in enumerate(all_edges):
                if (has_neg1[k] or has_neg2[k]):
                    # This edge involves at least one -1, check if it exists
                    if seq[i] <= seq[j]:
                        pi, pj = find(i), find(j)
                        if pi != pj:
                            parent[pi] = pj
                else:
                    # This edge always exists (was pre-filtered)
                    pi, pj = find(i), find(j)
                    if pi != pj:
                        parent[pi] = pj
            
            # Count components
            components = len(set(find(i) for i in range(n)))
            total_sum = (total_sum + components) % MOD
        else:
            pos = neg_positions[idx]
            for val in range(1, m + 1):
                assignment_map[pos] = val
                generate_assignments(idx + 1, assignment_map)
            del assignment_map[pos]
    
    if num_negatives == 0:
        # No -1s to replace, just compute once
        parent = list(range(n))
        
        def find(x):
            if parent[x] != x:
                parent[x] = find(parent[x])
            return parent[x]
        
        for i, j in all_edges:
            pi, pj = find(i), find(j)
            if pi != pj:
                parent[pi] = pj
        
        components = len(set(find(i) for i in range(n)))
        total_sum = components
    else:
        generate_assignments()
    
    print(total_sum)

solve()
