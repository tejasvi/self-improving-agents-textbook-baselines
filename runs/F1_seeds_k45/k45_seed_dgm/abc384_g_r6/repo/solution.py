import bisect

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    for _ in range(K):
        X, Y = map(int, input().split())
        
        # Get the first X elements of A and first Y elements of B
        A_slice = A[:X]
        B_slice = sorted(B[:Y])
        
        # Compute prefix sum for B_slice
        B_slice_prefix = [0] * (Y + 1)
        for i in range(Y):
            B_slice_prefix[i + 1] = B_slice_prefix[i] + B_slice[i]
        
        # For each A_i (i from 0 to X-1), compute sum of |A_i - B_j| for j from 0 to Y-1
        total = 0
        for a_val in A_slice:
            # Find how many B values are < a_val
            # Using binary search on B_slice
            pos = bisect.bisect_left(B_slice, a_val)
            
            # Sum of (a_val - B_j) for B_j < a_val
            # = a_val * pos - sum(B_j for B_j < a_val)
            sum_less = B_slice_prefix[pos]
            contribution_less = a_val * pos - sum_less
            
            # Sum of (B_j - a_val) for B_j >= a_val
            # = sum(B_j for B_j >= a_val) - a_val * (Y - pos)
            sum_greater_equal = B_slice_prefix[Y] - sum_less
            contribution_greater_equal = sum_greater_equal - a_val * (Y - pos)
            
            total += contribution_less + contribution_greater_equal
        
        print(total)

solve()
