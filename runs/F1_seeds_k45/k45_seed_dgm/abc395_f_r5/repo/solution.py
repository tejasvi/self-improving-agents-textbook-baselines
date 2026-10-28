import sys
from collections import defaultdict

def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    # Collect all possible values for H
    # H must be at least max of all (U_i or D_i) since we can only reduce
    # H can be at most the maximum of (U_i + D_i)
    possible_H = set()
    
    # Consider H values based on each original sum and reductions
    for u, d in teeth:
        h = u + d
        possible_H.add(h)
        # Also try reducing one side
        for reduction in range(1, min(u, d) + 1):
            possible_H.add(h - reduction)
    
    # Limit the search space - H should not be too small
    min_h = max(max(u, d) for u, d in teeth)
    possible_H = {h for h in possible_H if h >= min_h}
    
    min_cost = float('inf')
    
    for H in possible_H:
        # Try to achieve this H with DP
        # dp[u_val] = minimum cost when current upper tooth has length u_val
        
        dp = defaultdict(lambda: float('inf'))
        
        # Initialize for first tooth
        u0, d0 = teeth[0]
        
        # Try all possible values for first upper tooth
        for u_new in range(0, u0 + 1):
            d_new = H - u_new
            
            # Check if this is valid
            if d_new < 0 or d_new > d0:
                continue
            
            cost = (u0 - u_new) + (d0 - d_new)
            dp[u_new] = cost
        
        # Process remaining teeth
        for i in range(1, N):
            ui, di = teeth[i]
            new_dp = defaultdict(lambda: float('inf'))
            
            # For each possible value of current upper tooth
            for u_new in range(0, ui + 1):
                d_new = H - u_new
                
                # Check if this is valid
                if d_new < 0 or d_new > di:
                    continue
                
                cost = (ui - u_new) + (di - d_new)
                
                # Try transitions from previous states
                for u_prev in dp:
                    if dp[u_prev] == float('inf'):
                        continue
                    
                    # Check constraint |u_prev - u_new| <= X
                    if abs(u_prev - u_new) <= X:
                        new_cost = dp[u_prev] + cost
                        new_dp[u_new] = min(new_dp[u_new], new_cost)
            
            dp = new_dp
        
        # Find minimum cost for this H
        if dp:
            min_cost = min(min_cost, min(dp.values()))
    
    return min_cost

print(solve())
