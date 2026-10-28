# Write your solution here. Read from stdin, write to stdout.

def solve():
    # Read input
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        params = tuple(line[1+j] for j in range(K))
        plans.append((cost, params))
    
    # Use recursion with memoization
    # State: (current_plan_index, current_params)
    # We try taking each plan starting from index or not taking it
    
    # Actually, simpler approach: DFS exploring all subsets with pruning
    min_cost = [float('inf')]  # Using list to make it mutable in nested function
    
    def dfs(used_mask, params, cost):
        # Check if goal is reached
        if all(params[j] >= P for j in range(K)):
            min_cost[0] = min(min_cost[0], cost)
            return
        
        # Pruning
        if cost >= min_cost[0]:
            return
        
        # Try each unused plan
        for i in range(N):
            if used_mask & (1 << i):
                continue
            
            plan_cost, plan_params = plans[i]
            new_params = tuple(params[j] + plan_params[j] for j in range(K))
            new_mask = used_mask | (1 << i)
            
            dfs(new_mask, new_params, cost + plan_cost)
    
    if N <= 20:
        # Use bitmask DFS
        dfs(0, tuple([0] * K), 0)
    else:
        # For larger N, we need a different approach
        # Use frozenset to track used plans
        memo = {}
        
        def dfs_large(used_set, params):
            key = (frozenset(used_set), params)
            if key in memo:
                return memo[key]
            
            # Check if goal
            if all(params[j] >= P for j in range(K)):
                return 0
            
            best = float('inf')
            
            # Try each unused plan
            for i in range(N):
                if i in used_set:
                    continue
                
                plan_cost, plan_params = plans[i]
                new_params = tuple(params[j] + plan_params[j] for j in range(K))
                new_used = used_set | {i}
                
                rest_cost = dfs_large(new_used, new_params)
                if rest_cost != float('inf'):
                    best = min(best, plan_cost + rest_cost)
            
            memo[key] = best
            return best
        
        result = dfs_large(set(), tuple([0] * K))
        if result == float('inf'):
            print(-1)
        else:
            print(result)
        return
    
    if min_cost[0] == float('inf'):
        print(-1)
    else:
        print(min_cost[0])

solve()
