def matrix_mult(A, B, p, n):
    """Multiply two n×n matrices modulo p"""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

def matrix_power(M, exp, p, n):
    """Compute M^exp modulo p using fast exponentiation"""
    result = [[0] * n for _ in range(n)]
    for i in range(n):
        result[i][i] = 1
    
    base = [row[:] for row in M]  # Copy M
    
    while exp > 0:
        if exp % 2 == 1:
            result = matrix_mult(result, base, p, n)
        base = matrix_mult(base, base, p, n)
        exp //= 2
    
    return result

def matrix_add(A, B, p, n):
    """Add two matrices modulo p"""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            C[i][j] = (A[i][j] + B[i][j]) % p
    return C

def solve():
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
    
    num_zeros = len(zero_positions)
    
    # If there are too many zeros, we need a smarter approach
    # But for now, let's try the brute force with some optimizations
    
    if num_zeros == 0:
        # No zeros, just compute A^p
        result = matrix_power(A, p, p, N)
    else:
        # Initialize result matrix with zeros
        result = [[0] * N for _ in range(N)]
        
        # Generate all combinations using iterative approach
        # This represents each combination as a base-(p-1) number
        total_combinations = (p - 1) ** num_zeros
        
        for combo in range(total_combinations):
            # Create current matrix
            current_matrix = [row[:] for row in A]
            
            # Decode combo to get the values for each zero position
            temp = combo
            for idx in range(num_zeros):
                pos_i, pos_j = zero_positions[idx]
                val = (temp % (p - 1)) + 1
                current_matrix[pos_i][pos_j] = val
                temp //= (p - 1)
            
            # Compute B^p and add to result
            B_power_p = matrix_power(current_matrix, p, p, N)
            result = matrix_add(result, B_power_p, p, N)
    
    # Print the result
    for i in range(N):
        print(' '.join(map(str, result[i])))

solve()
