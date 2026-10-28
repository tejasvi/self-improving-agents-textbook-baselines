from collections import deque, defaultdict

def is_palindrome(s):
    """Check if a string is a palindrome."""
    return s == s[::-1]

def solve():
    n = int(input())
    
    # Read the adjacency matrix
    graph = []
    for i in range(n):
        row = input().strip()
        graph.append(row)
    
    # Build adjacency list
    adj = defaultdict(list)
    for i in range(n):
        for j in range(n):
            if graph[i][j] != '-':
                adj[i].append((j, graph[i][j]))
    
    # Result matrix
    result = [[-1] * n for _ in range(n)]
    
    # For each starting vertex
    for start in range(n):
        # BFS to find shortest palindromic paths
        # State: (current_vertex, path_string, length)
        queue = deque([(start, "", 0)])
        
        # visited[vertex][string] = shortest length to reach that state
        visited = defaultdict(lambda: defaultdict(lambda: float('inf')))
        visited[start][""] = 0
        
        # We'll process states by length to ensure we find shortest paths first
        # Limit the search space - paths shouldn't be too long
        max_length = 2 * n * n  # Upper bound on useful path length
        
        while queue:
            current, path_str, length = queue.popleft()
            
            # Skip if we've seen a shorter path to this state
            if visited[current][path_str] < length:
                continue
            
            # If path is a palindrome, record it at destination
            if is_palindrome(path_str):
                if result[start][current] == -1 or result[start][current] > length:
                    result[start][current] = length
            
            # Don't explore further if path is too long
            if length >= max_length:
                continue
            
            # Explore neighbors
            for neighbor, edge_label in adj[current]:
                new_path = path_str + edge_label
                new_length = length + 1
                
                # Only continue if we haven't visited this state with a shorter path
                if visited[neighbor][new_path] > new_length:
                    visited[neighbor][new_path] = new_length
                    queue.append((neighbor, new_path, new_length))
    
    # Print result
    for i in range(n):
        print(' '.join(map(str, result[i])))

if __name__ == "__main__":
    solve()
