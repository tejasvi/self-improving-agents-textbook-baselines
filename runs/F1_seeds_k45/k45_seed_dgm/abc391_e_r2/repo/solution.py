def solve():
    N = int(input())
    A = list(map(int, input().split()))
    
    def majority(*values):
        """Return the majority value among 3 values"""
        count_ones = sum(values)
        return 1 if count_ones >= 2 else 0
    
    memo = {}
    
    def min_cost_to_flip(indices, level, target_value):
        """
        Calculate minimum cost to make a group at given level have target_value.
        indices: tuple of starting indices for each position at the previous level
        level: current level (0 = leaf/original array A, higher = more aggregated)
        target_value: desired value (0 or 1)
        
        Returns: minimum number of changes needed
        """
        if level == 0:
            # Base case: at leaf level, these are actual array positions
            cost = 0
            for idx in indices:
                if A[idx] != target_value:
                    cost += 1
            return cost
        
        # At level > 0, we need to choose values for 3 children (previous level)
        # such that their majority equals target_value
        # and the total cost is minimized
        
        min_cost = float('inf')
        
        # Try all 8 combinations of child values
        for c0 in [0, 1]:
            for c1 in [0, 1]:
                for c2 in [0, 1]:
                    # Check if this combination's majority equals target_value
                    if majority(c0, c1, c2) == target_value:
                        # Calculate cost to achieve this configuration
                        child_indices = tuple(indices)  # Each index represents a position at prev level
                        cost = 0
                        cost += min_cost_to_flip((indices[0],), level - 1, c0)
                        cost += min_cost_to_flip((indices[1],), level - 1, c1)
                        cost += min_cost_to_flip((indices[2],), level - 1, c2)
                        min_cost = min(min_cost, cost)
        
        return min_cost
    
    # Build tree recursively
    # At level L, position i represents a group starting at position i*3^L in the original array
    
    def min_changes(pos, level, target):
        """
        pos: position at current level
        level: current level (0 = original array)
        target: target value
        
        Returns: minimum changes to make this position have target value
        """
        key = (pos, level, target)
        if key in memo:
            return memo[key]
        
        if level == 0:
            # Base case: leaf node
            result = 0 if A[pos] == target else 1
            memo[key] = result
            return result
        
        # This position spans 3 child positions at level-1
        # Child positions: 3*pos, 3*pos+1, 3*pos+2
        min_cost = float('inf')
        
        # Try all 8 combinations of child values
        for c0 in [0, 1]:
            for c1 in [0, 1]:
                for c2 in [0, 1]:
                    # Check if majority equals target
                    if majority(c0, c1, c2) == target:
                        cost = 0
                        cost += min_changes(3 * pos, level - 1, c0)
                        cost += min_changes(3 * pos + 1, level - 1, c1)
                        cost += min_changes(3 * pos + 2, level - 1, c2)
                        min_cost = min(min_cost, cost)
        
        memo[key] = min_cost
        return min_cost
    
    # First, determine the current final value
    current_value = majority(0, 0, 0)  # dummy, will be overwritten
    
    # Simulate the majority vote operations to find current value
    temp_A = A[:]
    for _ in range(N):
        new_A = []
        for i in range(len(temp_A) // 3):
            group = temp_A[i*3:(i+1)*3]
            new_A.append(majority(*group))
        temp_A = new_A
    
    current_value = temp_A[0]
    target_value = 1 - current_value
    
    # Calculate minimum cost to flip the final value
    result = min_changes(0, N, target_value)
    print(result)

solve()
