from itertools import combinations

# Read input
N, K = map(int, input().split())
A = list(map(int, input().split()))

# Find the maximum XOR of K distinct elements
max_xor = 0

for combo in combinations(A, K):
    # Calculate XOR of all elements in the combination
    xor_val = 0
    for num in combo:
        xor_val ^= num
    max_xor = max(max_xor, xor_val)

print(max_xor)
