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
    partition = [-1] * (N + 1)  # 0 or 1 for bipartition color
    
    xor_sum = 0
    
    for start in range(1, N + 1):
        if visited[start]:
            continue
        
        # BFS to find component and bipartition
        queue = deque([start])
        visited[start] = True
        partition[start] = 0
        
        count_0 = 0  # count of vertices with partition 0
        count_1 = 0  # count of vertices with partition 1
        component_vertices = []
        
        while queue:
            u = queue.popleft()
            component_vertices.append(u)
            
            for v in graph[u]:
                if not visited[v]:
                    visited[v] = True
                    partition[v] = 1 - partition[u]
                    queue.append(v)
        
        # Count partition sizes
        for v in component_vertices:
            if partition[v] == 0:
                count_0 += 1
            else:
                count_1 += 1
        
        # Grundy number for this component is min(count_0, count_1)
        grundy = min(count_0, count_1)
        xor_sum ^= grundy
    
    if xor_sum != 0:
        print("Aoki")
    else:
        print("Takahashi")

solve()
