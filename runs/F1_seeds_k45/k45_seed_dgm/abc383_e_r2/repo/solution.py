import heapq
from itertools import permutations

def read_input():
    N, M, K = map(int, input().split())
    
    edges = []
    graph = [[] for _ in range(N + 1)]
    
    for _ in range(M):
        u, v, w = map(int, input().split())
        edges.append((w, u, v))
        graph[u].append((v, w))
        graph[v].append((u, w))
    
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    
    return N, M, K, graph, A, B

def compute_minimax_path(graph, start, N):
    """
    Compute minimax path from start to all other vertices.
    minimax[v] = minimum of the maximum edge weights on any path from start to v
    """
    minimax = [float('inf')] * (N + 1)
    minimax[start] = 0
    
    # Use a min-heap: (max_weight_so_far, vertex)
    pq = [(0, start)]
    
    while pq:
        max_weight, u = heapq.heappop(pq)
        
        if max_weight > minimax[u]:
            continue
        
        for v, w in graph[u]:
            new_max = max(max_weight, w)
            if new_max < minimax[v]:
                minimax[v] = new_max
                heapq.heappush(pq, (new_max, v))
    
    return minimax

def solve(N, M, K, graph, A, B):
    # Compute f(x, y) for all pairs we need
    # We only need f(A[i], B[j]) for all i, j
    
    # Precompute minimax paths from all vertices in A
    minimax_from_A = {}
    unique_A = set(A)
    for a in unique_A:
        minimax_from_A[a] = compute_minimax_path(graph, a, N)
    
    # Build cost matrix: cost[i][j] = f(A[i], B[j])
    cost = []
    for i in range(K):
        row = []
        for j in range(K):
            a_vertex = A[i]
            b_vertex = B[j]
            f_value = minimax_from_A[a_vertex][b_vertex]
            row.append(f_value)
        cost.append(row)
    
    # Find the optimal permutation of B
    # Since K is small (K <= N <= 2*10^5), but in practice for matching problems,
    # if K is small enough, we can use brute force permutations
    # However, for larger K, we need a better approach
    
    # For small K (up to ~10), brute force permutations work
    # For larger K, use assignment algorithm (Hungarian algorithm)
    
    if K <= 8:
        # Brute force for small K
        min_sum = float('inf')
        for perm in permutations(range(K)):
            current_sum = sum(cost[i][perm[i]] for i in range(K))
            min_sum = min(min_sum, current_sum)
        return min_sum
    else:
        # Use backtracking with pruning for larger K
        used = [False] * K
        current_sum = [0]
        min_sum = [float('inf')]
        
        def backtrack(idx):
            if idx == K:
                min_sum[0] = min(min_sum[0], current_sum[0])
                return
            
            # Pruning: if current sum already exceeds minimum, stop
            if current_sum[0] >= min_sum[0]:
                return
            
            for j in range(K):
                if not used[j]:
                    used[j] = True
                    current_sum[0] += cost[idx][j]
                    backtrack(idx + 1)
                    current_sum[0] -= cost[idx][j]
                    used[j] = False
        
        backtrack(0)
        return min_sum[0]

def main():
    N, M, K, graph, A, B = read_input()
    result = solve(N, M, K, graph, A, B)
    print(result)

if __name__ == "__main__":
    main()
