# Write your solution here. Read from stdin, write to stdout.

def solve():
    N, X = map(int, input().split())
    teeth = []
    for _ in range(N):
        u, d = map(int, input().split())
        teeth.append((u, d))
    
    U = [t[0] for t in teeth]
    D = [t[1] for t in teeth]
    
    # Calculate sum of all U_i + D_i
    total_sum = sum(U[i] + D[i] for i in range(N))
    
    # The cost is sum(U_i + D_i) - N * H where H is the target height
    # We want to maximize H to minimize cost
    
    def can_achieve(H):
        """Check if we can achieve height H with valid tooth lengths"""
        if H < 0:
            return False
        
        # For each tooth i: u_i + d_i = H
        # Constraints: 0 <= u_i <= U_i and 0 <= d_i <= D_i
        # So: 0 <= u_i <= U_i and 0 <= H - u_i <= D_i
        # Which means: max(0, H - D_i) <= u_i <= min(U_i, H)
        
        # Also we need |u_i - u_{i+1}| <= X
        
        # Use DP with ranges to check feasibility
        # Track which u_i values are reachable
        
        # Start with tooth 0
        min_u0 = max(0, H - D[0])
        max_u0 = min(U[0], H)
        
        if min_u0 > max_u0:
            return False
        
        # For each position, we track the valid range of u_i values
        current_min = min_u0
        current_max = max_u0
        
        for i in range(1, N):
            # u_i must satisfy:
            # 1. max(0, H - D_i) <= u_i <= min(U_i, H)
            # 2. |u_i - u_{i-1}| <= X for some valid u_{i-1}
            
            min_ui = max(0, H - D[i])
            max_ui = min(U[i], H)
            
            if min_ui > max_ui:
                return False
            
            # From current range [current_min, current_max], we can reach
            # u_i values in [current_min - X, current_max + X]
            # But u_i must also be in [min_ui, max_ui]
            
            new_min = max(min_ui, current_min - X)
            new_max = min(max_ui, current_max + X)
            
            if new_min > new_max:
                return False
            
            current_min = new_min
            current_max = new_max
        
        return True
    
    # Binary search for maximum valid H
    left, right = 0, total_sum // N + 1
    
    answer_H = 0
    while left <= right:
        mid = (left + right) // 2
        if can_achieve(mid):
            answer_H = mid
            left = mid + 1
        else:
            right = mid - 1
    
    # The cost is sum(U_i + D_i) - N * answer_H
    cost = total_sum - N * answer_H
    print(cost)

solve()
