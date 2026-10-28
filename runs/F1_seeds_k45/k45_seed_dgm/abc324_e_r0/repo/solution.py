def match_subsequence(s, t, start_pos):
    """
    Given string s and target t, starting from position start_pos in t,
    greedily match as many characters as possible.
    Returns the final position in t reached.
    """
    pos = start_pos
    for char in s:
        if pos < len(t) and char == t[pos]:
            pos += 1
    return pos

def can_form_subsequence(s1, s2, t):
    """
    Check if concatenation of s1 and s2 contains t as a subsequence.
    """
    # First match what we can from s1
    pos = match_subsequence(s1, t, 0)
    # Then match what we can from s2 starting from pos
    pos = match_subsequence(s2, t, pos)
    # If we reached the end of t, it's a valid pair
    return pos == len(t)

def main():
    line = input().split()
    n = int(line[0])
    t = line[1]
    
    strings = []
    for _ in range(n):
        strings.append(input().strip())
    
    count = 0
    for i in range(n):
        for j in range(n):
            if can_form_subsequence(strings[i], strings[j], t):
                count += 1
    
    print(count)

if __name__ == "__main__":
    main()
