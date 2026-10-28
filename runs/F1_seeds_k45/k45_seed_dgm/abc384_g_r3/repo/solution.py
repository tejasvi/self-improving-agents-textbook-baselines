import bisect

# Read input
N = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))
K = int(input())

# Preprocess B: sort it and create prefix sum for efficient computation
B_sorted = sorted(B)
B_prefix = [0] * (N + 1)
for i in range(N):
    B_prefix[i + 1] = B_prefix[i] + B_sorted[i]

# For each query
for _ in range(K):
    X, Y = map(int, input().split())
    
    total = 0
    
    # Sum |A_i - B_j| for i in [1, X] and j in [1, Y]
    # We use the sorted B array but only consider first Y elements
    for i in range(X):
        a_val = A[i]
        
        # Find how many elements in B[:Y] are <= a_val
        # We use bisect on B_sorted[:Y]
        pos = bisect.bisect_right(B_sorted, a_val, 0, Y)
        
        # Count of elements <= a_val in B[:Y]
        count_le = pos
        # Count of elements > a_val in B[:Y]
        count_gt = Y - pos
        
        # Sum of B_j where B_j <= a_val (first 'pos' elements in B_sorted[:Y])
        sum_le = B_prefix[pos]
        
        # Sum of B_j where B_j > a_val (elements from pos to Y in B_sorted)
        sum_gt = B_prefix[Y] - B_prefix[pos]
        
        # Contribution: sum of (a_val - B_j) for B_j <= a_val
        #            + sum of (B_j - a_val) for B_j > a_val
        contribution = (a_val * count_le - sum_le) + (sum_gt - a_val * count_gt)
        total += contribution
    
    print(total)
