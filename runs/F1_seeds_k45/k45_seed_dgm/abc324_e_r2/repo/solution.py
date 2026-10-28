def max_match_after(s, t, start_pos):
    """
    Given a string s and target string t, starting from position start_pos in t,
    find the furthest position we can reach in t by processing all characters of s.
    Returns the position in t after processing all of s.
    """
    pos = start_pos
    for char in s:
        if pos < len(t) and char == t[pos]:
            pos += 1
    return pos


def solve():
    # Read input
    line = input().split()
    n = int(line[0])
    t = line[1]
    
    strings = []
    for _ in range(n):
        strings.append(input().strip())
    
    # Precompute for each string and each starting position in t,
    # what position we reach after processing that string
    max_reach = []
    for i in range(n):
        reaches = []
        for start_pos in range(len(t) + 1):
            end_pos = max_match_after(strings[i], t, start_pos)
            reaches.append(end_pos)
        max_reach.append(reaches)
    
    # Count valid pairs
    count = 0
    for i in range(n):
        for j in range(n):
            # After processing S_i starting from position 0 in t
            pos_after_i = max_reach[i][0]
            # After processing S_j starting from position pos_after_i in t
            pos_after_j = max_reach[j][pos_after_i]
            
            if pos_after_j == len(t):
                count += 1
    
    print(count)


if __name__ == "__main__":
    solve()
