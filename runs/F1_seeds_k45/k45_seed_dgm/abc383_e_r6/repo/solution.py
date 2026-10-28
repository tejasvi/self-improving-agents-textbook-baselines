import heapq
from itertools import permutations

def main():
    # Read input
    N, M, K = map(int, input().split())
    
    graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    # Compute minimax paths from each vertex in A
    def get_minimax_dist(src):
        """Get minimax distances from src to all other vertices"""
        dist = [float('inf')] * (N + 1)
        dist[src] = 0
        pq = [(0, src)]
        
        while pq:
            d, u = heapq.heappop(pq)
            
            if d > dist[u]:
                continue
            
            for v, w in graph[u]:
                new_dist = max(d, w)
                if new_dist < dist[v]:
                    dist[v] = new_dist
                    heapq.heappush(pq, (new_dist, v))
        
        return dist
    
    # Get minimax distances from all vertices in A
    minimax = {}
    for a in A:
        minimax[a] = get_minimax_dist(a)
    
    # Build cost matrix: cost[i][j] = f(A[i], B[j])
    cost_matrix = []
    for i, a in enumerate(A):
        row = []
        for j, b in enumerate(B):
            row.append(minimax[a][b])
        cost_matrix.append(row)
    
    # Find optimal matching
    # For small K, use brute force
    if K <= 8:
        min_cost = float('inf')
        for perm in permutations(range(K)):
            cost = sum(cost_matrix[i][perm[i]] for i in range(K))
            min_cost = min(min_cost, cost)
        print(min_cost)
    else:
        # For larger K, use Hungarian algorithm via scipy or greedy
        try:
            from scipy.optimize import linear_sum_assignment
            row_ind, col_ind = linear_sum_assignment(cost_matrix)
            result = sum(cost_matrix[i][j] for i, j in zip(row_ind, col_ind))
            print(result)
        except:
            # Fallback: greedy or DP-based matching
            # Use a simple DP approach for K <= N scenario
            INF = float('inf')
            dp = [INF] * (1 << K)
            dp[0] = 0
            
            for mask in range(1 << K):
                if dp[mask] == INF:
                    continue
                idx = bin(mask).count('1')  # Number of A[i] already matched
                if idx == K:
                    continue
                
                # Try matching A[idx] with each unmatched B[j]
                for j in range(K):
                    if not (mask & (1 << j)):
                        new_mask = mask | (1 << j)
                        dp[new_mask] = min(dp[new_mask], dp[mask] + cost_matrix[idx][j])
            
            print(dp[(1 << K) - 1])

if __name__ == "__main__":
    main()
