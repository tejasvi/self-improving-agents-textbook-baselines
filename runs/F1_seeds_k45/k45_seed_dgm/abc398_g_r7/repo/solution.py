# Write your solution here. Read from stdin, write to stdout.

from collections import defaultdict, deque

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Find connected components and bipartition each
    visited = [False] * (N + 1)
    color = [-1] * (N + 1)  # -1: unvisited, 0 or 1: colors
    
    grundy_xor = 0
    
    for start in range(1, N + 1):
        if visited[start]:
            continue
        
        # BFS to find component and bipartition
        queue = deque([start])
        visited[start] = True
        color[start] = 0
        
        count = [0, 0]  # count[i] = number of vertices with color i
        
        while queue:
            u = queue.popleft()
            count[color[u]] += 1
            
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    color[v] = 1 - color[u]
                    queue.append(v)
        
        # For this component, calculate Grundy number
        # Max edges in complete bipartite graph: count[0] * count[1]
        # Current edges need to be counted
        # But we already have the edges, so the number of possible moves
        # in this component is count[0] * count[1] minus current edges
        
        # Actually, let's count the actual edges in this component
        component_vertices = set()
        queue = deque([start])
        comp_visited = set([start])
        component_vertices.add(start)
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                component_vertices.add(v)
                if v not in comp_visited:
                    comp_visited.add(v)
                    queue.append(v)
        
        # Count edges in this component
        edge_count = 0
        for u in component_vertices:
            for v in graph[u]:
                if u < v and v in component_vertices:
                    edge_count += 1
        
        # Grundy number for this component
        max_edges = count[0] * count[1]
        grundy = max_edges - edge_count
        
        grundy_xor ^= grundy
    
    if grundy_xor != 0:
        print("Aoki")
    else:
        print("Takahashi")

solve()
