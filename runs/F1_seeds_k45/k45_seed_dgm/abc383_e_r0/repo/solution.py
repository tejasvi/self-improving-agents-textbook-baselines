import sys
from collections import defaultdict
import heapq
from itertools import permutations

def read_input():
    N, M, K = map(int, input().split())
    
    edges = []
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((u, v, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    return N, M, K, edges, A, B

def build_graph(N, edges):
    graph = defaultdict(list)
    for u, v, w in edges:
        graph[u].append((v, w))
        graph[v].append((u, w))
    return graph

def find_minimax_path(start, end, graph, N):
    """
    Find the minimax path from start to end.
    Uses Dijkstra's algorithm where we minimize the maximum edge weight.
    """
    if start == end:
        return 0
    
    # dist[i] = minimum possible maximum edge weight to reach vertex i
    dist = [float('inf')] * (N + 1)
    dist[start] = 0
    
    pq = [(0, start)]
    
    while pq:
        max_edge, u = heapq.heappop(pq)
        
        if max_edge > dist[u]:
            continue
        
        if u == end:
            return max_edge
        
        for v, w in graph[u]:
            # The maximum edge weight on the path through this edge
            new_max = max(max_edge, w)
            
            if new_max < dist[v]:
                dist[v] = new_max
                heapq.heappush(pq, (new_max, v))
    
    return dist[end]

def solve():
    N, M, K, edges, A, B = read_input()
    
    graph = build_graph(N, edges)
    
    # Compute f(A_i, B_j) for all i, j
    cost = []
    for a in A:
        row = []
        for b in B:
            f_val = find_minimax_path(a, b, graph, N)
            row.append(f_val)
        cost.append(row)
    
    # Find the minimum cost perfect matching
    # Since K is small, we can try all permutations of B
    min_sum = float('inf')
    
    for perm in permutations(range(K)):
        current_sum = sum(cost[i][perm[i]] for i in range(K))
        min_sum = min(min_sum, current_sum)
    
    print(min_sum)

solve()
