from collections import defaultdict, deque

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Find connected components and check if they're bipartite
    visited = [False] * (N + 1)
    color = [-1] * (N + 1)
    
    total_xor = 0
    
    for start in range(1, N + 1):
        if visited[start]:
            continue
        
        # BFS to color the component
        queue = deque([start])
        visited[start] = True
        color[start] = 0
        
        component = []
        count = [0, 0]  # count[0] = vertices with color 0, count[1] = vertices with color 1
        
        while queue:
            u = queue.popleft()
            component.append(u)
            count[color[u]] += 1
            
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    color[v] = 1 - color[u]
                    queue.append(v)
        
        # For a bipartite component with parts of size a and b:
        # Max possible edges = a * b
        # Current edges in this component need to be counted
        
        # Count edges in this component
        edges_in_component = 0
        for u in component:
            for v in graph[u]:
                if u < v:  # Count each edge once
                    edges_in_component += 1
        
        a, b = count[0], count[1]
        max_edges = a * b
        remaining_moves = max_edges - edges_in_component
        
        # XOR the Grundy numbers
        total_xor ^= remaining_moves
    
    # If XOR is non-zero, first player wins
    if total_xor != 0:
        print("Aoki")
    else:
        print("Takahashi")

solve()
