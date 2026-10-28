def solve():
    N = int(input())
    A = input().strip()
    
    # Parse input - A is a string of 0s and 1s
    bits = [int(c) for c in A]
    
    # Compute the final value after N operations
    def compute_final(arr, n):
        """Compute final value after n operations"""
        current = arr
        for _ in range(n):
            next_level = []
            for i in range(0, len(current), 3):
                count = sum(current[i:i+3])
                next_level.append(1 if count >= 2 else 0)
            current = next_level
        return current[0]
    
    final_value = compute_final(bits, N)
    target_value = 1 - final_value  # Flip the final value
    
    # Find minimum cost to reach target_value
    # Use recursive function with memoization using (start, length, level, target)
    memo = {}
    
    def min_cost_to_reach(start, length, level, target):
        """
        Find minimum cost to change bits in range [start, start+length)
        at the given level (where level=0 is the base bits, level=N is final result)
        such that after (N-level) operations, the result is target.
        """
        if level == N:
            # At the final level, we have a single bit
            cost = 0 if bits[start] == target else 1
            return cost
        
        key = (start, length, level, target)
        if key in memo:
            return memo[key]
        
        # At this level, we have 'length' bits
        # We need to partition into 3 groups and compute majority
        group_size = length // 3
        
        # Compute what results we need from the 3 groups to get target majority
        # at the current level
        min_total_cost = float('inf')
        
        if target == 1:
            # Need at least 2 groups to return 1
            possible_combinations = [
                (1, 1, 0), (1, 1, 1),
                (1, 0, 1), (0, 1, 1)
            ]
        else:
            # Need at least 2 groups to return 0
            possible_combinations = [
                (0, 0, 1), (0, 0, 0),
                (0, 1, 0), (1, 0, 0)
            ]
        
        for comb in possible_combinations:
            cost1 = min_cost_to_reach(start, group_size, level + 1, comb[0])
            cost2 = min_cost_to_reach(start + group_size, group_size, level + 1, comb[1])
            cost3 = min_cost_to_reach(start + 2*group_size, group_size, level + 1, comb[2])
            total_cost = cost1 + cost2 + cost3
            min_total_cost = min(min_total_cost, total_cost)
        
        memo[key] = min_total_cost
        return min_total_cost
    
    result = min_cost_to_reach(0, len(bits), 0, target_value)
    print(result)

solve()
