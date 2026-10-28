import sys
from collections import defaultdict
import heapq

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    graph = defaultdict(list)
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Compute f(x, y) for all pairs in A and B using Dijkstra-like approach
    # f(x, y) = minimum bottleneck path from x to y
    # This is equivalent to finding the minimum maximum edge weight on any path
    
    def compute_bottleneck_distances(start):
        """
        Compute the minimum bottleneck path from start to all other vertices.
        Uses a modified Dijkstra where instead of summing weights,
        we track the maximum weight seen so far on the path.
        """
        dist = [float('inf')] * (N + 1)
        dist[start] = 0
        pq = [(0, start)]  # (max_weight_so_far, node)
        
        while pq:
            max_weight, u = heapq.heappop(pq)
            
            if max_weight > dist[u]:
                continue
            
            for v, w in graph[u]:
                new_max_weight = max(max_weight, w)
                if new_max_weight < dist[v]:
                    dist[v] = new_max_weight
                    heapq.heappush(pq, (new_max_weight, v))
        
        return dist
    
    # Compute bottleneck distances from each vertex in A
    cost_matrix = []
    for a in A:
        dist = compute_bottleneck_distances(a)
        costs = [dist[b] for b in B]
        cost_matrix.append(costs)
    
    # Now we need to find the optimal assignment of B to A
    # This is the minimum cost bipartite matching problem
    # Since K is small, we can use dynamic programming with bitmask
    
    def min_cost_matching(cost_matrix):
        """
        Find minimum cost matching using DP with bitmask.
        cost_matrix[i][j] = cost of matching A_i to B_j
        """
        K = len(cost_matrix)
        memo = {}
        
        def dp(a_idx, used_mask):
            """
            a_idx: which element of A we're trying to match
            used_mask: bitmask of which elements of B have been used
            returns: minimum cost to match A[a_idx:] with remaining B elements
            """
            if a_idx == K:
                return 0
            
            if (a_idx, used_mask) in memo:
                return memo[(a_idx, used_mask)]
            
            result = float('inf')
            for b_idx in range(K):
                if not (used_mask & (1 << b_idx)):
                    # Try matching A[a_idx] with B[b_idx]
                    cost = cost_matrix[a_idx][b_idx] + dp(a_idx + 1, used_mask | (1 << b_idx))
                    result = min(result, cost)
            
            memo[(a_idx, used_mask)] = result
            return result
        
        return dp(0, 0)
    
    answer = min_cost_matching(cost_matrix)
    print(answer)

solve()
