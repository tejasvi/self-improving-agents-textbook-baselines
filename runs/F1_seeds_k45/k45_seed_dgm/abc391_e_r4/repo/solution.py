def solve():
    N = int(input())
    A = input().strip()
    
    # Memoization for (start, length, target_value) -> minimum cost
    memo = {}
    
    def min_cost(start, length, target):
        """
        Returns the minimum number of flips needed to make substring A[start:start+length]
        evaluate to the target value (0 or 1) after all majority operations.
        """
        if (start, length, target) in memo:
            return memo[(start, length, target)]
        
        # Base case: single character
        if length == 1:
            bit = int(A[start])
            cost = 0 if bit == target else 1
            memo[(start, length, target)] = cost
            return cost
        
        # Recursive case: length = 3^k for k >= 1
        # Split into 3 equal parts
        part_len = length // 3
        
        # For the target to be achieved at this level,
        # we need to consider what the three parts should be
        # such that their majority equals target
        
        min_changes = float('inf')
        
        # Try all 8 combinations of what the three parts should evaluate to
        for v1 in [0, 1]:
            for v2 in [0, 1]:
                for v3 in [0, 1]:
                    # Check if majority of (v1, v2, v3) equals target
                    majority_bit = 1 if (v1 + v2 + v3) >= 2 else 0
                    
                    if majority_bit == target:
                        # This combination works
                        cost = (min_cost(start, part_len, v1) + 
                               min_cost(start + part_len, part_len, v2) + 
                               min_cost(start + 2*part_len, part_len, v3))
                        min_changes = min(min_changes, cost)
        
        memo[(start, length, target)] = min_changes
        return min_changes
    
    # Determine what the original evaluates to
    def get_value(start, length):
        if length == 1:
            return int(A[start])
        
        part_len = length // 3
        v1 = get_value(start, part_len)
        v2 = get_value(start + part_len, part_len)
        v3 = get_value(start + 2*part_len, part_len)
        
        # Majority
        return 1 if (v1 + v2 + v3) >= 2 else 0
    
    original_value = get_value(0, len(A))
    
    # The answer is the cost to flip to the opposite value
    if original_value == 0:
        result = min_cost(0, len(A), 1)
    else:
        result = min_cost(0, len(A), 0)
    
    print(result)

solve()
