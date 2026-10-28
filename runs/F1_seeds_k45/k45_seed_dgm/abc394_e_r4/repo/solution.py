from collections import deque, defaultdict

def is_palindrome(s):
    return s == s[::-1]

def solve():
    n = int(input())
    
    # Read the adjacency matrix
    adj = []
    for i in range(n):
        row = input().strip()
        adj.append(row)
    
    # For each pair (i, j), find shortest palindromic path
    result = [[0] * n for _ in range(n)]
    
    for start in range(n):
        for end in range(n):
            # BFS to find shortest palindromic path from start to end
            # State: (current_vertex, path_string, distance)
            queue = deque([(start, "", 0)])
            
            # To avoid infinite loops, we track visited states with (vertex, path_string)
            # But path_string can be exponentially large, so we need to bound the search
            visited = {}  # (vertex, path_string) -> shortest_distance
            
            shortest = -1
            
            while queue:
                v, path, dist = queue.popleft()
                
                # Check if we reached the end and path is palindrome
                if v == end and is_palindrome(path):
                    shortest = dist
                    break
                
                # Avoid exploring paths that are too long
                # Since we want shortest, and N <= 100, we can limit path length
                # The maximum useful path length should be bounded
                # For a palindrome with N vertices, worst case is around 2*N or N^2
                if dist > n * n:  # Safety bound
                    continue
                
                # Avoid revisiting same state to prevent infinite loops
                state = (v, path)
                if state in visited and visited[state] <= dist:
                    continue
                visited[state] = dist
                
                # Try all outgoing edges
                for next_v in range(n):
                    edge_label = adj[v][next_v]
                    if edge_label != '-':
                        new_path = path + edge_label
                        queue.append((next_v, new_path, dist + 1))
            
            result[start][end] = shortest
    
    # Print result
    for i in range(n):
        print(' '.join(map(str, result[i])))

solve()
