def exists_matrix(row_sums, col_sums, forbidden_ones=None, forbidden_zeros=None):
    """
    Check if a binary matrix exists with given row/col sums,
    with certain positions forbidden from being 0 or 1.
    
    forbidden_ones: set of (i,j) that must be 0
    forbidden_zeros: set of (i,j) that must be 1
    """
    if forbidden_ones is None:
        forbidden_ones = set()
    if forbidden_zeros is None:
        forbidden_zeros = set()
    
    n = len(row_sums)
    
    # Quick check
    if sum(row_sums) != sum(col_sums):
        return False
    
    # Apply forced constraints
    row_needs = list(row_sums)
    col_needs = list(col_sums)
    
    # forbidden_zeros means position MUST be 1
    for i, j in forbidden_zeros:
        row_needs[i] -= 1
        col_needs[j] -= 1
    
    if any(x < 0 for x in row_needs) or any(x < 0 for x in col_needs):
        return False
    
    # Now we need to place remaining ones in positions not in forbidden_ones
    # This is a matching problem
    
    # Use a greedy/backtracking approach
    matrix = [[0] * n for _ in range(n)]
    
    # Set forced 1s
    for i, j in forbidden_zeros:
        matrix[i][j] = 1
    
    # Try to fill remaining
    def backtrack(pos):
        if pos == n * n:
            # Check if all constraints satisfied
            for i in range(n):
                if sum(matrix[i]) != row_sums[i]:
                    return False
            for j in range(n):
                if sum(matrix[i][j] for i in range(n)) != col_sums[j]:
                    return False
            return True
        
        i = pos // n
        j = pos % n
        
        if matrix[i][j] == 1:  # Already set as forced 1
            return backtrack(pos + 1)
        
        if (i, j) in forbidden_ones:  # Must be 0
            matrix[i][j] = 0
            return backtrack(pos + 1)
        
        # Try 0
        matrix[i][j] = 0
        row_sum = sum(matrix[i])
        col_sum = sum(matrix[k][j] for k in range(n))
        
        # Check feasibility
        remaining_cols_in_row = n - j - 1
        remaining_rows_in_col = n - i - 1
        
        if row_sum <= row_sums[i] and col_sum <= col_sums[j] and \
           row_sum + remaining_cols_in_row >= row_sums[i] and \
           col_sum + remaining_rows_in_col >= col_sums[j]:
            if backtrack(pos + 1):
                return True
        
        # Try 1
        matrix[i][j] = 1
        row_sum = sum(matrix[i])
        col_sum = sum(matrix[k][j] for k in range(n))
        
        if row_sum <= row_sums[i] and col_sum <= col_sums[j] and \
           row_sum + remaining_cols_in_row >= row_sums[i] and \
           col_sum + remaining_rows_in_col >= col_sums[j]:
            if backtrack(pos + 1):
                return True
        
        matrix[i][j] = 0
        return False
    
    return backtrack(0)


def count_fixed_elements(row_sums, col_sums):
    """Count fixed elements for given row and column sums."""
    n = len(row_sums)
    fixed = 0
    
    for i in range(n):
        for j in range(n):
            # Can this position be 1?
            can_be_1 = exists_matrix(row_sums, col_sums, forbidden_ones=set(), forbidden_zeros={(i, j)})
            
            # Can this position be 0?
            can_be_0 = exists_matrix(row_sums, col_sums, forbidden_ones={(i, j)}, forbidden_zeros=set())
            
            # If only one option exists, it's fixed
            if can_be_1 and not can_be_0:
                fixed += 1
            elif can_be_0 and not can_be_1:
                fixed += 1
    
    return fixed


def solve(n, queries):
    """Find all possible numbers of fixed elements."""
    possible_k = set()
    
    from itertools import product
    
    # Enumerate all row/col sum combinations
    for row_sums_tuple in product(range(n + 1), repeat=n):
        row_sum = sum(row_sums_tuple)
        
        for col_sums_tuple in product(range(n + 1), repeat=n):
            if sum(col_sums_tuple) != row_sum:
                continue
            
            row_sums = list(row_sums_tuple)
            col_sums = list(col_sums_tuple)
            
            # Check if this configuration is realizable
            if exists_matrix(row_sums, col_sums):
                k = count_fixed_elements(row_sums, col_sums)
                possible_k.add(k)
    
    # Answer queries
    for k in queries:
        print("Yes" if k in possible_k else "No")


# Read input
n, q = map(int, input().split())
queries = []
for _ in range(q):
    queries.append(int(input()))

solve(n, queries)
