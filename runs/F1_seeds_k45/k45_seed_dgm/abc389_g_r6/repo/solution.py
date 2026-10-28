from collections import deque

def is_connected_dfs(n, adj):
    """Check if graph is connected using DFS"""
    if not adj[0]:  # Vertex 0 has no edges
        return False
    
    visited = [False] * n
    stack = [0]
    visited[0] = True
    count = 1
    
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                count += 1
                stack.append(v)
    
    return count == n

def get_reachable_from_0(n, adj):
    """Get vertices reachable from vertex 0"""
    if not adj[0]:
        return {0}
    
    visited = [False] * n
    stack = [0]
    visited[0] = True
    
    while stack:
        u = stack.pop()
        for v in adj[u]:
            if not visited[v]:
                visited[v] = True
                stack.append(v)
    
    return set(i for i in range(n) if visited[i])

def check_valid_graph(n, adj):
    """Check if graph satisfies the condition (even == odd distances from vertex 0)"""
    distances = [-1] * n
    distances[0] = 0
    queue = deque([0])
    
    while queue:
        u = queue.popleft()
        for v in adj[u]:
            if distances[v] == -1:
                distances[v] = distances[u] + 1
                queue.append(v)
    
    even_count = sum(1 for d in distances if d >= 0 and d % 2 == 0)
    odd_count = sum(1 for d in distances if d >= 0 and d % 2 == 1)
    
    return even_count == odd_count

def solve(n, p):
    """Solve the problem using optimized backtracking"""
    max_edges = n * (n - 1) // 2
    min_edges = n - 1
    
    results = [0] * (max_edges - min_edges + 1)
    
    # Generate all possible edges in order
    all_edges = []
    for i in range(n):
        for j in range(i + 1, n):
            all_edges.append((i, j))
    
    count_per_m = [0] * (max_edges + 1)
    
    # Use backtracking to enumerate all graphs
    def backtrack(edge_idx, adj, current_m):
        """
        Backtrack through edges to enumerate all connected graphs
        """
        # Pruning: if we already exceed max_edges
        if current_m > max_edges:
            return
        
        # If we've processed all edges, check if this is a valid graph
        if edge_idx == len(all_edges):
            if current_m >= min_edges:
                # Check connectivity first (faster to fail early)
                if is_connected_dfs(n, adj):
                    # Then check the distance condition
                    if check_valid_graph(n, adj):
                        count_per_m[current_m] += 1
            return
        
        # Pruning: if we can't reach min_edges even taking all remaining edges
        remaining = len(all_edges) - edge_idx
        if current_m + remaining < min_edges:
            return
        
        # If we have min_edges edges, check connectivity for early pruning
        # Only check occasionally to avoid overhead
        if current_m == min_edges and edge_idx > len(all_edges) // 3:
            reachable = get_reachable_from_0(n, adj)
            unreachable = set(range(n)) - reachable
            
            # Check if remaining edges can connect the unreachable vertices
            can_connect = False
            for u, v in all_edges[edge_idx:]:
                if (u in reachable and v in unreachable) or (v in reachable and u in unreachable):
                    can_connect = True
                    break
            
            if not can_connect and len(unreachable) > 0:
                # Prune this branch - it's impossible to connect all vertices
                return
        
        u, v = all_edges[edge_idx]
        
        # Try not including this edge
        backtrack(edge_idx + 1, adj, current_m)
        
        # Try including this edge (only if we haven't exceeded max_edges)
        if current_m < max_edges:
            adj[u].append(v)
            adj[v].append(u)
            
            backtrack(edge_idx + 1, adj, current_m + 1)
            
            # Backtrack
            adj[u].pop()
            adj[v].pop()
    
    adj = [[] for _ in range(n)]
    backtrack(0, adj, 0)
    
    # Build result array
    for m in range(min_edges, max_edges + 1):
        results[m - min_edges] = count_per_m[m] % p
    
    return results

def main():
    line = input().strip()
    n, p = map(int, line.split())
    
    results = solve(n, p)
    print(' '.join(map(str, results)))

if __name__ == '__main__':
    main()
