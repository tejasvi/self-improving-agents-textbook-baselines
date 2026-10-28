# Write your solution here. Read from stdin, write to stdout.

def solve_query(s, l, r):
    """
    Find the maximum length of a subsequence that is an 11/22 string
    s: the full string
    l, r: 1-indexed positions (l and r inclusive)
    """
    # Convert to 0-indexed
    l -= 1
    r -= 1
    
    substring = s[l:r+1]
    n = len(substring)
    
    # Count of 1's from the start up to each position (inclusive)
    ones_before = [0] * n
    count = 0
    for i in range(n):
        if substring[i] == '1':
            count += 1
        ones_before[i] = count
    
    # Count of 2's from each position to the end (inclusive)
    twos_after = [0] * n
    count = 0
    for i in range(n-1, -1, -1):
        if substring[i] == '2':
            count += 1
        twos_after[i] = count
    
    max_length = 0
    
    # Try each position as the slash position
    for slash_pos in range(n):
        if substring[slash_pos] != '/':
            continue
        
        # Count 1's before this slash position
        ones = ones_before[slash_pos - 1] if slash_pos > 0 else 0
        
        # Count 2's after this slash position
        twos = twos_after[slash_pos + 1] if slash_pos < n - 1 else 0
        
        # The maximum matching pairs
        pairs = min(ones, twos)
        
        # Length is 2*pairs + 1 (for the slash)
        length = 2 * pairs + 1
        
        max_length = max(max_length, length)
    
    return max_length

# Read input
n, q = map(int, input().split())
s = input().strip()

# Process queries
for _ in range(q):
    l, r = map(int, input().split())
    print(solve_query(s, l, r))
