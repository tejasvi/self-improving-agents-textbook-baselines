# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    U = [teeth[i][0] for i in range(N)]
    D = [teeth[i][1] for i in range(N)]
    
    # The minimum possible H is the maximum of all U_i + D_i
    min_H = max(U[i] + D[i] for i in range(N))
    
    min_cost = float('inf')
    
    # Try H values starting from min_H
    # Key observation: we don't need to try all H values
    # The optimal H should be close to min_H
    
    # Maximum reasonable H: at most min_H + max(U)
    # (going beyond doesn't make sense as we'd reduce too many teeth)
    
    max_H = min_H + max(U)
    
    for H in range(min_H, min(max_H + 1, min_H + 500000)):
        cost = compute_cost_for_H(N, U, D, H, X)
        if cost is not None:
            min_cost = min(min_cost, cost)
            # If cost is 0, we can stop
            if min_cost == 0:
                break
    
    print(min_cost)


def compute_cost_for_H(N, U, D, H, X):
    """
    Compute the minimum cost to achieve sum H with adjacent upper teeth
    differing by at most X. Returns None if impossible.
    
    Uses DP with range compression on upper tooth values.
    """
    # For each position i, the upper tooth must be in range [max(0, H - D_i), U_i]
    ranges = []
    for i in range(N):
        min_val = max(0, H - D[i])
        max_val = U[i]
        if min_val > max_val:
            return None  # Impossible for this H
        ranges.append((min_val, max_val))
    
    # DP: dp[i][v] = minimum cost to satisfy first i+1 positions with tooth i having value v
    # Key insight: we don't need to try all values, only critical ones
    
    # Collect all critical values (boundaries of ranges)
    critical_values = set()
    for min_val, max_val in ranges:
        critical_values.add(min_val)
        critical_values.add(max_val)
    
    # Also add values that connect adjacent ranges
    critical_values.add(ranges[0][0])
    critical_values.add(ranges[0][1])
    
    for i in range(1, N):
        prev_min, prev_max = ranges[i-1]
        curr_min, curr_max = ranges[i]
        
        # Add values within X distance from previous boundaries
        for prev_val in [prev_min, prev_max]:
            critical_values.add(max(curr_min, prev_val - X))
            critical_values.add(min(curr_max, prev_val + X))
    
    # Also add last position boundaries
    critical_values.add(ranges[N-1][0])
    critical_values.add(ranges[N-1][1])
    
    # Filter to only values within valid ranges
    filtered_values = set()
    for i, (min_val, max_val) in enumerate(ranges):
        for v in critical_values:
            if min_val <= v <= max_val:
                filtered_values.add((i, v))
    
    # Now do DP
    from collections import defaultdict
    
    dp = defaultdict(lambda: float('inf'))
    
    # Initialize first position
    for v in critical_values:
        min_val, max_val = ranges[0]
        if min_val <= v <= max_val:
            cost = U[0] - v
            dp[(0, v)] = cost
    
    # Fill DP
    for i in range(1, N):
        new_dp = defaultdict(lambda: float('inf'))
        min_val_i, max_val_i = ranges[i]
        
        for v_curr in critical_values:
            if not (min_val_i <= v_curr <= max_val_i):
                continue
            
            # Find minimum from previous position
            for v_prev in critical_values:
                min_val_prev, max_val_prev = ranges[i-1]
                if not (min_val_prev <= v_prev <= max_val_prev):
                    continue
                
                if (i-1, v_prev) not in dp:
                    continue
                
                if abs(v_curr - v_prev) <= X:
                    cost = dp[(i-1, v_prev)] + (U[i] - v_curr)
                    new_dp[(i, v_curr)] = min(new_dp[(i, v_curr)], cost)
        
        dp.update(new_dp)
    
    # Find answer
    result = float('inf')
    for v in critical_values:
        min_val, max_val = ranges[N-1]
        if min_val <= v <= max_val:
            if (N-1, v) in dp:
                result = min(result, dp[(N-1, v)])
    
    return result if result != float('inf') else None


solve()
