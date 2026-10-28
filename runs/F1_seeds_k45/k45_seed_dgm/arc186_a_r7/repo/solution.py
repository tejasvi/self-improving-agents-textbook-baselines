import sys
from itertools import combinations

def is_valid_row_col_sums(N, row_sums, col_sums):
    """Check if row sums and column sums are valid (same total)"""
    return sum(row_sums) == sum(col_sums)

def get_all_matrices_with_sums(N, row_sums, col_sums, matrix=None, row_idx=0, results=None):
    """
    Generate all distinct matrices with given row and column sums.
    """
    if results is None:
        results = []
    if matrix is None:
        matrix = [[0] * N for _ in range(N)]
    
    # If we've filled all rows
    if row_idx == N:
        # Check if all column sums are satisfied
        for j in range(N):
            if sum(matrix[i][j] for i in range(N)) != col_sums[j]:
                return results
        results.append([row[:] for row in matrix])
        return results
    
    # Try all possible ways to fill row_idx with exactly row_sums[row_idx] ones
    for positions in combinations(range(N), row_sums[row_idx]):
        row = [0] * N
        for pos in positions:
            row[pos] = 1
        
        # Check if this row is feasible
        feasible = True
        for j in range(N):
            current_col_sum = sum(matrix[i][j] for i in range(row_idx)) + row[j]
            remaining_rows = N - row_idx - 1
            max_possible = current_col_sum + remaining_rows
            if current_col_sum > col_sums[j] or max_possible < col_sums[j]:
                feasible = False
                break
        
        if feasible:
            matrix[row_idx] = row[:]
            get_all_matrices_with_sums(N, row_sums, col_sums, matrix, row_idx + 1, results)
    
    return results

def count_fixed_elements(N, row_sums, col_sums):
    """Count the number of fixed elements for a given set of row and column sums."""
    matrices = get_all_matrices_with_sums(N, row_sums, col_sums)
    
    if not matrices:
        return -1
    
    if len(matrices) == 1:
        # All elements are fixed
        return N * N
    
    # Count fixed elements
    fixed_count = 0
    for i in range(N):
        for j in range(N):
            # Check if all matrices have the same value at (i, j)
            value = matrices[0][i][j]
            all_same = all(m[i][j] == value for m in matrices)
            if all_same:
                fixed_count += 1
    
    return fixed_count

def get_all_row_col_sums(N):
    """Generate all valid combinations of row and column sums."""
    def generate_tuples(n, length):
        if length == 0:
            yield ()
            return
        
        for val in range(n + 1):
            for rest in generate_tuples(n, length - 1):
                yield (val,) + rest
    
    for row_sums in generate_tuples(N, N):
        row_total = sum(row_sums)
        # Column sums must have the same total
        for col_sums in generate_tuples(N, N):
            if sum(col_sums) == row_total:
                yield (row_sums, col_sums)

def solve(N):
    """Find all possible counts of fixed elements for N x N matrices."""
    possible_counts = set()
    
    # Generate all possible row and column sum combinations
    for row_sums, col_sums in get_all_row_col_sums(N):
        fixed = count_fixed_elements(N, row_sums, col_sums)
        if fixed >= 0:
            possible_counts.add(fixed)
    
    return possible_counts

# Read input
N, Q = map(int, input().split())
possible_counts = solve(N)

for _ in range(Q):
    K = int(input())
    if K in possible_counts:
        print("Yes")
    else:
        print("No")
