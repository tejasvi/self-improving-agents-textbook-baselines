# Write your solution here. Read from stdin, write to stdout.

def can_match_subsequence(s, t, start_pos):
    """
    Check how far we can match string t in string s, starting from position start_pos in t.
    Returns the position in t after matching (i.e., the index of the next character to match).
    """
    pos = start_pos
    for char in s:
        if pos < len(t) and char == t[pos]:
            pos += 1
    return pos

def solve():
    line = input().split()
    n = int(line[0])
    t = line[1]
    
    strings = []
    for _ in range(n):
        strings.append(input().strip())
    
    count = 0
    
    # For each pair (i, j)
    for i in range(n):
        for j in range(n):
            # Concatenate S_i and S_j
            concatenated = strings[i] + strings[j]
            
            # Check if T is a subsequence of concatenated
            pos = 0
            for char in concatenated:
                if pos < len(t) and char == t[pos]:
                    pos += 1
            
            # If we matched all of T
            if pos == len(t):
                count += 1
    
    print(count)

solve()
