MOD = 998244353

def matrix_mult(A, B, n):
    """Multiply two n x n matrices modulo MOD"""
    C = [[0] * n for _ in range(n)]
    for i in range(n):
        for j in range(n):
            for k in range(n):
                C[i][j] = (C[i][j] + A[i][k] * B[k][j]) % MOD
    return C

def matrix_pow(A, p, n):
    """Compute A^p modulo MOD using binary exponentiation"""
    result = [[0] * n for _ in range(n)]
    # Initialize as identity matrix
    for i in range(n):
        result[i][i] = 1
    
    base = [row[:] for row in A]  # Copy of A
    
    while p > 0:
        if p % 2 == 1:
            result = matrix_mult(result, base, n)
        base = matrix_mult(base, base, n)
        p //= 2
    
    return result

def vector_matrix_mult(v, A, n):
    """Multiply vector v by matrix A from the right"""
    result = [0] * n
    for j in range(n):
        for i in range(n):
            result[j] = (result[j] + v[i] * A[i][j]) % MOD
    return result

def solve():
    # Read input
    N, M, K = map(int, input().split())
    
    # Initialize adjacency matrix
    adj = [[0] * N for _ in range(N)]
    
    # Add edges from i to i+1 (cycle edges)
    for i in range(N):
        adj[i][(i + 1) % N] = 1
    
    # Add custom edges
    for _ in range(M):
        x, y = map(int, input().split())
        x -= 1  # Convert to 0-indexed
        y -= 1
        adj[x][y] += 1
    
    # Compute A^K where A is the adjacency matrix
    result_matrix = matrix_pow(adj, K, N)
    
    # The answer is result_matrix[0][0] (paths from vertex 0 to vertex 0 in K steps)
    # Actually, we need result_matrix[0][v] for all v, but the question asks for
    # number of paths of length K starting from vertex 1 (0-indexed: 0)
    # The answer is the sum of all entries in row 0, or more specifically,
    # we need to sum paths to any vertex
    
    # Actually, reading the problem again:
    # We need to count sequences (v_0, v_1, ..., v_K) where v_0 = 1
    # This means we start at vertex 1 (0-indexed: 0) and after K moves we can be at any vertex
    # The count is the sum of result_matrix[0][j] for all j (paths from 0 to any vertex j in K steps)
    
    answer = sum(result_matrix[0]) % MOD
    print(answer)

solve()
