from itertools import combinations

# Read input
N, K = map(int, input().split())
A = list(map(int, input().split()))

# Find the maximum XOR of K distinct elements
max_xor = 0

# Iterate through all combinations of K elements
for combo in combinations(A, K):
    # Calculate XOR of current combination
    xor_result = 0
    for num in combo:
        xor_result ^= num
    
    # Update maximum
    max_xor = max(max_xor, xor_result)

print(max_xor)
