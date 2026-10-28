from collections import deque, defaultdict

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    graph = defaultdict(list)
    for _ in range(M):
        u, v = map(int, input().split())
        graph[u].append(v)
        graph[v].append(u)
    
    # Color the graph using BFS (bipartite coloring)
    # Since the graph has no odd cycles, it's bipartite
    color = [-1] * (N + 1)
    count = [0, 0]  # count[0] = vertices with color 0, count[1] = vertices with color 1
    
    # Process each connected component
    for start in range(1, N + 1):
        if color[start] == -1:
            # BFS to color this component
            queue = deque([start])
            color[start] = 0
            count[0] += 1
            
            while queue:
                u = queue.popleft()
                for v in graph[u]:
                    if color[v] == -1:
                        color[v] = 1 - color[u]
                        count[color[v]] += 1
                        queue.append(v)
    
    # Maximum possible edges in bipartite graph
    max_edges = count[0] * count[1]
    
    # Number of moves possible
    moves = max_edges - M
    
    # If moves is odd, first player (Aoki) wins
    if moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()
