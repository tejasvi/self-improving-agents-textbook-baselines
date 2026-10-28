import bisect

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    # For each query
    for _ in range(K):
        X_k, Y_k = map(int, input().split())
        
        # We need sum of |A_i - B_j| for i in [0, X_k) and j in [0, Y_k)
        # Use only first X_k elements of A and first Y_k elements of B
        A_subset = A[:X_k]
        B_subset = sorted(B[:Y_k])
        
        # Precompute prefix sum for B_subset
        prefix = [0] * (Y_k + 1)
        for i in range(Y_k):
            prefix[i + 1] = prefix[i] + B_subset[i]
        
        total = 0
        
        # For each A_i, compute its contribution
        for a_val in A_subset:
            # Find position where a_val would be inserted in B_subset
            # This gives us count of elements < a_val
            pos = bisect.bisect_left(B_subset, a_val)
            
            # Elements in B_subset[0:pos] are < a_val
            # Elements in B_subset[pos:] are >= a_val
            
            sum_less = prefix[pos]  # sum of elements < a_val
            sum_greater = prefix[Y_k] - prefix[pos]  # sum of elements >= a_val
            count_less = pos
            count_greater = Y_k - pos
            
            contribution = a_val * count_less - sum_less + sum_greater - a_val * count_greater
            total += contribution
        
        print(total)

solve()
