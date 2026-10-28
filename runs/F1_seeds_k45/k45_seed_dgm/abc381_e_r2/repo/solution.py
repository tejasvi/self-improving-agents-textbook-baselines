def solve_query(T):
    """
    Find the maximum length of a subsequence that is an 11/22 string.
    
    An 11/22 string has the form: 1...1/2...2
    where:
    - All characters before / are 1
    - The middle character is /
    - All characters after / are 2
    """
    n = len(T)
    max_length = 0
    
    # Try each slash as the middle character
    for slash_idx in range(n):
        if T[slash_idx] != '/':
            continue
        
        # Count 1s before this slash
        ones_before = 0
        for i in range(slash_idx):
            if T[i] == '1':
                ones_before += 1
        
        # Count 2s after this slash
        twos_after = 0
        for i in range(slash_idx + 1, n):
            if T[i] == '2':
                twos_after += 1
        
        # The length is: ones + slash + twos
        # But we need at least a slash, so minimum is 1
        current_length = ones_before + 1 + twos_after
        max_length = max(max_length, current_length)
    
    return max_length


# Read input
N, Q = map(int, input().split())
S = input().strip()

# Process queries
for _ in range(Q):
    L, R = map(int, input().split())
    # Convert to 0-indexed
    substring = S[L-1:R]
    result = solve_query(substring)
    print(result)
