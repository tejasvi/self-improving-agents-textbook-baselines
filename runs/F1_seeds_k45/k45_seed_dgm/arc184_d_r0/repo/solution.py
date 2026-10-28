def solve():
    MOD = 998244353
    n = int(input())
    balls = []
    for _ in range(n):
        x, y = map(int, input().split())
        balls.append((x, y))
    
    # A set is valid if it forms an antichain in the dominance relation
    # Ball i dominates ball j if (x_i < x_j and y_i < y_j) or (x_i > x_j and y_i > y_j)
    # A valid set has no ball dominating another
    
    def dominates(i, j):
        """Check if ball i dominates ball j"""
        xi, yi = balls[i]
        xj, yj = balls[j]
        return (xi < xj and yi < yj) or (xi > xj and yi > yj)
    
    valid_sets = set()
    
    # Iterate through all possible subsets
    for mask in range(1 << n):
        subset = []
        for i in range(n):
            if mask & (1 << i):
                subset.append(i)
        
        # Check if this subset is valid (antichain)
        is_valid = True
        for i in subset:
            for j in subset:
                if i != j and dominates(i, j):
                    is_valid = False
                    break
            if not is_valid:
                break
        
        if is_valid:
            valid_sets.add(tuple(sorted(subset)))
    
    print(len(valid_sets) % MOD)

solve()
