from itertools import combinations

# Read input
N, K = map(int, input().split())
A = list(map(int, input().split()))

# Find maximum XOR for all combinations of K elements
max_xor = 0

for combo in combinations(A, K):
    # Calculate XOR of all elements in the combination
    xor_result = 0
    for num in combo:
        xor_result ^= num
    
    # Update maximum
    max_xor = max(max_xor, xor_result)

print(max_xor)
