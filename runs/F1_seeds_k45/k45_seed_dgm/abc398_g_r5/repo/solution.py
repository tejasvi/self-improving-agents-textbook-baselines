from collections import defaultdict, deque

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Find connected components and 2-color them (bipartite coloring)
    color = [-1] * (N + 1)
    components_info = []
    
    for start in range(1, N + 1):
        if color[start] != -1:
            continue
        
        # BFS to color and find component info
        queue = deque([start])
        color[start] = 0
        partition0 = [start]
        partition1 = []
        
        while queue:
            u = queue.popleft()
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    if color[v] == 0:
                        partition0.append(v)
                    else:
                        partition1.append(v)
                    queue.append(v)
        
        # Store partition sizes for this component
        size0 = len(partition0)
        size1 = len(partition1)
        
        # Count edges in this component (count from partition 0 only, since all edges go between partitions)
        edges_in_component = 0
        for u in partition0:
            edges_in_component += len(graph[u])
        
        # Maximum possible edges in complete bipartite graph
        max_edges = size0 * size1
        
        # Moves available = max_edges - current_edges
        moves_available = max_edges - edges_in_component
        
        components_info.append(moves_available)
    
    # XOR all Grundy numbers (which are just the move counts for a nim-like game)
    xor_sum = 0
    for moves in components_info:
        xor_sum ^= moves
    
    # If xor_sum != 0, first player (Aoki) wins
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

solve()
