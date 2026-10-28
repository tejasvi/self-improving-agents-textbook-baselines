from itertools import product

def matrix_multiply_inplace(A, B, p, n, result=None):
    """Multiply two n×n matrices modulo p"""
    if result is None:
        result = [[0] * n for _ in range(n)]
    else:
        for i in range(n):
            for j in range(n):
                result[i][j] = 0
    
    for i in range(n):
        for k in range(n):
            if A[i][k] != 0:  # Skip if zero
                for j in range(n):
                    result[i][j] = (result[i][j] + A[i][k] * B[k][j]) % p
    return result

def matrix_power(matrix, exp, p, n):
    """Compute matrix^exp modulo p using binary exponentiation"""
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1  # Identity matrix
    
    base = [row[:] for row in matrix]  # Copy matrix
    temp = [[0] * n for _ in range(n)]  # Reusable temp matrix
    
    while exp > 0:
        if exp & 1:  # if exp is odd
            temp = matrix_multiply_inplace(result, base, p, n, temp)
            result, temp = temp, result
        base = matrix_multiply_inplace(base, base, p, n, temp)
        exp >>= 1
    
    return result

def solve():
    line = input().split()
    n = int(line[0])
    p = int(line[1])
    
    A = []
    zero_positions = []
    
    # Read matrix and find zero positions
    for i in range(n):
        row = list(map(int, input().split()))
        A.append(row)
        for j in range(n):
            if row[j] == 0:
                zero_positions.append((i, j))
    
    num_zeros = len(zero_positions)
    
    # Handle case with no zeros
    if num_zeros == 0:
        result = matrix_power(A, p, p, n)
        for i in range(n):
            print(' '.join(map(str, result[i])))
        return
    
    # Initialize sum matrix
    sum_matrix = [[0] * n for _ in range(n)]
    
    # Use product iterator to generate all combinations
    for values in product(range(1, p), repeat=num_zeros):
        # Create matrix B by replacing zeros
        B = [row[:] for row in A]
        for idx, (i, j) in enumerate(zero_positions):
            B[i][j] = values[idx]
        
        # Compute B^p
        B_p = matrix_power(B, p, p, n)
        
        # Add to sum
        for i in range(n):
            for j in range(n):
                sum_matrix[i][j] = (sum_matrix[i][j] + B_p[i][j]) % p
    
    # Print result
    for i in range(n):
        print(' '.join(map(str, sum_matrix[i])))

solve()
