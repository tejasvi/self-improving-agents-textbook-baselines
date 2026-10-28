def nand(a, b):
    """NAND operation: returns 1 unless both inputs are 1"""
    if a == 1 and b == 1:
        return 0
    return 1

def solve():
    n = int(input())
    s = input().strip()
    
    # Convert string to list of integers
    A = [int(c) for c in s]
    
    total = 0
    
    # For each starting position i
    for i in range(n):
        # For each ending position j >= i
        current_val = A[i]
        total += current_val
        
        for j in range(i + 1, n):
            current_val = nand(current_val, A[j])
            total += current_val
    
    print(total)

solve()
