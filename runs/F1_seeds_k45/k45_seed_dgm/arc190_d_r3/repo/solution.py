import sys
from itertools import product

def matrix_multiply(A, B, p):
    """Multiply two NxN matrices modulo p"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def matrix_power(A, exp, p):
    """Compute A^exp modulo p using binary exponentiation"""
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in A]
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_multiply(result, base, p)
        base = matrix_multiply(base, base, p)
        exp //= 2
    
    return result

def add_matrices(A, B, p):
    """Add two NxN matrices modulo p"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % p
    return C

def solve():
    # Read input
    line = input().split()
    n, p = int(line[0]), int(line[1])
    
    A = []
    for i in range(n):
        row = list(map(int, input().split()))
        A.append(row)
    
    # Find all zero positions
    zeros = []
    for i in range(n):
        for j in range(n):
            if A[i][j] == 0:
                zeros.append((i, j))
    
    k = len(zeros)
    
    if k == 0:
        # No zeros, just compute A^p
        result = matrix_power(A, p, p)
        for row in result:
            print(' '.join(map(str, row)))
        return
    
    # Initialize sum matrix
    sum_matrix = [[0] * n for _ in range(n)]
    
    # Iterate through all possible replacements
    # Each zero can be replaced with values 1 to p-1
    for replacement in product(range(1, p), repeat=k):
        # Create matrix B by replacing zeros with values from replacement
        B = [row[:] for row in A]
        for idx, (i, j) in enumerate(zeros):
            B[i][j] = replacement[idx]
        
        # Compute B^p mod p
        B_pow_p = matrix_power(B, p, p)
        
        # Add to sum_matrix
        sum_matrix = add_matrices(sum_matrix, B_pow_p, p)
    
    # Output result
    for row in sum_matrix:
        print(' '.join(map(str, row)))

solve()
