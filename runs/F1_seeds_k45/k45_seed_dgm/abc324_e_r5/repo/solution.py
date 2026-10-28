def get_prefix_match(s, t):
    """
    Get the maximum prefix of t that can be matched as a subsequence in s.
    Returns the index of the next character in t we need to find.
    """
    t_idx = 0
    for char in s:
        if t_idx < len(t) and char == t[t_idx]:
            t_idx += 1
    return t_idx


def get_suffix_match(s, t):
    """
    For each starting position in t, compute how far we can progress in t
    by matching characters in s.
    Returns a dictionary: starting_t_idx -> ending_t_idx
    """
    result = {}
    for start_idx in range(len(t)):
        matched = start_idx
        for char in s:
            if matched < len(t) and char == t[matched]:
                matched += 1
        result[start_idx] = matched
    return result


def main():
    line = input().split()
    n = int(line[0])
    target = line[1]
    
    strings = []
    for _ in range(n):
        strings.append(input().strip())
    
    # For each string, compute:
    # 1. How many initial characters of target can be matched as subsequence
    prefix_matches = []
    for s in strings:
        prefix_matches.append(get_prefix_match(s, target))
    
    # 2. For each string, if we start at position k in target,
    #    how far can we progress?
    suffix_matches = []
    for s in strings:
        suffix_matches.append(get_suffix_match(s, target))
    
    count = 0
    for i in range(n):
        for j in range(n):
            # After processing S_i, we've matched up to position prefix_matches[i] in target
            # Now we need to match the rest in S_j
            start_pos = prefix_matches[i]
            end_pos = suffix_matches[j][start_pos]
            
            if end_pos == len(target):
                count += 1
    
    print(count)


if __name__ == "__main__":
    main()
