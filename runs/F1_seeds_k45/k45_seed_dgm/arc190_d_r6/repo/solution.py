def matrix_mult(A, B, p):
    """Multiply two matrices modulo p"""
    n = len(A)
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % p
    return C

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
    return [[(A[i][j] + B[i][j]) % p for j in range(n)] for i in range(n)]

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
    
    K = len(zero_positions)
    
    # Initialize sum matrix with zeros
    sum_matrix = [[0] * N for _ in range(N)]
    
    # Generate all possible matrices B by replacing zeros with values 1 to p-1
    def generate_and_sum(idx, current_matrix):
        if idx == K:
            # Compute B^p and add to sum
            result = matrix_pow(current_matrix, p, p)
            nonlocal sum_matrix
            sum_matrix = matrix_add(sum_matrix, result, p)
            return
        
        i, j = zero_positions[idx]
        for val in range(1, p):
            current_matrix[i][j] = val
            generate_and_sum(idx + 1, current_matrix)
    
    # Start with matrix A
    generate_and_sum(0, [row[:] for row in A])
    
    # Print result
    for i in range(N):
        print(' '.join(map(str, sum_matrix[i])))

solve()
