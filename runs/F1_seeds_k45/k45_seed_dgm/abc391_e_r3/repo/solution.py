def solve():
    N = int(input())
    A = input().strip()
    
    # Convert string to list of integers
    bits = [int(c) for c in A]
    
    def majority(b1, b2, b3):
        """Return the majority value among three bits"""
        return 1 if (b1 + b2 + b3) >= 2 else 0
    
    # Build up the levels by applying the operation
    levels = [bits]
    for level_num in range(N):
        current = levels[-1]
        next_level = []
        for i in range(0, len(current), 3):
            group = current[i:i+3]
            maj = majority(group[0], group[1], group[2])
            next_level.append(maj)
        levels.append(next_level)
    
    # The final value
    final_value = levels[-1][0]
    target_value = 1 - final_value
    
    # Now we compute minimum cost to achieve each value at each position
    # dp[(level, position, value)] = minimum cost to make position at level have value
    
    dp = {}
    
    # Base case: level 0 (original bits)
    for i in range(len(bits)):
        dp[(0, i, bits[i])] = 0
        dp[(0, i, 1 - bits[i])] = 1
    
    # Forward pass: compute costs for achieving values at each level
    for level_num in range(N):
        current_size = len(levels[level_num])
        next_size = len(levels[level_num + 1])
        
        for i in range(next_size):
            # Position i at level_num+1 depends on positions 3*i, 3*i+1, 3*i+2 at level_num
            idx1, idx2, idx3 = 3*i, 3*i+1, 3*i+2
            
            # Try all combinations of values at the three positions
            for v1 in [0, 1]:
                for v2 in [0, 1]:
                    for v3 in [0, 1]:
                        maj = majority(v1, v2, v3)
                        # Cost to achieve v1, v2, v3 at the three positions
                        cost1 = dp.get((level_num, idx1, v1), float('inf'))
                        cost2 = dp.get((level_num, idx2, v2), float('inf'))
                        cost3 = dp.get((level_num, idx3, v3), float('inf'))
                        total_cost = cost1 + cost2 + cost3
                        
                        if total_cost < float('inf'):
                            key = (level_num + 1, i, maj)
                            if key not in dp:
                                dp[key] = total_cost
                            else:
                                dp[key] = min(dp[key], total_cost)
    
    # The answer is the minimum cost to achieve the opposite of the final value
    answer = dp.get((N, 0, target_value), float('inf'))
    print(answer)

solve()
