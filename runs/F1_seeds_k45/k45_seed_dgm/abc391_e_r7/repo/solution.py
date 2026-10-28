# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    A = input().strip()
    
    # Convert string to list of integers
    bits = [int(x) for x in A]
    
    def majority(children):
        """Return majority value among 3 children"""
        if sum(children) >= 2:
            return 1
        else:
            return 0
    
    # levels[i] contains all nodes at level i
    # Each node is represented by a tuple (value, cost_to_flip)
    
    levels = []
    
    # Level 0: just the bits themselves
    # Cost to flip each bit is 1
    level_0 = [(bits[i], 1) for i in range(len(bits))]
    levels.append(level_0)
    
    # Build levels 1 to N
    for level_num in range(1, N + 1):
        prev_level = levels[-1]
        current_level = []
        
        # Process groups of 3 from previous level
        for group_idx in range(len(prev_level) // 3):
            i = group_idx * 3
            child0_val, child0_cost = prev_level[i]
            child1_val, child1_cost = prev_level[i + 1]
            child2_val, child2_cost = prev_level[i + 2]
            
            # Current node's value is majority of children
            current_val = majority([child0_val, child1_val, child2_val])
            
            # To flip from current_val to 1-current_val:
            # We need at least 2 children to equal 1-current_val
            target_val = 1 - current_val
            
            children = [
                (child0_val, child0_cost),
                (child1_val, child1_cost),
                (child2_val, child2_cost)
            ]
            
            min_flip_cost = float('inf')
            
            # Try each pair of children
            for i_idx in range(3):
                for j_idx in range(i_idx + 1, 3):
                    cost = 0
                    for k in range(3):
                        val, flip_cost = children[k]
                        if k == i_idx or k == j_idx:
                            # This child should be target_val
                            if val != target_val:
                                cost += flip_cost
                        # else: child can be anything (no additional cost)
                    min_flip_cost = min(min_flip_cost, cost)
            
            # Also try flipping all 3 children
            cost = sum(flip_cost for val, flip_cost in children if val != target_val)
            min_flip_cost = min(min_flip_cost, cost)
            
            current_level.append((current_val, min_flip_cost))
        
        levels.append(current_level)
    
    # The root is at levels[N][0]
    root_val, root_flip_cost = levels[N][0]
    print(root_flip_cost)

solve()
