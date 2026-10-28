MOD = 998244353

def modinv(a, m=MOD):
    """Compute modular inverse of a modulo m using Fermat's little theorem"""
    return pow(a, m - 2, m)

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    # E[i] = expected value when x = i (i from 0 to N)
    # E[N] = 0 (no more outcomes can increase x beyond N)
    # For i < N:
    # E[i] = (1/N) * sum(A[y-1] + E[y] for y = i+1 to N)
    #      = (1/N) * (sum(A[j] for j=i to N-1) + sum(E[y] for y=i+1 to N))
    #
    # Multiply by N:
    # N*E[i] = sum(A[j] for j=i to N-1) + sum(E[y] for y=i+1 to N)
    #
    # Rearrange:
    # N*E[i] - sum(E[y] for y=i+1 to N) = sum(A[j] for j=i to N-1)
    
    # We'll work with variables E[0], E[1], ..., E[N-1]
    # (E[N] = 0 is already accounted for)
    
    # Build augmented matrix for the system
    matrix = [[0] * N for _ in range(N)]
    rhs = [0] * N
    
    for i in range(N):
        # Equation for E[i]:
        # N*E[i] - sum(E[y] for y=i+1 to N-1) = sum(A[j] for j=i to N-1)
        
        matrix[i][i] = N % MOD
        
        for j in range(i + 1, N):
            matrix[i][j] = (matrix[i][j] - 1) % MOD
        
        # Right hand side
        for j in range(i, N):
            rhs[i] = (rhs[i] + A[j]) % MOD
    
    # Gaussian elimination with partial pivoting in modular arithmetic
    for col in range(N):
        # Find pivot
        pivot_row = -1
        for row in range(col, N):
            if matrix[row][col] % MOD != 0:
                pivot_row = row
                break
        
        if pivot_row == -1:
            continue
        
        # Swap rows
        matrix[col], matrix[pivot_row] = matrix[pivot_row], matrix[col]
        rhs[col], rhs[pivot_row] = rhs[pivot_row], rhs[col]
        
        # Eliminate
        inv = modinv(matrix[col][col])
        for j in range(col, N):
            matrix[col][j] = (matrix[col][j] * inv) % MOD
        rhs[col] = (rhs[col] * inv) % MOD
        
        for row in range(N):
            if row != col and matrix[row][col] != 0:
                factor = matrix[row][col]
                for j in range(col, N):
                    matrix[row][j] = (matrix[row][j] - factor * matrix[col][j]) % MOD
                rhs[row] = (rhs[row] - factor * rhs[col]) % MOD
    
    # Extract solution (E[0] is what we want)
    E_0 = rhs[0] % MOD
    
    print(E_0)

solve()
