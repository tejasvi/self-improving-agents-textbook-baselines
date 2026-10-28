import sys
from collections import defaultdict

def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    # H must be at least the maximum of U_i + D_i
    min_H = max(u + d for u, d in teeth)
    
    # For a given H:
    # - U'_i + D'_i = H
    # - D'_i = H - U'_i
    # - We need 0 < D'_i <= D_i, so 0 < H - U'_i <= D_i
    #   => H - D_i <= U'_i < H
    # - We also need 0 <= U'_i <= U_i
    # - So max(0, H - D_i) <= U'_i <= min(H-1, U_i)
    # 
    # Cost = sum of reductions = sum(U_i - U'_i) + sum(D_i - D'_i)
    #      = sum(U_i - U'_i) + sum(D_i - (H - U'_i))
    #      = sum(U_i + D_i) - N*H
    
    def can_achieve_H(H):
        # Check if we can make teeth fit with this H using DP on intervals
        min_u = [max(0, H - d) for u, d in teeth]
        max_u = [min(H - 1, u) for u, d in teeth]
        
        # Check if basic constraints are satisfiable
        for i in range(N):
            if min_u[i] > max_u[i]:
                return False
        
        # DP: maintain the range of achievable values at each position
        curr_min = min_u[0]
        curr_max = max_u[0]
        
        for i in range(1, N):
            next_min_u = min_u[i]
            next_max_u = max_u[i]
            
            # From [curr_min, curr_max], reachable range at next position with constraint |diff| <= X
            reachable_min = curr_min - X
            reachable_max = curr_max + X
            
            # Intersect with required range [next_min_u, next_max_u]
            new_min = max(next_min_u, reachable_min)
            new_max = min(next_max_u, reachable_max)
            
            if new_min > new_max:
                return False
            
            curr_min = new_min
            curr_max = new_max
        
        return True
    
    # Binary search for minimum valid H
    # Upper bound: sum of all original lengths
    left = min_H
    right = min_H + sum(u + d for u, d in teeth)
    
    answer = float('inf')
    
    while left <= right:
        mid = (left + right) // 2
        if can_achieve_H(mid):
            answer = min(answer, mid * N - sum(u + d for u, d in teeth))
            right = mid - 1
        else:
            left = mid + 1
    
    print(answer)

solve()
