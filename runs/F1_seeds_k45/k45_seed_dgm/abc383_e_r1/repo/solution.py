import heapq
from scipy.optimize import linear_sum_assignment
import numpy as np

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Build adjacency list
    graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Function to compute f(x, y) - minimax path from x to y
    def minimax_path(start, end):
        """Find minimum maximum edge weight on any path from start to end"""
        if start == end:
            return 0
        
        # Use modified Dijkstra's algorithm
        # dist[i] = minimum possible maximum edge weight to reach vertex i
        dist = [float('inf')] * (N + 1)
        dist[start] = 0
        pq = [(0, start)]  # (max_weight_so_far, vertex)
        
        while pq:
            max_weight, u = heapq.heappop(pq)
            
            if max_weight > dist[u]:
                continue
            
            if u == end:
                return max_weight
            
            for v, w in graph[u]:
                # The new maximum weight on path to v through u
                new_max = max(max_weight, w)
                
                if new_max < dist[v]:
                    dist[v] = new_max
                    heapq.heappush(pq, (new_max, v))
        
        return dist[end]
    
    # Compute f(A_i, B_j) for all pairs
    # We'll create a cost matrix where cost[i][j] = f(A[i], B[j])
    cost_matrix = []
    
    for i in range(K):
        row = []
        for j in range(K):
            row.append(minimax_path(A[i], B[j]))
        cost_matrix.append(row)
    
    # Convert to numpy array for linear_sum_assignment
    cost_array = np.array(cost_matrix, dtype=np.int64)
    
    # Use Hungarian algorithm to find minimum cost assignment
    row_ind, col_ind = linear_sum_assignment(cost_array)
    
    # Calculate the minimum sum
    min_sum = 0
    for i, j in zip(row_ind, col_ind):
        min_sum += cost_matrix[i][j]
    
    print(min_sum)

solve()
