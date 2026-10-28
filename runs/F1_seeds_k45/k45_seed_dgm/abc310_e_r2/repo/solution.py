def nand(a, b):
    """Compute NAND operation: 1 if not (a and b)"""
    return 1 - (a & b)

def solve():
    n = int(input())
    s = input().strip()
    
    # Convert string to list of integers
    A = [int(c) for c in s]
    
    total = 0
    
    # For each starting position i
    for i in range(n):
        # Initialize f(i, i) = A[i]
        f = A[i]
        total += f
        
        # For each ending position j > i
        for j in range(i + 1, n):
            # f(i, j) = f(i, j-1) ⊥ A[j]
            f = nand(f, A[j])
            total += f
    
    print(total)

solve()
