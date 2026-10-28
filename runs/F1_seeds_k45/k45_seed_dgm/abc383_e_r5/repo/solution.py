import sys
from collections import defaultdict
import heapq
from itertools import permutations

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Build graph
    graph = defaultdict(list)
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Compute f(x, y) for all pairs using modified Dijkstra
    # f(x, y) = minimum possible maximum edge weight on path from x to y
    # This is the "minimax path" problem
    
    def compute_minimax(start):
        """Compute minimax distances from start vertex to all other vertices"""
        # dist[v] = minimum of maximum edge weights on path from start to v
        dist = [float('inf')] * (N + 1)
        dist[start] = 0
        
        # Use max-heap (negate values for min-heap behavior)
        pq = [(0, start)]
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if d > dist[u]:
                continue
            
            for v, w in graph[u]:
                # The max weight on path through this edge is max(dist[u], w)
                new_dist = max(dist[u], w)
                
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        
        return dist
    
    # Get all unique vertices we need to compute from
    relevant_vertices = set(A) | set(B)
    
    # Precompute minimax distances from all relevant vertices
    minimax_dist = {}
    for vertex in relevant_vertices:
        minimax_dist[vertex] = compute_minimax(vertex)
    
    # Build cost matrix: cost[i][j] = f(A[i], B[j])
    cost_matrix = []
    for a in A:
        row = []
        for b in B:
            row.append(minimax_dist[a][b])
        cost_matrix.append(row)
    
    # Find optimal assignment using Hungarian algorithm
    # For small K, we can also try brute force or use scipy
    
    # Since K can be up to N (2×10^5), we need efficient algorithm
    # Use Hungarian algorithm
    
    min_cost = hungarian_algorithm(cost_matrix)
    print(min_cost)

def hungarian_algorithm(cost_matrix):
    """
    Solve the assignment problem using the Hungarian algorithm.
    Returns the minimum cost of assignment.
    """
    n = len(cost_matrix)
    m = len(cost_matrix[0]) if n > 0 else 0
    
    if n == 0 or m == 0:
        return 0
    
    # For rectangular matrices, we need to handle differently
    # Assuming n == m for now (K workers, K jobs)
    
    # Create a copy of cost matrix
    cost = [row[:] for row in cost_matrix]
    
    # Subtract row minima
    for i in range(n):
        min_val = min(cost[i])
        for j in range(m):
            cost[i][j] -= min_val
    
    # Subtract column minima
    for j in range(m):
        min_val = min(cost[i][j] for i in range(n))
        for i in range(n):
            cost[i][j] -= min_val
    
    # Find maximum matching with 0-cost edges
    while True:
        # Find initial matching with 0-cost edges
        match_row = [-1] * n
        match_col = [-1] * m
        
        for i in range(n):
            for j in range(m):
                if cost[i][j] == 0 and match_row[i] == -1 and match_col[j] == -1:
                    match_row[i] = j
                    match_col[j] = i
        
        # Check if we have perfect matching
        if all(match_row[i] != -1 for i in range(n)):
            # Perfect matching found
            total_cost = 0
            for i in range(n):
                j = match_row[i]
                total_cost += cost_matrix[i][j]
            return total_cost
        
        # Find uncovered rows and columns
        covered_rows = [False] * n
        covered_cols = [False] * m
        
        # Mark covered rows
        unmatched = [i for i in range(n) if match_row[i] == -1]
        
        # BFS to find augmenting paths
        queue = unmatched[:]
        visited_row = [False] * n
        visited_col = [False] * m
        
        for u in unmatched:
            visited_row[u] = True
        
        while queue:
            i = queue.pop(0)
            for j in range(m):
                if cost[i][j] == 0 and not visited_col[j]:
                    visited_col[j] = True
                    if match_col[j] == -1:
                        # Found augmenting path, augment
                        while j != -1:
                            prev_i = match_col[j]
                            match_col[j] = i
                            j_prev = match_row[i]
                            match_row[i] = j
                            i = prev_i
                            j = j_prev
                        break
                    else:
                        next_i = match_col[j]
                        if not visited_row[next_i]:
                            visited_row[next_i] = True
                            queue.append(next_i)
        
        # Update covered rows and columns
        for i in range(n):
            covered_rows[i] = visited_row[i]
        for j in range(m):
            covered_cols[j] = visited_col[j]
        
        # Find uncovered minimum
        min_uncovered = float('inf')
        for i in range(n):
            if covered_rows[i]:
                for j in range(m):
                    if not covered_cols[j]:
                        min_uncovered = min(min_uncovered, cost[i][j])
        
        if min_uncovered == float('inf'):
            # No uncovered cell, something wrong
            break
        
        # Update cost matrix
        for i in range(n):
            for j in range(m):
                if covered_rows[i] and not covered_cols[j]:
                    cost[i][j] -= min_uncovered
                elif not covered_rows[i] and covered_cols[j]:
                    cost[i][j] += min_uncovered

if __name__ == "__main__":
    solve()
