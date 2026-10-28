from itertools import combinations

def solve():
    # Read input
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    # Generate all combinations of K elements from A
    max_xor = 0
    
    for combo in combinations(A, K):
        # Compute XOR of all elements in the combination
        xor_val = 0
        for num in combo:
            xor_val ^= num
        max_xor = max(max_xor, xor_val)
    
    print(max_xor)

solve()
