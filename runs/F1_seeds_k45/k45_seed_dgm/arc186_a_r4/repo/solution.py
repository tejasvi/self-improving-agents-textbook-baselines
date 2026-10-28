from itertools import combinations
import sys

def can_construct_matrices(row_sums, col_sums):
    """Check if matrices with given row/col sums exist and return all valid matrices."""
    N = len(row_sums)
    
    # Quick check: total sum must match
    if sum(row_sums) != sum(col_sums):
        return []
    
    # Generate all valid binary matrices using backtracking
    def backtrack(matrix, row_idx, col_counts):
        if row_idx == N:
            # Check if all column sums match
            if col_counts == list(col_sums):
                return [matrix[:]]
            return []
        
        result = []
        # Generate all combinations for this row
        row_sum = row_sums[row_idx]
        
        # Try all ways to place row_sum ones in N positions
        for positions in combinations(range(N), row_sum):
            # Check if this choice violates column sum constraints
            valid = True
            for col in range(N):
                if col_counts[col] + (1 if col in positions else 0) > col_sums[col]:
                    valid = False
                    break
            
            if valid:
                new_row = [0] * N
                for col in positions:
                    new_row[col] = 1
                
                new_col_counts = col_counts[:]
                for col in positions:
                    new_col_counts[col] += 1
                
                matrix.append(new_row)
                result.extend(backtrack(matrix, row_idx + 1, new_col_counts))
                matrix.pop()
        
        return result
    
    matrices = backtrack([], 0, [0] * N)
    return matrices

def count_fixed_elements(matrices):
    """Count how many elements are the same in all matrices."""
    if not matrices:
        return 0
    
    N = len(matrices[0])
    fixed_count = 0
    
    for i in range(N):
        for j in range(N):
            # Check if element (i,j) is the same in all matrices
            val = matrices[0][i][j]
            is_fixed = all(mat[i][j] == val for mat in matrices)
            if is_fixed:
                fixed_count += 1
    
    return fixed_count

def solve_small(N):
    """Find all possible numbers of fixed elements for small N."""
    possible_fixed = set()
    
    # Enumerate all possible matrices
    for matrix_bits in range(2 ** (N * N)):
        matrix = []
        temp = matrix_bits
        for i in range(N):
            row = []
            for j in range(N):
                row.append(temp & 1)
                temp >>= 1
            matrix.append(row)
        
        # Get row and column sums
        row_sums = [sum(row) for row in matrix]
        col_sums = [sum(matrix[i][j] for i in range(N)) for j in range(N)]
        
        # Find all matrices with same row/col sums
        matrices = can_construct_matrices(row_sums, col_sums)
        
        if matrices:
            fixed_count = count_fixed_elements(matrices)
            possible_fixed.add(fixed_count)
    
    return possible_fixed

def solve_large(N):
    """Find possible numbers of fixed elements for large N using enumeration."""
    possible_fixed = set()
    
    # Enumerate all possible row and column sum vectors more systematically
    # For N up to 30, we can't enumerate all 2^(N^2) matrices
    # Instead, we enumerate all possible (row_sums, col_sums) pairs
    
    def generate_vectors(n):
        """Generate all possible sum vectors of length n with elements 0 to n."""
        if n == 1:
            return [[i] for i in range(n + 1)]
        smaller = generate_vectors(n - 1)
        result = []
        for vec in smaller:
            for i in range(n + 1):
                result.append(vec + [i])
        return result
    
    # This is still exponential... for N=30 it's too much
    # Let me use a smarter sampling strategy
    
    import random
    random.seed(42)
    
    # Try various structured patterns
    patterns = []
    
    # All zeros
    patterns.append(([0] * N, [0] * N))
    
    # All ones
    patterns.append(([N] * N, [N] * N))
    
    # Identity-like patterns
    for k in range(N + 1):
        patterns.append(([k] * N, [k] * N))
    
    # Random patterns
    for _ in range(min(10000, 2 ** min(N, 15))):
        row_sums = [random.randint(0, N) for _ in range(N)]
        # Make column sums match row sums by adjusting
        col_sums = row_sums[:]
        patterns.append((row_sums, col_sums))
    
    # Try more structured patterns
    for total in range(N * N + 1):
        # Try to distribute 'total' ones uniformly across rows/cols
        avg = total // N
        remainder = total % N
        row_sums = [avg] * N
        col_sums = [avg] * N
        for i in range(remainder):
            row_sums[i] += 1
            col_sums[i] += 1
        if sum(row_sums) == sum(col_sums):
            patterns.append((row_sums, col_sums))
    
    for row_sums, col_sums in patterns:
        if sum(row_sums) == sum(col_sums):
            matrices = can_construct_matrices(row_sums, col_sums)
            if matrices:
                fixed_count = count_fixed_elements(matrices)
                possible_fixed.add(fixed_count)
    
    return possible_fixed

N, Q = map(int, input().split())

# Choose approach based on N
if N <= 6:
    possible_counts = solve_small(N)
else:
    possible_counts = solve_large(N)

for _ in range(Q):
    K = int(input())
    if K in possible_counts:
        print("Yes")
    else:
        print("No")
