from collections import deque

def is_palindrome(s):
    return s == s[::-1]

def solve():
    N = int(input())
    graph = []
    for i in range(N):
        graph.append(input().strip())
    
    # Result matrix
    result = [[-1] * N for _ in range(N)]
    
    # For each starting vertex
    for start in range(N):
        # BFS to find shortest palindromic paths
        # State: (current_vertex, string_formed, path_length)
        queue = deque([(start, "", 0)])
        
        # Track the shortest palindromic path to each vertex
        # ans[v] = shortest palindromic path from start to v
        ans = [-1] * N
        
        # Handle empty string - staying at start vertex
        if is_palindrome(""):
            ans[start] = 0
        
        # To avoid infinite exploration, limit by path length
        # We'll explore paths up to length 2*N as a reasonable bound
        max_length = 2 * N + 10
        
        # visited tracks (vertex, string) pairs we've seen to avoid infinite loops
        # But we need to be careful - different strings at same vertex should be explored
        # Use a dict to track best path length for each string at each vertex
        visited = {}  # (vertex, string) -> path_length
        
        while queue:
            v, s, length = queue.popleft()
            
            # Skip if we've seen this state with a shorter path
            state = (v, s)
            if state in visited and visited[state] <= length:
                continue
            visited[state] = length
            
            # Check if current string is palindrome
            if is_palindrome(s):
                if ans[v] == -1 or ans[v] > length:
                    ans[v] = length
            
            # Don't explore further if we've exceeded max length
            if length >= max_length:
                continue
            
            # Explore neighbors
            for next_v in range(N):
                edge_label = graph[v][next_v]
                if edge_label != '-':
                    next_s = s + edge_label
                    next_length = length + 1
                    
                    # Only add to queue if we haven't visited this state
                    # or if we found a shorter path
                    next_state = (next_v, next_s)
                    if next_state not in visited or visited[next_state] > next_length:
                        queue.append((next_v, next_s, next_length))
        
        result[start] = ans
    
    # Print result
    for row in result:
        print(' '.join(map(str, row)))

solve()
