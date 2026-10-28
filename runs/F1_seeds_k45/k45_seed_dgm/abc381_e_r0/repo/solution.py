# Write your solution here. Read from stdin, write to stdout.

N, Q = map(int, input().split())
S = input().strip()

for _ in range(Q):
    L, R = map(int, input().split())
    # Convert to 0-indexed
    L -= 1
    R -= 1
    
    substring = S[L:R+1]
    
    max_length = 0
    
    # Try each position in the substring as the position of /
    for i in range(len(substring)):
        if substring[i] == '/':
            # Count 1's before position i
            ones_before = substring[:i].count('1')
            # Count 2's after position i
            twos_after = substring[i+1:].count('2')
            
            # The length of the 11/22 string with this / in the middle
            k = min(ones_before, twos_after)
            length = 2 * k + 1
            
            max_length = max(max_length, length)
    
    print(max_length)
