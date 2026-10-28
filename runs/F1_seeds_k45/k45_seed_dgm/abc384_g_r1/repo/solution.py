import bisect

def solve():
    N = int(input())
    A = list(map(int, input().split()))
    B = list(map(int, input().split()))
    K = int(input())
    
    for _ in range(K):
        X, Y = map(int, input().split())
        
        # Extract only the first X elements of A and first Y elements of B
        A_sub = A[:X]
        B_sub = B[:Y]
        
        # Sort B_sub for binary search optimization
        B_sub_sorted = sorted(B_sub)
        
        # Precompute prefix sum for B_sub_sorted
        B_sub_prefix = [0]
        for b in B_sub_sorted:
            B_sub_prefix.append(B_sub_prefix[-1] + b)
        
        total = 0
        
        # For each element in A_sub, sum the absolute differences with all elements in B_sub
        for a in A_sub:
            # Find the position where a would be inserted in B_sub_sorted (binary search)
            pos = bisect.bisect_left(B_sub_sorted, a)
            
            # Sum of (a - b) for all b < a (i.e., b in B_sub_sorted[0:pos])
            # = a * pos - sum(B_sub_sorted[0:pos])
            sum_less = a * pos - B_sub_prefix[pos]
            
            # Sum of (b - a) for all b >= a (i.e., b in B_sub_sorted[pos:Y])
            # = sum(B_sub_sorted[pos:Y]) - a * (Y - pos)
            sum_greater = B_sub_prefix[Y] - B_sub_prefix[pos] - a * (Y - pos)
            
            total += sum_less + sum_greater
        
        print(total)

solve()
