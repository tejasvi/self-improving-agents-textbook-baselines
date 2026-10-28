from collections import deque, defaultdict

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Find connected components and their bipartitions using BFS
    visited = [False] * (N + 1)
    total_moves = 0
    
    for start in range(1, N + 1):
        if visited[start]:
            continue
        
        # BFS to find component and bipartition
        color = [-1] * (N + 1)
        queue = deque([start])
        color[start] = 0
        visited[start] = True
        
        partition_count = [0, 0]  # count of vertices in each partition
        
        while queue:
            u = queue.popleft()
            partition_count[color[u]] += 1
            
            for v in graph[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    visited[v] = True
                    queue.append(v)
        
        # For this component, calculate the number of edges we can add
        # Edges within partition 0: partition_count[0] * (partition_count[0] - 1) / 2
        # Edges within partition 1: partition_count[1] * (partition_count[1] - 1) / 2
        a = partition_count[0]
        b = partition_count[1]
        moves_in_component = a * (a - 1) // 2 + b * (b - 1) // 2
        total_moves += moves_in_component
    
    # If total moves is odd, first player (Aoki) wins
    if total_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()
