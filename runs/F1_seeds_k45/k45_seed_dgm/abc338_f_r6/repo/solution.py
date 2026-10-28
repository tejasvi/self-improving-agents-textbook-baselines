#!/usr/bin/env python3
"""
Solution for Negative Traveling Salesman Problem

We need to find a walk that visits each vertex at least once with minimum weight.
We can revisit edges and vertices, so this is a shortest path problem with constraints.

Approach:
- Use dynamic programming with bitmask DP
- dp[v][mask] = minimum cost to be at vertex v having visited all vertices in mask
- We can start from any vertex and need to find a path that visits all vertices
- Check all possible final vertices and return the minimum
"""

from collections import defaultdict
import sys

def solve():
    line = input().split()
    N, M = int(line[0]), int(line[1])
    
    # Read edges
    edges = []
    graph = defaultdict(list)  # graph[u] = [(v, w), ...]
    
    for _ in range(M):
        parts = input().split()
        u, v, w = int(parts[0]), int(parts[1]), int(parts[2])
        u -= 1  # Convert to 0-indexed
        v -= 1
        edges.append((u, v, w))
        graph[u].append((v, w))
    
    # DP with bitmask
    # dp[v][mask] = minimum cost to reach vertex v with visited set = mask
    INF = float('inf')
    dp = [[INF] * (1 << N) for _ in range(N)]
    
    # We can start from any vertex
    for start in range(N):
        mask = 1 << start
        dp[start][mask] = 0
    
    # Use Bellman-Ford style relaxation for negative weights
    # Iterate enough times to find shortest paths
    for iteration in range(N * (1 << N)):
        updated = False
        for v in range(N):
            for mask in range(1 << N):
                if dp[v][mask] == INF:
                    continue
                
                # Try to go to each neighbor
                for u, w in graph[v]:
                    new_mask = mask | (1 << u)
                    new_cost = dp[v][mask] + w
                    
                    if new_cost < dp[u][new_mask]:
                        dp[u][new_mask] = new_cost
                        updated = True
        
        if not updated:
            break
    
    # Find the minimum cost to visit all vertices
    full_mask = (1 << N) - 1
    result = INF
    
    for v in range(N):
        result = min(result, dp[v][full_mask])
    
    if result == INF:
        print("No")
    else:
        print(result)

if __name__ == "__main__":
    solve()
