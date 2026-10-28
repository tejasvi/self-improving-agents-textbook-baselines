def solve():
    N = int(input())
    A = input().strip()
    
    # Convert string to list of integers for easier manipulation
    bits = [int(b) for b in A]
    
    def majority(b1, b2, b3):
        """Return the majority value of 3 bits"""
        return 1 if b1 + b2 + b3 >= 2 else 0
    
    def get_final_value(current):
        """Get the final value after applying operations"""
        current = list(current)
        while len(current) > 1:
            next_level = []
            for i in range(0, len(current), 3):
                maj = majority(current[i], current[i+1], current[i+2])
                next_level.append(maj)
            current = next_level
        return current[0]
    
    final_value = get_final_value(bits)
    target_value = 1 - final_value  # We want to flip to the opposite
    
    memo = {}
    
    def get_min_cost_for_group(b1, b2, b3, target_maj):
        """
        Given 3 bits, find minimum flips to make their majority = target_maj
        """
        current_sum = b1 + b2 + b3
        current_maj = 1 if current_sum >= 2 else 0
        
        if current_maj == target_maj:
            return 0
        
        # Need to change current_maj to target_maj
        if target_maj == 1:
            # Need sum >= 2, currently sum <= 1
            # Need to flip enough 0s to 1s
            return 2 - current_sum
        else:
            # Need sum < 2, currently sum >= 2
            # Need to flip enough 1s to 0s
            return current_sum - 1
    
    def min_cost_to_reach(level_bits, target):
        """
        Given bits at a level, find minimum flips to make final result = target.
        level_bits: tuple of bits
        target: target final value (0 or 1)
        """
        if len(level_bits) == 1:
            # Base case: single bit
            if level_bits[0] == target:
                return 0
            else:
                return 1
        
        key = (level_bits, target)
        if key in memo:
            return memo[key]
        
        # Divide into groups of 3 and compute next level
        groups = []
        for i in range(0, len(level_bits), 3):
            groups.append((level_bits[i], level_bits[i+1], level_bits[i+2]))
        
        num_groups = len(groups)
        
        # DP to find minimum cost
        # dp[i][bits_tuple] = minimum cost to process first i groups
        # with next_level = bits_tuple
        
        # Use recursion with memoization
        dp_memo = {}
        
        def helper(group_idx, next_bits_so_far):
            """
            group_idx: which group we're processing (0 to num_groups-1)
            next_bits_so_far: tuple of bits we've decided for next level
            """
            if group_idx == num_groups:
                # All groups processed, recursively compute cost for next level
                return min_cost_to_reach(next_bits_so_far, target)
            
            key = (group_idx, next_bits_so_far)
            if key in dp_memo:
                return dp_memo[key]
            
            b1, b2, b3 = groups[group_idx]
            
            min_cost = float('inf')
            # Try making this group's majority 0
            cost_0 = get_min_cost_for_group(b1, b2, b3, 0)
            min_cost = min(min_cost, cost_0 + helper(group_idx + 1, next_bits_so_far + (0,)))
            
            # Try making this group's majority 1
            cost_1 = get_min_cost_for_group(b1, b2, b3, 1)
            min_cost = min(min_cost, cost_1 + helper(group_idx + 1, next_bits_so_far + (1,)))
            
            dp_memo[key] = min_cost
            return min_cost
        
        result = helper(0, ())
        memo[key] = result
        return result
    
    result = min_cost_to_reach(tuple(bits), target_value)
    print(result)

solve()
