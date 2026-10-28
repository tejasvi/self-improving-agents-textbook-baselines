from itertools import combinations

def count_fixed_elements(row_sums, col_sums, N):
    """
    Count the number of fixed elements for a given row and column sum configuration.
    An element at (i, j) is fixed if it must have the same value in all matrices
    with the given row and column sums.
    """
    fixed = 0
    
    for i in range(N):
        for j in range(N):
            # An element (i, j) is forced to be 1 if:
            # row_sum[i] + col_sum[j] > N
            # because we need more 1s than can fit without this position
            
            # An element (i, j) is forced to be 0 if:
            # row_sum[i] + col_sum[j] <= N and row_sum[i] + col_sum[j] < N
            # Actually: forced to 0 if row_sum[i] + col_sum[j] < N... not quite
            
            # Better characterization:
            # Element (i, j) is forced to 1 iff:
            # min(remaining_positions_in_row, remaining_positions_in_col) < required_ones
            # Which simplifies to: row_sums[i] + col_sums[j] > N
            
            if row_sums[i] + col_sums[j] > N:
                # Forced to be 1
                fixed += 1
            elif row_sums[i] + col_sums[j] <= N and row_sums[i] + col_sums[j] + (N - 1) >= N:
                # Could be either 0 or 1 (needs more careful analysis)
                # For now, let's use a more careful check
                pass
    
    return fixed

def can_form_matrix(row_sums, col_sums, N):
    """Check if a binary matrix can be formed with given row and column sums."""
    return sum(row_sums) == sum(col_sums)

def generate_partitions(N, max_val=None):
    """Generate all partitions of N with parts of size at most max_val."""
    if max_val is None:
        max_val = N
    
    if N == 0:
        yield []
        return
    
    for i in range(min(N, max_val), 0, -1):
        for partition in generate_partitions(N - i, i):
            yield [i] + partition

def solve():
    line = input().split()
    N = int(line[0])
    Q = int(line[1])
    
    queries = []
    for _ in range(Q):
        K = int(input())
        queries.append(K)
    
    # For small N, we can enumerate configurations
    # The key insight: we need to generate all valid (row_sums, col_sums) pairs
    # and for each, count how many elements are forced
    
    possible_counts = set()
    
    # Generate all possible row sum sequences (multisets of size N, each element 0..N)
    def generate_sequences(N):
        """Generate all non-increasing sequences of N elements, each 0..N"""
        def gen(pos, current):
            if pos == N:
                yield current[:]
                return
            start = current[-1] if current else N
            for val in range(start, -1, -1):
                current.append(val)
                yield from gen(pos + 1, current)
                current.pop()
        
        yield from gen(0, [])
    
    seen_configs = set()
    
    for row_sums in generate_sequences(N):
        row_sum_total = sum(row_sums)
        for col_sums in generate_sequences(N):
            col_sum_total = sum(col_sums)
            
            if row_sum_total != col_sum_total:
                continue
            
            config = (tuple(row_sums), tuple(col_sums))
            if config in seen_configs:
                continue
            seen_configs.add(config)
            
            # Count fixed elements
            fixed = 0
            for i in range(N):
                for j in range(N):
                    # Element (i, j) is forced to 1 if row_sums[i] + col_sums[j] > N
                    if row_sums[i] + col_sums[j] > N:
                        fixed += 1
            
            possible_counts.add(fixed)
    
    # Answer queries
    for K in queries:
        if K in possible_counts:
            print("Yes")
        else:
            print("No")

solve()
