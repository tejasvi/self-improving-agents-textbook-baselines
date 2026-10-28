import math

def solve():
    N = int(input())
    D = list(map(int, input().split()))
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    # DP with memoization
    # State: (section_index, sensors_type1_used, sensors_type2_used) -> min_cost
    memo = {}
    
    def dp(section_idx, used1, used2):
        """
        Returns minimum cost to monitor sections from section_idx onwards
        given that we've already used used1 sensors of type1 and used2 sensors of type2
        """
        if section_idx == N:
            return 0
        
        if (section_idx, used1, used2) in memo:
            return memo[(section_idx, used1, used2)]
        
        section_length = D[section_idx]
        result = float('inf')
        
        # Try all combinations of type1 and type2 sensors for this section
        # Maximum sensors of each type we might need for this section
        max_need_type1 = math.ceil(section_length / L1)
        max_need_type2 = math.ceil(section_length / L2)
        
        # Try all combinations of adding sensors
        for add1 in range(max_need_type1 + 1):
            for add2 in range(max_need_type2 + 1):
                # Check if this combination covers the section
                coverage = add1 * L1 + add2 * L2
                if coverage >= section_length:
                    new_used1 = used1 + add1
                    new_used2 = used2 + add2
                    
                    # Check if we exceed maximum allowed
                    if new_used1 <= K1 and new_used2 <= K2:
                        cost = add1 * C1 + add2 * C2
                        future_cost = dp(section_idx + 1, new_used1, new_used2)
                        if future_cost != float('inf'):
                            result = min(result, cost + future_cost)
        
        memo[(section_idx, used1, used2)] = result
        return result
    
    answer = dp(0, 0, 0)
    
    if answer == float('inf'):
        print(-1)
    else:
        print(answer)

solve()
