from itertools import product, combinations
from collections import defaultdict

def count_fixed_elements(n, row_sums, col_sums):
    """
    Count the number of fixed elements for a given set of row and column sums.
    An element is fixed if it must be the same in all matrices with given row/col sums.
    """
    # Generate all possible matrices with the given row and column sums
    all_matrices = []
    
    def backtrack(matrix, row_idx):
        if row_idx == n:
            # Check if column sums match
            col_sum_check = [sum(matrix[i][j] for i in range(n)) for j in range(n)]
            if col_sum_check == col_sums:
                all_matrices.append([row[:] for row in matrix])
            return
        
        # Generate all possible rows with the required sum
        row_sum = row_sums[row_idx]
        for row in combinations(range(n), row_sum):
            new_row = [0] * n
            for col in row:
                new_row[col] = 1
            
            # Prune: check if this partial assignment can lead to a valid solution
            # Check if remaining rows can satisfy column constraints
            current_col_sums = [sum(matrix[i][j] for i in range(row_idx)) + new_row[j] 
                               for j in range(n)]
            remaining_rows = n - row_idx - 1
            
            # Check if it's still possible to satisfy column sums
            valid = True
            for j in range(n):
                if current_col_sums[j] > col_sums[j]:
                    valid = False
                    break
                if current_col_sums[j] + remaining_rows < col_sums[j]:
                    valid = False
                    break
            
            if valid:
                matrix[row_idx] = new_row
                backtrack(matrix, row_idx + 1)
    
    matrix = [[0] * n for _ in range(n)]
    backtrack(matrix, 0)
    
    if not all_matrices:
        return 0
    
    # Count fixed elements
    fixed_count = 0
    for i in range(n):
        for j in range(n):
            value = all_matrices[0][i][j]
            is_fixed = all(matrix[i][j] == value for matrix in all_matrices)
            if is_fixed:
                fixed_count += 1
    
    return fixed_count

def solve(n, queries):
    """
    Find which fixed element counts are achievable.
    """
    possible_counts = set()
    
    # Iterate through all possible row sum combinations
    for row_sums_tuple in product(range(n + 1), repeat=n):
        row_sums = list(row_sums_tuple)
        total_ones = sum(row_sums)
        
        # Iterate through all possible column sum combinations with matching total
        for col_sums_tuple in product(range(n + 1), repeat=n):
            col_sums = list(col_sums_tuple)
            if sum(col_sums) != total_ones:
                continue
            
            # Count fixed elements for this configuration
            fixed = count_fixed_elements(n, row_sums, col_sums)
            possible_counts.add(fixed)
    
    return possible_counts

def main():
    line = input().split()
    n = int(line[0])
    q = int(line[1])
    
    queries = []
    for _ in range(q):
        k = int(input())
        queries.append(k)
    
    possible_counts = solve(n, queries)
    
    for k in queries:
        if k in possible_counts:
            print("Yes")
        else:
            print("No")

if __name__ == "__main__":
    main()
