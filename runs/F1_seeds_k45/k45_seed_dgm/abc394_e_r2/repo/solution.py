from collections import deque

def is_palindrome(s):
    return s == s[::-1]

def solve():
    N = int(input())
    edges = []
    for i in range(N):
        edges.append(input().strip())
    
    # For each pair (i, j), find the shortest palindromic path
    result = []
    
    for start in range(N):
        row = []
        for end in range(N):
            # BFS to find shortest palindromic path from start to end
            # State: (current_vertex, string_built, path_length)
            queue = deque([(start, "", 0)])
            visited = {}  # (vertex, string) -> min_length to reach it
            
            shortest = -1
            
            # We need to limit the search. Maximum useful length would be 
            # bounded by the number of possible unique palindromes we can form
            # In worst case, we might need to explore many states
            max_length = 2 * N * 26  # Conservative upper bound
            
            while queue:
                curr_vertex, curr_string, path_length = queue.popleft()
                
                # Check if we reached the destination with a palindrome
                if curr_vertex == end and is_palindrome(curr_string):
                    shortest = path_length
                    break
                
                # Skip if path is too long
                if path_length >= max_length:
                    continue
                
                # Prune: if we've seen this (vertex, string) with shorter path, skip
                state = (curr_vertex, curr_string)
                if state in visited and visited[state] <= path_length:
                    continue
                visited[state] = path_length
                
                # Try all outgoing edges
                for next_vertex in range(N):
                    edge_label = edges[curr_vertex][next_vertex]
                    if edge_label != '-':
                        new_string = curr_string + edge_label
                        new_length = path_length + 1
                        
                        # Only continue if string length is reasonable
                        if len(new_string) <= max_length:
                            queue.append((next_vertex, new_string, new_length))
            
            row.append(shortest)
        result.append(row)
    
    # Print result
    for row in result:
        print(' '.join(map(str, row)))

solve()
