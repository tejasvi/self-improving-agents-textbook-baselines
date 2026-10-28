from collections import deque

def is_palindrome(s):
    return s == s[::-1]

def solve():
    n = int(input())
    graph = []
    for i in range(n):
        row = input().strip()
        graph.append(row)
    
    # For each pair (i, j), find the shortest path with palindromic labels
    result = []
    
    for start in range(n):
        row_result = []
        for end in range(n):
            # BFS to find shortest palindromic path from start to end
            shortest = find_shortest_palindromic_path(graph, n, start, end)
            row_result.append(shortest)
        result.append(row_result)
    
    # Print results
    for row in result:
        print(' '.join(map(str, row)))

def find_shortest_palindromic_path(graph, n, start, end):
    """
    Find shortest path from start to end where labels form a palindrome.
    State: (current_vertex, path_string)
    We use BFS to explore states by path length.
    """
    
    # Special case: start == end, empty string is palindrome with length 0
    if start == end:
        return 0
    
    # BFS: queue contains (current_vertex, path_string, length)
    queue = deque([(start, "", 0)])
    # visited tracks (vertex, path_string) to avoid re-exploring same state
    visited = set()
    visited.add((start, ""))
    
    min_palindrome_length = float('inf')
    
    # Reasonable bound on path length to search
    max_length = min(2 * n * n, 1000)
    
    while queue:
        current, path, length = queue.popleft()
        
        # Pruning: if we already found a palindrome path and current path is longer, skip
        if length >= min_palindrome_length:
            continue
        
        # Try all outgoing edges from current vertex
        for next_vertex in range(n):
            edge_label = graph[current][next_vertex]
            if edge_label == '-':
                continue
            
            new_path = path + edge_label
            new_length = length + 1
            
            # Check if this new path is a palindrome and leads to end vertex
            if next_vertex == end and is_palindrome(new_path):
                min_palindrome_length = min(min_palindrome_length, new_length)
            
            # Continue exploring only if we haven't exceeded bounds
            if new_length < min_palindrome_length and new_length < max_length:
                state = (next_vertex, new_path)
                if state not in visited:
                    visited.add(state)
                    queue.append((next_vertex, new_path, new_length))
    
    if min_palindrome_length == float('inf'):
        return -1
    return min_palindrome_length

if __name__ == "__main__":
    solve()
