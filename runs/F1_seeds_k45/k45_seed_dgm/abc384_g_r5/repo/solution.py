import bisect

# Read input
N = int(input())
A = list(map(int, input().split()))
B = list(map(int, input().split()))
K = int(input())

# Create sorted versions of A and B for binary search
A_sorted = sorted(A)
B_sorted = sorted(B)

# Precompute prefix sums for sorted sequences
A_prefix = [0]
for a in A_sorted:
    A_prefix.append(A_prefix[-1] + a)

B_prefix = [0]
for b in B_sorted:
    B_prefix.append(B_prefix[-1] + b)

# Process queries
for _ in range(K):
    X, Y = map(int, input().split())
    
    # We need to compute sum of |A_i - B_j| for i in [1, X], j in [1, Y]
    # Using original indices (1-based): A[1..X], B[1..Y]
    
    # For efficiency, we'll iterate through A[0:X] and sum contributions
    total = 0
    
    for i in range(X):
        a_val = A[i]
        
        # Find how many B[0:Y] values are less than a_val
        # Using binary search on B_sorted[0:Y]
        pos = bisect.bisect_left(B_sorted, a_val, hi=Y)
        
        # Count of B values < a_val
        count_less = pos
        # Sum of B values < a_val
        sum_less = B_prefix[pos]
        
        # Sum of B values >= a_val
        sum_greater_eq = B_prefix[Y] - B_prefix[pos]
        count_greater_eq = Y - pos
        
        # Contribution of A[i]:
        # sum of |a_val - B_j| for j in [1, Y]
        # = sum(a_val - B_j) for B_j < a_val + sum(B_j - a_val) for B_j >= a_val
        # = count_less * a_val - sum_less + sum_greater_eq - count_greater_eq * a_val
        
        contribution = count_less * a_val - sum_less + sum_greater_eq - count_greater_eq * a_val
        total += contribution
    
    print(total)
