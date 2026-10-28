from collections import deque

def is_palindrome(s):
    """Check if a string is a palindrome"""
    return s == s[::-1]

def solve():
    n = int(input())
    graph = []
    for _ in range(n):
        graph.append(input().strip())
    
    # Build adjacency list with edge labels
    adj = [[] for _ in range(n)]
    for i in range(n):
        for j in range(n):
            if graph[i][j] != '-':
                adj[i].append((j, graph[i][j]))
    
    # For each starting vertex
    result = []
    for start in range(n):
        row = []
        
        # For each ending vertex
        for end in range(n):
            # BFS to find shortest palindromic path
            # State: (current_vertex, path_string)
            # We'll use a distance dictionary
            queue = deque([(start, "")])
            visited = {(start, ""): 0}  # Maps (vertex, path_string) -> distance
            min_dist = -1
            
            while queue:
                curr_vertex, path_string = queue.popleft()
                dist = visited[(curr_vertex, path_string)]
                
                # Check if we reached the end vertex and path is palindrome
                if curr_vertex == end and is_palindrome(path_string):
                    if min_dist == -1:
                        min_dist = dist
                    else:
                        min_dist = min(min_dist, dist)
                
                # Explore neighbors
                for next_vertex, edge_label in adj[curr_vertex]:
                    new_path = path_string + edge_label
                    new_dist = dist + 1
                    
                    # Pruning: only continue if path length is reasonable
                    # A palindrome of length n requires at most 2n-1 edges
                    # But we need to be careful not to prune too aggressively
                    # Let's limit based on what we've found so far
                    if min_dist != -1 and new_dist >= min_dist:
                        continue
                    
                    # Avoid infinite loops - limit path length
                    if new_dist > 2 * n * n:  # Some reasonable upper bound
                        continue
                    
                    state = (next_vertex, new_path)
                    if state not in visited or visited[state] > new_dist:
                        visited[state] = new_dist
                        queue.append(state)
            
            row.append(min_dist)
        
        result.append(row)
    
    # Print results
    for row in result:
        print(' '.join(map(str, row)))

solve()
