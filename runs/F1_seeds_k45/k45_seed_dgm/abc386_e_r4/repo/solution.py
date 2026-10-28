from itertools import combinations

def solve():
    # Read input
    N, K = map(int, input().split())
    A = list(map(int, input().split()))
    
    max_xor = 0
    
    # Try all combinations of K elements
    for combo in combinations(A, K):
        # Calculate XOR of all elements in this combination
        current_xor = 0
        for num in combo:
            current_xor ^= num
        
        # Update maximum
        max_xor = max(max_xor, current_xor)
    
    print(max_xor)

solve()
