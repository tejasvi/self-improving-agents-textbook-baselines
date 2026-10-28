import sys
from itertools import product

def matrix_mult(A, B, p, N):
    """Multiply two N x N matrices modulo p"""
    C = [[0] * N for _ in range(N)]
    for i in range(N):
        for j in range(N):
            for k in range(N):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def matrix_pow(A, exp, p, N):
    """Compute A^exp modulo p"""
    result = [[1 if i == j else 0 for j in range(N)] for i in range(N)]
    base = [row[:] for row in A]
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base, p, N)
        base = matrix_mult(base, base, p, N)
        exp //= 2
    
    return result

def add_matrices(A, B, p, N):
    """Add two matrices modulo p"""
    return [[(A[i][j] + B[i][j]) % p for j in range(N)] for i in range(N)]

def solve():
    # Read input
    N, p = map(int, input().split())
    A = []
    zero_positions = []
    
    for i in range(N):
        row = list(map(int, input().split()))
        A.append(row)
        for j in range(N):
            if row[j] == 0:
                zero_positions.append((i, j))
    
    K = len(zero_positions)
    
    # Initialize result matrix
    result = [[0] * N for _ in range(N)]
    
    # Enumerate all possible replacements of zeros
    # Each zero can be replaced by values 1 to p-1
    for replacement in product(range(1, p), repeat=K):
        # Create matrix B with current replacement
        B = [row[:] for row in A]
        for idx, (i, j) in enumerate(zero_positions):
            B[i][j] = replacement[idx]
        
        # Compute B^p
        B_pow_p = matrix_pow(B, p, p, N)
        
        # Add to result
        result = add_matrices(result, B_pow_p, p, N)
    
    # Print result
    for i in range(N):
        print(' '.join(str(result[i][j]) for j in range(N)))

if __name__ == "__main__":
    solve()
