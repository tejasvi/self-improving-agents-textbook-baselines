# Write your solution here. Read from stdin, write to stdout.
import bisect

def solve():
    # Read input
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    # For each query
    for _ in range(K):
        X, Y = map(int, input().split())
        
        # We need to sum |A_i - B_j| for i in [1, X] and j in [1, Y]
        # Get the first Y elements of B and sort them
        B_Y = sorted(B[:Y])
        
        # Precompute prefix sum for B_Y
        B_prefix = [0]
        for b in B_Y:
            B_prefix.append(B_prefix[-1] + b)
        B_Y_sum = B_prefix[Y]
        
        total = 0
        
        # For each A_i where i in [1, X]
        for i in range(X):
            a_val = A[i]
            
            # Find how many B_j values are less than a_val
            pos = bisect.bisect_left(B_Y, a_val)
            
            # Sum of (a_val - B_j) for j where B_j < a_val
            sum_less = pos * a_val - B_prefix[pos]
            
            # Sum of (B_j - a_val) for j where B_j >= a_val
            sum_greater = (B_Y_sum - B_prefix[pos]) - (Y - pos) * a_val
            
            total += sum_less + sum_greater
        
        print(total)

solve()
