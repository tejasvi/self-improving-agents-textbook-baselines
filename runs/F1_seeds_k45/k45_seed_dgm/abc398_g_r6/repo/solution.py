from collections import deque, defaultdict

def solve():
    N, M = map(int, input().split())
    
    # Build adjacency list
    adj = defaultdict(list)
    for _ in range(M):
        u, v = map(int, input().split())
        adj[u].append(v)
        adj[v].append(u)
    
    # Perform a 2-coloring of the entire graph using BFS
    # This is possible since the input graph is bipartite (no odd cycles)
    color = [-1] * (N + 1)
    color_0_count = 0
    color_1_count = 0
    
    for start in range(1, N + 1):
        if color[start] != -1:
            continue
        
        # BFS to color this connected component
        queue = deque([start])
        color[start] = 0
        color_0_count += 1
        
        while queue:
            u = queue.popleft()
            for v in adj[u]:
                if color[v] == -1:
                    color[v] = 1 - color[u]
                    if color[v] == 0:
                        color_0_count += 1
                    else:
                        color_1_count += 1
                    queue.append(v)
    
    # The game ends when we have a complete bipartite graph
    # Maximum edges in a complete bipartite graph with partitions of size a and b is a*b
    # The number of moves remaining equals (a*b) - M
    # By Sprague-Grundy theorem: if remaining moves is odd, first player wins; if even, second player wins
    
    max_edges = color_0_count * color_1_count
    remaining_moves = max_edges - M
    
    if remaining_moves % 2 == 1:
        print("Aoki")
    else:
        print("Takahashi")

solve()
