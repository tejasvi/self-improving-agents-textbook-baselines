def solve():
    MOD = 998244353
    
    N = int(input())
    s = input().strip()
    
    # Count hub connections
    hub_count = sum(1 for c in s if c == '1')
    
    # We'll use a smarter approach:
    # For cycle edges, enumerate their orientations
    # For hub edges, enumerate their orientations
    # This is still exponential but more manageable
    
    # Actually, let's think about it differently:
    # The cycle edges form N edges
    # The hub edges form hub_count edges
    # Total = N + hub_count edges
    
    total_edges = N + hub_count
    
    # If total_edges is still too large (> 20-25), we need a smarter approach
    # For now, let's try the brute force with some optimization
    
    if total_edges > 25:
        # Need a smarter approach
        # Let's use a more clever enumeration
        return solve_smart(N, s)
    
    unique_sequences = set()
    
    # Enumerate all orientations
    for mask in range(1 << total_edges):
        in_degree = [0] * (N + 1)
        
        # Process cycle edges (first N edges)
        for i in range(N):
            u, v = i, (i + 1) % N
            if mask & (1 << i):
                in_degree[u] += 1
            else:
                in_degree[v] += 1
        
        # Process hub edges
        edge_idx = N
        for i in range(N):
            if s[i] == '1':
                u, v = i, N
                if mask & (1 << edge_idx):
                    in_degree[u] += 1
                else:
                    in_degree[v] += 1
                edge_idx += 1
        
        unique_sequences.add(tuple(in_degree))
    
    return len(unique_sequences) % MOD

def solve_smart(N, s):
    """For larger inputs, we need a smarter approach"""
    MOD = 998244353
    
    # Key observation: We can decompose the problem
    # The cycle edges and hub edges are somewhat independent
    
    # For cycle: Each cycle orientation gives vertex i an in-degree contribution from cycle
    # For hub: Each hub orientation gives vertex i an in-degree contribution from hub
    
    # Let's compute possible in-degrees from cycle and hub separately
    
    # Get all possible cycle orientations and their in-degree contributions
    cycle_indegrees = {}  # maps cycle in-degree tuple to count
    
    for mask_cycle in range(1 << N):
        in_deg_cycle = [0] * N
        for i in range(N):
            u, v = i, (i + 1) % N
            if mask_cycle & (1 << i):
                in_deg_cycle[u] += 1
            else:
                in_deg_cycle[v] += 1
        cycle_indegrees[tuple(in_deg_cycle)] = mask_cycle
    
    # Get all possible hub orientations and their in-degree contributions
    hub_edges = [(i, N) for i in range(N) if s[i] == '1']
    hub_indegrees = {}  # maps (hub in-degree tuple on vertices, hub in-degree on N) to count
    
    for mask_hub in range(1 << len(hub_edges)):
        in_deg_hub_vertices = [0] * N
        in_deg_hub_center = 0
        
        for edge_idx, (u, v) in enumerate(hub_edges):
            if mask_hub & (1 << edge_idx):
                in_deg_hub_vertices[u] += 1
            else:
                in_deg_hub_center += 1
        
        hub_indegrees[tuple(in_deg_hub_vertices + [in_deg_hub_center])] = mask_hub
    
    # Combine
    unique_sequences = set()
    for cycle_deg_tuple in cycle_indegrees.keys():
        for hub_deg_tuple in hub_indegrees.keys():
            full_deg = tuple(cycle_deg_tuple[i] + hub_deg_tuple[i] for i in range(N)) + (hub_deg_tuple[N],)
            unique_sequences.add(full_deg)
    
    return len(unique_sequences) % MOD

print(solve())
