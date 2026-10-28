from itertools import product, combinations
import sys

def generate_matrices_with_sums(N, row_sums, col_sums):
    """Generate all N×N binary matrices with given row and column sums."""
    total_rows = sum(row_sums)
    total_cols = sum(col_sums)
    
    # Check if sums are feasible
    if total_rows != total_cols:
        return []
    
    # Use backtracking to generate all valid matrices
    matrices = []
    matrix = [[0] * N for _ in range(N)]
    
    def backtrack(row, col, remaining_row_sum):
        if row == N:
            # Check if column sums match
            for j in range(N):
                if sum(matrix[i][j] for i in range(N)) != col_sums[j]:
                    return
            matrices.append([row[:] for row in matrix])
            return
        
        if col == N:
            # Move to next row
            if remaining_row_sum[row] != 0:
                return
            backtrack(row + 1, 0, remaining_row_sum)
            return
        
        # Try placing 0
        # Check if it's still possible to reach row sum
        remaining_in_row = remaining_row_sum[row]
        remaining_cols = N - col
        
        matrix[row][col] = 0
        backtrack(row, col + 1, remaining_row_sum)
        
        # Try placing 1 if needed
        if remaining_in_row > 0:
            matrix[row][col] = 1
            new_remaining = remaining_row_sum[:]
            new_remaining[row] -= 1
            backtrack(row, col + 1, new_remaining)
            matrix[row][col] = 0
    
    backtrack(0, 0, list(row_sums))
    return matrices

def count_fixed_elements(matrices):
    """Count how many elements are fixed across all matrices."""
    if not matrices:
        return 0
    
    N = len(matrices[0])
    fixed_count = 0
    
    for i in range(N):
        for j in range(N):
            value = matrices[0][i][j]
            all_same = all(m[i][j] == value for m in matrices)
            if all_same:
                fixed_count += 1
    
    return fixed_count

def solve():
    N, Q = map(int, input().split())
    queries = []
    for _ in range(Q):
        K = int(input())
        queries.append(K)
    
    # Find all possible numbers of fixed elements
    possible_K = set()
    
    # Try all possible row sum combinations
    for row_sum_combo in product(range(N + 1), repeat=N):
        row_sum_total = sum(row_sum_combo)
        
        # Try all possible column sum combinations with same total
        for col_sum_combo in product(range(N + 1), repeat=N):
            if sum(col_sum_combo) != row_sum_total:
                continue
            
            # Generate all matrices with these sums
            matrices = generate_matrices_with_sums(N, row_sum_combo, col_sum_combo)
            
            if matrices:
                fixed = count_fixed_elements(matrices)
                possible_K.add(fixed)
    
    # Answer queries
    for K in queries:
        if K in possible_K:
            print("Yes")
        else:
            print("No")

solve()
