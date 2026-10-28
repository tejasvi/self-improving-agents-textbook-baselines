from collections import deque

def solve():
    n = int(input())
    graph = []
    for _ in range(n):
        graph.append(input().strip())
    
    # Result matrix
    result = [[-1] * n for _ in range(n)]
    
    # For each pair (i, j), find shortest palindromic path
    for start in range(n):
        for end in range(n):
            result[start][end] = bfs_palindrome(graph, n, start, end)
    
    # Print result
    for row in result:
        print(' '.join(map(str, row)))

def bfs_palindrome(graph, n, start, end):
    """
    Find shortest palindromic path from start to end using BFS.
    
    We use BFS to explore paths level by level (by length).
    State: (current_vertex, path_string)
    """
    
    # Special case: same vertex, empty path is a palindrome
    if start == end:
        return 0
    
    # Quick check for single character palindromes
    if graph[start][end] != '-':
        best = 1
    else:
        best = float('inf')
    
    # BFS to explore paths by length
    queue = deque([(start, "")])
    visited = set()
    visited.add((start, ""))
    
    max_depth = 2 * n + 5
    
    while queue:
        vertex, path = queue.popleft()
        
        if len(path) > max_depth:
            continue
        
        # Prune: if path is already longer than best solution, skip
        if len(path) >= best:
            continue
        
        # Check if we reached the target with a palindrome
        if vertex == end and is_palindrome(path):
            best = len(path)
            continue  # Continue to find potentially better solutions
        
        # Explore neighbors
        for next_v in range(n):
            if graph[vertex][next_v] != '-':
                new_path = path + graph[vertex][next_v]
                
                if len(new_path) > max_depth:
                    continue
                
                state = (next_v, new_path)
                if state not in visited:
                    visited.add(state)
                    queue.append((next_v, new_path))
    
    return best if best != float('inf') else -1

def is_palindrome(s):
    return s == s[::-1]

solve()
