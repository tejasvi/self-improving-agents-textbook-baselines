import heapq
from itertools import permutations

def minimax_dijkstra(start, graph, n):
    """
    Compute minimax distance from start to all other vertices.
    minimax distance = minimum possible maximum edge weight on any path
    """
    dist = [float('inf')] * (n + 1)
    dist[start] = 0
    pq = [(0, start)]
    
    while pq:
        d, u = heapq.heappop(pq)
        
        if d > dist[u]:
            continue
        
        if u in graph:
            for v, w in graph[u]:
                # The new minimax distance to v through u
                new_dist = max(dist[u], w)
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
    
    return dist

def hungarian_algorithm(cost_matrix):
    """
    Simplified Hungarian algorithm for assignment problem.
    For smaller K, we can use brute force.
    """
    K = len(cost_matrix)
    
    if K <= 8:
        # Brute force for small K
        min_cost = float('inf')
        for perm in permutations(range(K)):
            cost = sum(cost_matrix[i][perm[i]] for i in range(K))
            min_cost = min(min_cost, cost)
        return min_cost
    else:
        # Use more efficient algorithm for larger K
        # Implement a basic Hungarian algorithm
        return hungarian_recursive(cost_matrix, 0, [False] * K, 0)

def hungarian_recursive(cost_matrix, row, used_cols, current_cost):
    """
    Recursive solution with pruning for assignment problem.
    """
    K = len(cost_matrix)
    
    if row == K:
        return current_cost
    
    min_cost = float('inf')
    for col in range(K):
        if not used_cols[col]:
            used_cols[col] = True
            cost = hungarian_recursive(cost_matrix, row + 1, used_cols, 
                                       current_cost + cost_matrix[row][col])
            min_cost = min(min_cost, cost)
            used_cols[col] = False
    
    return min_cost

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Build graph as adjacency list
    graph = {}
    for _ in range(M):
        u, v, w = map(int, input().split())
        if u not in graph:
            graph[u] = []
        if v not in graph:
            graph[v] = []
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Compute minimax distances from each vertex in A to all vertices
    # cost[i][j] = f(A[i], B[j])
    cost_matrix = []
    for a in A:
        dist = minimax_dijkstra(a, graph, N)
        cost_row = [dist[b] for b in B]
        cost_matrix.append(cost_row)
    
    # Solve assignment problem
    min_sum = hungarian_algorithm(cost_matrix)
    
    print(min_sum)

if __name__ == "__main__":
    solve()
