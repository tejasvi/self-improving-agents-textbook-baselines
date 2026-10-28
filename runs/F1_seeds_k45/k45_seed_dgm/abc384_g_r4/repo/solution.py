import bisect

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    # Precompute prefix sums for efficient range queries
    # For B[0:Y_k], we'll compute the sum and count
    
    # For each query, we need sum of |A_i - B_j| for i in [0, X_k-1], j in [0, Y_k-1]
    # We can sort B and use binary search to split into cases where A_i >= B_j and A_i < B_j
    
    # Since we have K queries (up to 10^4) and N is up to 10^5:
    # For each query, we iterate through A[0:X_k] and for each A_i:
    #   - Find how many B[0:Y_k] are <= A_i using binary search
    #   - Sum of B[j] <= A_i: (count * A_i) - (sum of those B_j)
    #   - Sum of B[j] > A_i: (sum of those B_j) - (count * A_i)
    
    for _ in range(K):
        X, Y = map(int, input().split())
        # X, Y are 1-indexed in the problem, but we use 0-indexed
        X -= 1
        Y -= 1
        
        # Get the subsequences
        A_sub = A[:X+1]
        B_sub = B[:Y+1]
        
        # Sort B_sub for binary search
        B_sorted = sorted(B_sub)
        
        # Compute prefix sums of B_sorted
        B_prefix = [0] * (len(B_sorted) + 1)
        for i in range(len(B_sorted)):
            B_prefix[i+1] = B_prefix[i] + B_sorted[i]
        
        total = 0
        for a_val in A_sub:
            # Find the position where a_val would be inserted in B_sorted
            # All B_j < a_val contribute (a_val - B_j)
            # All B_j >= a_val contribute (B_j - a_val)
            
            pos = bisect.bisect_left(B_sorted, a_val)
            
            # Sum of B_j < a_val
            sum_less = B_prefix[pos]
            count_less = pos
            contrib_less = count_less * a_val - sum_less
            
            # Sum of B_j >= a_val
            sum_greater_equal = B_prefix[len(B_sorted)] - B_prefix[pos]
            count_greater_equal = len(B_sorted) - pos
            contrib_greater_equal = sum_greater_equal - count_greater_equal * a_val
            
            total += contrib_less + contrib_greater_equal
        
        print(total)

solve()
