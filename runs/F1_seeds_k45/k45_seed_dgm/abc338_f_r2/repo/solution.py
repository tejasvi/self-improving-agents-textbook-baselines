#!/usr/bin/env python3
"""
Negative Traveling Salesman Problem

We need to find a walk that visits each vertex at least once with minimum cost.
The graph can have negative edges but no negative cycles.

Approach:
1. Use DP with bitmask: dp[mask][v] = minimum cost to visit all vertices in mask and currently at v
2. Initialize: for each starting vertex, set dp[1<<(v-1)][v] = 0
3. Iterate through all states and relax edges
4. Use Bellman-Ford style relaxation with enough iterations to handle negative weights
"""

from collections import defaultdict

def solve():
    # Read input
    N, M = map(int, input().split())
    
    # Build adjacency list
    edges = defaultdict(list)  # edges[u] = [(v, w), ...]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges[u].append((v, w))
    
    # DP with bitmask
    # dp[mask][v] = minimum cost to visit all vertices in mask and currently be at v
    INF = float('inf')
    dp = [[INF] * (N + 1) for _ in range(1 << N)]
    
    # Initialize: we can start at any vertex with cost 0
    for start in range(1, N + 1):
        mask = 1 << (start - 1)
        dp[mask][start] = 0
    
    # Full mask - all vertices visited
    full_mask = (1 << N) - 1
    
    # Relax edges using Bellman-Ford style approach
    # We need at most N * (1 << N) iterations in the worst case,
    # but in practice much fewer
    for iteration in range(N * (1 << N)):
        updated = False
        
        for current_mask in range(1 << N):
            for u in range(1, N + 1):
                if dp[current_mask][u] == INF:
                    continue
                if not (current_mask & (1 << (u - 1))):
                    continue
                
                # Try to go to adjacent vertices
                for v, w in edges[u]:
                    new_mask = current_mask | (1 << (v - 1))
                    new_cost = dp[current_mask][u] + w
                    
                    if new_cost < dp[new_mask][v]:
                        dp[new_mask][v] = new_cost
                        updated = True
        
        if not updated:
            break
    
    # Find minimum cost to visit all vertices
    best = INF
    for v in range(1, N + 1):
        best = min(best, dp[full_mask][v])
    
    if best == INF:
        print("No")
    else:
        print(best)

solve()
