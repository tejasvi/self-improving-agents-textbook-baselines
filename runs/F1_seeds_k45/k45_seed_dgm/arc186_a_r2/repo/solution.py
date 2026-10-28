from itertools import combinations

def gale_ryser_check(row_sums, col_sums):
    """Check if a binary matrix with given row and column sums exists."""
    if sum(row_sums) != sum(col_sums):
        return False
    
    r = sorted(row_sums, reverse=True)
    c = sorted(col_sums, reverse=True)
    
    n = len(r)
    
    for k in range(1, n + 1):
        lhs = sum(r[:k])
        rhs = sum(min(i, k) for i in c)
        if lhs > rhs:
            return False
    
    return True


def count_fixed_elements(N, row_sums, col_sums, max_matrices=10000):
    """
    For a given row and column sum configuration, count elements that must be fixed.
    Stops early if we find too many matrices (which would be slow to process).
    """
    if not gale_ryser_check(row_sums, col_sums):
        return None
    
    valid_matrices = []
    
    def backtrack(matrix, row_idx):
        # Early termination if we have too many matrices
        if len(valid_matrices) > max_matrices:
            return
        
        if row_idx == N:
            valid_matrices.append([row[:] for row in matrix])
            return
        
        row_sum = row_sums[row_idx]
        
        for positions in combinations(range(N), row_sum):
            new_row = [0] * N
            for pos in positions:
                new_row[pos] = 1
            
            feasible = True
            for j in range(N):
                col_sum_so_far = sum(matrix[i][j] for i in range(row_idx)) + new_row[j]
                remaining_rows = N - row_idx - 1
                if col_sum_so_far > col_sums[j] or col_sum_so_far + remaining_rows < col_sums[j]:
                    feasible = False
                    break
            
            if feasible:
                matrix.append(new_row)
                backtrack(matrix, row_idx + 1)
                matrix.pop()
    
    backtrack([], 0)
    
    if not valid_matrices:
        return None
    
    # If we hit the limit, we can't reliably count fixed elements
    if len(valid_matrices) > max_matrices:
        return None
    
    if len(valid_matrices) == 1:
        return N * N
    
    fixed_count = 0
    for i in range(N):
        for j in range(N):
            first_val = valid_matrices[0][i][j]
            if all(matrix[i][j] == first_val for matrix in valid_matrices):
                fixed_count += 1
    
    return fixed_count


def solve():
    N, Q = map(int, input().split())
    queries = []
    for _ in range(Q):
        queries.append(int(input()))
    
    possible_counts = set()
    
    # For small N, enumerate systematically
    if N <= 7:
        def enumerate_all():
            def gen_row_sums(idx, row_sums, total):
                if idx == N:
                    gen_col_sums(0, row_sums, [], 0, total)
                    return
                
                for row_sum in range(N + 1):
                    row_sums.append(row_sum)
                    gen_row_sums(idx + 1, row_sums, total + row_sum)
                    row_sums.pop()
            
            def gen_col_sums(col_idx, row_sums, col_sums, current_sum, target_sum):
                if col_idx == N:
                    if current_sum == target_sum:
                        result = count_fixed_elements(N, row_sums, col_sums)
                        if result is not None:
                            possible_counts.add(result)
                    return
                
                remaining_cols = N - col_idx - 1
                for col_sum in range(N + 1):
                    new_sum = current_sum + col_sum
                    if new_sum <= target_sum <= new_sum + remaining_cols * N:
                        col_sums.append(col_sum)
                        gen_col_sums(col_idx + 1, row_sums, col_sums, new_sum, target_sum)
                        col_sums.pop()
            
            gen_row_sums(0, [], 0)
        
        enumerate_all()
    
    # For all N, check specific structured cases
    # These cases often give us good coverage of achievable fixed counts
    
    # Uniform matrices
    for k in range(N + 1):
        result = count_fixed_elements(N, [k] * N, [k] * N)
        if result is not None:
            possible_counts.add(result)
    
    # Permutation matrices (each row and column has exactly one 1)
    # For N >= 2, there are N! permutation matrices
    if N <= 8:
        # Check if permutation matrices are flexible
        row_sums = [1] * N
        col_sums = [1] * N
        result = count_fixed_elements(N, row_sums, col_sums)
        if result is not None:
            possible_counts.add(result)
    
    # Near-uniform: some rows/cols have k, others have k+1
    for k in range(N):
        for num_k in range(N + 1):
            row_sums = [k] * (N - num_k) + [k + 1] * num_k
            
            # Match with column sums
            total = sum(row_sums)
            col_base = total // N
            col_remainder = total % N
            
            if col_base <= N and col_remainder <= N:
                col_sums = [col_base] * (N - col_remainder) + [col_base + 1] * col_remainder
                result = count_fixed_elements(N, row_sums, col_sums)
                if result is not None:
                    possible_counts.add(result)
    
    # Random sampling for larger N
    if N > 7:
        import random
        random.seed(42)
        
        # Try specific patterns
        for trial in range(min(100000, (N**2) * 10)):
            # Generate random valid configuration
            row_sums = [random.randint(0, N) for _ in range(N)]
            total = sum(row_sums)
            
            # Generate col_sums that match total
            col_sums = [0] * N
            remaining = total
            
            for i in range(N - 1):
                max_val = min(N, remaining)
                col_sums[i] = random.randint(0, max_val)
                remaining -= col_sums[i]
            
            col_sums[-1] = remaining
            
            if 0 <= col_sums[-1] <= N:
                result = count_fixed_elements(N, row_sums, col_sums, max_matrices=5000)
                if result is not None:
                    possible_counts.add(result)
    
    for K in queries:
        print("Yes" if K in possible_counts else "No")

solve()
