def solve():
    N, M = map(int, input().split())
    operations = []
    for _ in range(M):
        L, R = map(int, input().split())
        operations.append((L - 1, R - 1))  # 0-indexed
    
    # Use bitmask DP for small N
    if N <= 20:
        # dp[mask] = min_cost to reach this state
        dp = {0: 0}
        parent = {}
        
        for op_idx in range(M):
            L, R = operations[op_idx]
            new_dp = {}
            
            for mask, cost in dp.items():
                # Try operation 0 (do nothing)
                new_mask = mask
                if new_mask not in new_dp or cost < new_dp[new_mask]:
                    new_dp[new_mask] = cost
                    parent[(op_idx, new_mask)] = (mask, 0)
                
                # Try operation 1 (set positions in [L, R] to 1)
                new_mask = mask
                for j in range(L, R + 1):
                    new_mask |= (1 << j)
                new_cost = cost + 1
                if new_mask not in new_dp or new_cost < new_dp[new_mask]:
                    new_dp[new_mask] = new_cost
                    parent[(op_idx, new_mask)] = (mask, 1)
                
                # Try operation 2 (set positions NOT in [L, R] to 1)
                new_mask = mask
                for j in range(N):
                    if j < L or j > R:
                        new_mask |= (1 << j)
                new_cost = cost + 1
                if new_mask not in new_dp or new_cost < new_dp[new_mask]:
                    new_dp[new_mask] = new_cost
                    parent[(op_idx, new_mask)] = (mask, 2)
            
            dp = new_dp
        
        # Find the best final state
        target_mask = (1 << N) - 1
        if target_mask not in dp:
            print(-1)
        else:
            min_cost = dp[target_mask]
            solution = []
            current_mask = target_mask
            for op_idx in range(M - 1, -1, -1):
                prev_mask, choice = parent[(op_idx, current_mask)]
                solution.append(choice)
                current_mask = prev_mask
            
            solution.reverse()
            print(min_cost)
            print(' '.join(map(str, solution)))
    else:
        # For larger N, use backtracking with pruning
        min_cost = [float('inf')]
        best_solution = [None]
        
        # First, try a greedy heuristic to get an upper bound
        def greedy_upper_bound():
            covered = set()
            choices = [0] * M
            cost = 0
            
            # Simple greedy: go through operations and use op1 if it covers new positions
            for i in range(M):
                L, R = operations[i]
                op1_covers = sum(1 for j in range(L, R + 1) if j not in covered)
                op2_covers = sum(1 for j in range(N) if (j < L or j > R) and j not in covered)
                
                if op1_covers > op2_covers and op1_covers > 0:
                    choices[i] = 1
                    for j in range(L, R + 1):
                        covered.add(j)
                    cost += 1
                elif op2_covers > 0:
                    choices[i] = 2
                    for j in range(N):
                        if j < L or j > R:
                            covered.add(j)
                    cost += 1
            
            if len(covered) == N:
                return cost, choices
            return float('inf'), None
        
        ub_cost, ub_solution = greedy_upper_bound()
        if ub_cost < float('inf'):
            min_cost[0] = ub_cost
            best_solution[0] = ub_solution
        
        def backtrack(idx, choices, cost, covered):
            if cost >= min_cost[0]:
                return
            
            if len(covered) == N:
                if cost < min_cost[0]:
                    min_cost[0] = cost
                    best_solution[0] = choices[:]
                return
            
            if idx == M:
                return
            
            # Try operation 0
            backtrack(idx + 1, choices + [0], cost, covered)
            
            # Try operation 1
            L, R = operations[idx]
            new_covered = covered.copy()
            for j in range(L, R + 1):
                new_covered.add(j)
            backtrack(idx + 1, choices + [1], cost + 1, new_covered)
            
            # Try operation 2
            new_covered = covered.copy()
            for j in range(N):
                if j < L or j > R:
                    new_covered.add(j)
            backtrack(idx + 1, choices + [2], cost + 1, new_covered)
        
        backtrack(0, [], 0, set())
        
        if best_solution[0] is None:
            print(-1)
        else:
            print(min_cost[0])
            print(' '.join(map(str, best_solution[0])))

solve()
