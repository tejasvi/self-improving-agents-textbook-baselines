import heapq
from itertools import permutations

def compute_minimax_paths(n, edges):
    """
    Compute the minimax path weight between all pairs of vertices.
    The minimax path weight is the minimum of the maximum edge weights
    over all possible paths.
    
    This uses a modified Dijkstra's algorithm run from each vertex.
    """
    # Build adjacency list
    adj = [[] for _ in range(n + 1)]
    for u, v, w in edges:
        adj[u].append((v, w))
        adj[v].append((u, w))
    
    # For each starting vertex, compute minimax distances to all other vertices
    minimax = [[float('inf')] * (n + 1) for _ in range(n + 1)]
    
    for start in range(1, n + 1):
        # Use Dijkstra-like approach but tracking maximum edge weight
        dist = [float('inf')] * (n + 1)
        dist[start] = 0
        pq = [(0, start)]  # (max_weight_so_far, vertex)
        
        while pq:
            max_weight, u = heapq.heappop(pq)
            
            if max_weight > dist[u]:
                continue
            
            for v, w in adj[u]:
                new_max_weight = max(max_weight, w)
                if new_max_weight < dist[v]:
                    dist[v] = new_max_weight
                    heapq.heappush(pq, (new_max_weight, v))
        
        for i in range(1, n + 1):
            minimax[start][i] = dist[i]
    
    return minimax


def min_cost_matching(cost_matrix):
    """
    Find minimum cost perfect matching using brute force for small K
    or Hungarian algorithm for larger K.
    cost_matrix[i][j] = cost of matching element i from first set to j from second set
    """
    n = len(cost_matrix)
    
    # For K <= 10, use permutation brute force
    if n <= 10:
        min_cost = float('inf')
        for perm in permutations(range(n)):
            cost = sum(cost_matrix[i][perm[i]] for i in range(n))
            min_cost = min(min_cost, cost)
        return min_cost
    
    # For larger K, use Hungarian algorithm
    # Implementation of Kuhn-Munkres algorithm
    return hungarian_min_cost_matching(cost_matrix)


def hungarian_min_cost_matching(cost_matrix):
    """
    Hungarian algorithm implementation for minimum cost bipartite matching.
    Returns the minimum total cost.
    """
    n = len(cost_matrix)
    m = len(cost_matrix[0]) if n > 0 else 0
    
    # Ensure square matrix for Hungarian
    if n != m:
        # Pad with infinity
        size = max(n, m)
        padded = [[float('inf')] * size for _ in range(size)]
        for i in range(n):
            for j in range(m):
                padded[i][j] = cost_matrix[i][j]
        cost_matrix = padded
        n = m = size
    
    # Convert to integers (shift to handle floats)
    MAX_COST = 10**18
    int_cost = [[int(cost_matrix[i][j]) if cost_matrix[i][j] < MAX_COST else MAX_COST 
                 for j in range(n)] for i in range(n)]
    
    # Apply Hungarian algorithm
    u = [0] * (n + 1)
    v = [0] * (n + 1)
    p = [0] * (n + 1)
    way = [0] * (n + 1)
    
    for i in range(1, n + 1):
        p[0] = i
        j0 = 0
        minv = [float('inf')] * (n + 1)
        used = [False] * (n + 1)
        
        while p[j0] != 0:
            i0 = p[j0]
            delta = float('inf')
            j1 = 0
            
            for j in range(1, n + 1):
                if not used[j]:
                    cur = int_cost[i0 - 1][j - 1] - u[i0] - v[j]
                    if cur < minv[j]:
                        minv[j] = cur
                        way[j] = j0
                    if minv[j] < delta:
                        delta = minv[j]
                        j1 = j
            
            for j in range(n + 1):
                if used[j]:
                    u[p[j]] += delta
                    v[j] -= delta
                else:
                    minv[j] -= delta
            
            j0 = j1
            used[j0] = True
        
        while j0:
            j1 = way[j0]
            p[j0] = p[j1]
            j0 = j1
    
    return -v[0]


def solve():
    # Read input
    n, m, k = map(int, input().split())
    
    edges = []
    for _ in range(m):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Compute minimax paths between all pairs
    minimax = compute_minimax_paths(n, edges)
    
    # Build cost matrix: cost[i][j] = f(A[i], B[j])
    cost_matrix = []
    for a in A:
        row = []
        for b in B:
            cost = minimax[a][b]
            # Convert inf to a large number if needed
            if cost == float('inf'):
                cost = 10**18
            row.append(cost)
        cost_matrix.append(row)
    
    # Find optimal assignment
    min_cost = min_cost_matching(cost_matrix)
    
    print(int(min_cost))


if __name__ == "__main__":
    solve()
