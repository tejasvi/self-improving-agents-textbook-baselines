import sys
from itertools import product

def matrix_mult(A, B, p):
    """Multiply two matrices modulo p"""
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % p
    return result

def matrix_pow(A, exp, p):
    """Compute A^exp modulo p using binary exponentiation"""
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in A]
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base, p)
        base = matrix_mult(base, base, p)
        exp //= 2
    
    return result

def matrix_add(A, B, p):
    """Add two matrices modulo p"""
    n = len(A)
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            result[i][j] = (A[i][j] + B[i][j]) % p
    return result

def main():
    line = input().split()
    N = int(line[0])
    p = int(line[1])
    
    A = []
    zero_positions = []
    
    for i in range(N):
        row = list(map(int, input().split()))
        A.append(row)
        for j in range(N):
            if row[j] == 0:
                zero_positions.append((i, j))
    
    K = len(zero_positions)
    
    # Initialize result matrix with zeros
    result = [[0] * N for _ in range(N)]
    
    # Generate all possible values for zero positions
    if K == 0:
        # No zeros, just compute A^p
        result = matrix_pow(A, p, p)
    else:
        # Generate all combinations of values for zeros
        for values in product(range(1, p), repeat=K):
            # Create matrix B by replacing zeros with values
            B = [row[:] for row in A]
            for idx, (i, j) in enumerate(zero_positions):
                B[i][j] = values[idx]
            
            # Compute B^p
            B_p = matrix_pow(B, p, p)
            
            # Add to result
            result = matrix_add(result, B_p, p)
    
    # Print result
    for row in result:
        print(' '.join(map(str, row)))

if __name__ == "__main__":
    main()
