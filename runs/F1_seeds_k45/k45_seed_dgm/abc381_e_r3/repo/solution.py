def solve_query(substring):
    """
    Find the longest 11/22 subsequence in the given substring.
    
    An 11/22 string has the form: 1^k / 2^k for k >= 0
    (k ones, followed by a slash, followed by k twos)
    """
    n = len(substring)
    
    # If substring is empty, return 0
    if n == 0:
        return 0
    
    # Check if we can form just "/"
    if "/" in substring:
        max_length = 1
    else:
        max_length = 0
    
    # For each position i that contains '/', try to maximize the subsequence
    # We need k ones before slash and k twos after slash
    for slash_pos in range(n):
        if substring[slash_pos] != '/':
            continue
        
        # Count available 1's before this slash
        ones_before = substring[:slash_pos].count('1')
        
        # Count available 2's after this slash
        twos_after = substring[slash_pos + 1:].count('2')
        
        # We can take min(ones_before, twos_after) pairs of (1, 2)
        k = min(ones_before, twos_after)
        
        # Length = k ones + 1 slash + k twos = 2k + 1
        length = 2 * k + 1
        max_length = max(max_length, length)
    
    return max_length

# Read input
n, q = map(int, input().split())
s = input().strip()

# Process queries
for _ in range(q):
    l, r = map(int, input().split())
    # Convert to 0-indexed
    substring = s[l-1:r]
    result = solve_query(substring)
    print(result)
