# Write your solution here. Read from stdin, write to stdout.

def nand(a, b):
    """NAND operation: NOT(a AND b)"""
    return 1 - (a & b)

def solve():
    N = int(input())
    S = input().strip()
    
    # Convert string to list of integers
    A = [int(c) for c in S]
    
    total = 0
    
    # For each starting position i
    for i in range(N):
        # Compute f(i, j) for j >= i
        # f(i, i) = A[i]
        current = A[i]
        total += current
        
        # f(i, j) for j > i
        for j in range(i + 1, N):
            current = nand(current, A[j])
            total += current
    
    print(total)

solve()
