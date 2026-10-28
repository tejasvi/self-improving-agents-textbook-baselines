from collections import deque

def solve():
    n = int(input())
    graph = []
    for _ in range(n):
        graph.append(input().strip())
    
    # For each pair (i, j), find shortest palindromic path
    result = []
    
    for start in range(n):
        row = []
        for end in range(n):
            # Find shortest palindromic path from start to end
            ans = find_palindromic_path(start, end, graph, n)
            row.append(ans)
        result.append(row)
    
    # Print result
    for row in result:
        print(' '.join(map(str, row)))

def is_palindrome(s):
    return s == s[::-1]

def find_palindromic_path(start, end, graph, n):
    """Find shortest path from start to end with palindromic labels."""
    
    # BFS approach: state is (current_vertex, path_string, length)
    # We'll use a dictionary to track visited states to avoid infinite loops
    # Key: (current_vertex, path_string), Value: minimum length
    
    if start == end:
        # Empty path is a palindrome
        return 0
    
    queue = deque([(start, "", 0)])
    visited = {(start, ""): 0}
    min_length = float('inf')
    
    # We need to limit the search to avoid infinite loops
    # A path with all same character is not helpful unless it's length 1
    # The maximum useful length is bounded
    max_iterations = n * n * 26  # Reasonable upper bound
    iterations = 0
    
    while queue and iterations < max_iterations:
        iterations += 1
        current_vertex, path_str, length = queue.popleft()
        
        # Check if current string is a palindrome and we're at target
        if current_vertex == end and is_palindrome(path_str):
            min_length = min(min_length, length)
            continue
        
        # Prune: if path is already too long, skip
        if length > min_length:
            continue
        
        # Try all outgoing edges
        for next_vertex in range(n):
            edge_label = graph[current_vertex][next_vertex]
            if edge_label != '-':
                new_path = path_str + edge_label
                new_length = length + 1
                
                # Only continue if we haven't visited this state with a shorter path
                state = (next_vertex, new_path)
                if state not in visited or visited[state] > new_length:
                    visited[state] = new_length
                    queue.append((next_vertex, new_path, new_length))
    
    return min_length if min_length != float('inf') else -1

solve()
