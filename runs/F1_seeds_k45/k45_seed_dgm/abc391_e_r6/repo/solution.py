# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    A = input().split()
    
    # Convert to list of integers
    A = [int(x) for x in A]
    
    # dp[level][index] = (cost to make 0, cost to make 1)
    # level 0 is the original array, level N is the final single element
    # We'll work bottom-up: from original array to final result
    
    # Initialize with the original array (level 0)
    # cost to keep as is: 0, cost to flip: 1
    current_level = []
    for val in A:
        current_level.append((0 if val == 0 else 1, 1 if val == 0 else 0))
    
    # Apply operations N times
    for level in range(N):
        next_level = []
        # Process groups of 3
        for i in range(0, len(current_level), 3):
            # Get costs for three children
            cost0_0, cost1_0 = current_level[i]
            cost0_1, cost1_1 = current_level[i+1]
            cost0_2, cost1_2 = current_level[i+2]
            
            # Compute cost to make this position 0 or 1
            # Position becomes 0 if majority of children is 0
            # Position becomes 1 if majority of children is 1
            
            # To get majority 0: need at least 2 children to be 0
            # Possibilities: (0,0,0), (0,0,1), (0,1,0), (1,0,0)
            cost_to_0 = min(
                cost0_0 + cost0_1 + cost0_2,  # all 0
                cost0_0 + cost0_1 + cost1_2,  # 0,0,1
                cost0_0 + cost1_1 + cost0_2,  # 0,1,0
                cost1_0 + cost0_1 + cost0_2   # 1,0,0
            )
            
            # To get majority 1: need at least 2 children to be 1
            # Possibilities: (1,1,1), (1,1,0), (1,0,1), (0,1,1)
            cost_to_1 = min(
                cost1_0 + cost1_1 + cost1_2,  # all 1
                cost1_0 + cost1_1 + cost0_2,  # 1,1,0
                cost1_0 + cost0_1 + cost1_2,  # 1,0,1
                cost0_0 + cost1_1 + cost1_2   # 0,1,1
            )
            
            next_level.append((cost_to_0, cost_to_1))
        
        current_level = next_level
    
    # At the end, we have one element with (cost_to_0, cost_to_1)
    cost_to_0, cost_to_1 = current_level[0]
    
    # The current value of A'_1 is determined by majority vote
    # We need to compute what the current final value is
    current_level_values = []
    for val in A:
        current_level_values.append(val)
    
    for level in range(N):
        next_level = []
        for i in range(0, len(current_level_values), 3):
            v0 = current_level_values[i]
            v1 = current_level_values[i+1]
            v2 = current_level_values[i+2]
            majority = 1 if (v0 + v1 + v2) >= 2 else 0
            next_level.append(majority)
        current_level_values = next_level
    
    final_value = current_level_values[0]
    
    # We want to flip the final value
    if final_value == 0:
        # Currently 0, want to make it 1
        print(cost_to_1)
    else:
        # Currently 1, want to make it 0
        print(cost_to_0)

solve()
