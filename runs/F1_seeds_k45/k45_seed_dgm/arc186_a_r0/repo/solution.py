def can_construct_matrix(n, row_sums, col_sums):
    """Check if a 0/1 matrix with given row and column sums exists using Gale-Ryser theorem variant"""
    # For 0/1 matrices, we can use a greedy approach
    # Create a matrix trying to satisfy the constraints
    
    # Simple feasibility check: sum of row sums must equal sum of col sums
    if sum(row_sums) != sum(col_sums):
        return False
    
    # All values should be valid
    for r in row_sums:
        if r < 0 or r > n:
            return False
    for c in col_sums:
        if c < 0 or c > n:
            return False
    
    # Try to construct a matrix greedily
    matrix = [[0] * n for _ in range(n)]
    r_copy = list(row_sums)
    c_copy = list(col_sums)
    
    for i in range(n):
        # For row i, we need to place r_copy[i] ones
        # Choose columns greedily (those with highest remaining demand)
        cols = sorted(range(n), key=lambda j: -c_copy[j])
        
        for j in cols:
            if r_copy[i] == 0:
                break
            if c_copy[j] > 0:
                matrix[i][j] = 1
                r_copy[i] -= 1
                c_copy[j] -= 1
        
        if r_copy[i] > 0:
            return False
    
    return True


def count_fixed_elements_brute_force(n, row_sums, col_sums):
    """Count fixed elements by trying all possible 0/1 matrices"""
    import itertools
    
    # Generate all possible 0/1 matrices with given row/col sums
    matrices = []
    
    def backtrack(matrix, row_idx):
        if row_idx == n:
            # Check if column sums match
            col_sums_actual = [sum(matrix[i][j] for i in range(n)) for j in range(n)]
            if col_sums_actual == col_sums:
                matrices.append([row[:] for row in matrix])
            return
        
        # Generate all ways to place row_sums[row_idx] ones in current row
        positions = list(range(n))
        for combo in itertools.combinations(positions, row_sums[row_idx]):
            row = [0] * n
            for j in combo:
                row[j] = 1
            matrix[row_idx] = row
            backtrack(matrix, row_idx + 1)
    
    if len(matrices) == 0:
        matrix = [[0] * n for _ in range(n)]
        backtrack(matrix, 0)
    
    if not matrices:
        return -1  # No valid matrix
    
    # Count fixed elements
    fixed_count = 0
    for i in range(n):
        for j in range(n):
            val = matrices[0][i][j]
            all_same = all(m[i][j] == val for m in matrices)
            if all_same:
                fixed_count += 1
    
    return fixed_count


def solve():
    n, q = map(int, input().split())
    queries = []
    for _ in range(q):
        queries.append(int(input()))
    
    # Find all possible numbers of fixed elements
    possible = set()
    
    # Iterate through all possible row sum and column sum vectors
    from itertools import combinations_with_replacement, permutations
    
    # Row sums can be 0 to n
    # Column sums can be 0 to n
    for row_sums in combinations_with_replacement(range(n + 1), n):
        # Check if total is valid
        total = sum(row_sums)
        if total > n * n:
            continue
        
        # Generate all permutations of row sums
        for r_perm in set(permutations(row_sums)):
            # Try all column sum vectors with same total
            for col_sums in combinations_with_replacement(range(n + 1), n):
                if sum(col_sums) != total:
                    continue
                
                for c_perm in set(permutations(col_sums)):
                    # Check if valid matrices exist
                    if can_construct_matrix(n, list(r_perm), list(c_perm)):
                        fixed = count_fixed_elements_brute_force(n, list(r_perm), list(c_perm))
                        if fixed >= 0:
                            possible.add(fixed)
    
    for k in queries:
        if k in possible:
            print("Yes")
        else:
            print("No")


solve()
