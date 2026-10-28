from itertools import combinations

# Read input
N, K = map(int, input().split())
A = list(map(int, input().split()))

# Generate all combinations of K elements
max_xor = 0
for combo in combinations(A, K):
    # Calculate XOR of the combination
    xor_result = 0
    for element in combo:
        xor_result ^= element
    max_xor = max(max_xor, xor_result)

# Print the answer
print(max_xor)
