def matrix_mult(A, B, mod):
    """Multiply two matrices A and B modulo mod"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % mod
    return C

def matrix_pow(A, exp, mod):
    """Compute A^exp modulo mod using fast exponentiation"""
    n = len(A)
    result = [[1 if i == j else 0 for j in range(n)] for i in range(n)]
    base = [row[:] for row in A]
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base, mod)
        base = matrix_mult(base, base, mod)
        exp //= 2
    
    return result

def matrix_add(A, B, mod):
    """Add two matrices A and B modulo mod"""
    n = len(A)
    return [[(A[i][j] + B[i][j]) % mod for j in range(n)] for i in range(n)]

def solve():
    line = input().split()
    N = int(line[0])
    p = int(line[1])
    
    A = []
    for _ in range(N):
        row = list(map(int, input().split()))
        A.append(row)
    
    # Find all zero positions
    zero_positions = []
    for i in range(N):
        for j in range(N):
            if A[i][j] == 0:
                zero_positions.append((i, j))
    
    num_zeros = len(zero_positions)
    
    # Initialize result matrix
    result = [[0] * N for _ in range(N)]
    
    # Iterate through all possible replacements (p-1)^K combinations
    def generate_replacements(index):
        if index == num_zeros:
            # We have a complete replacement, compute B^p and add to result
            B = [row[:] for row in A]
            for zero_idx, (i, j) in enumerate(zero_positions):
                B[i][j] = current_replacement[zero_idx]
            
            # Compute B^p
            B_pow_p = matrix_pow(B, p, p)
            
            # Add to result
            for i in range(N):
                for j in range(N):
                    result[i][j] = (result[i][j] + B_pow_p[i][j]) % p
        else:
            # Try all values from 1 to p-1 for this zero position
            for val in range(1, p):
                current_replacement[index] = val
                generate_replacements(index + 1)
    
    current_replacement = [0] * num_zeros
    generate_replacements(0)
    
    # Print result
    for i in range(N):
        print(' '.join(map(str, result[i])))

solve()
