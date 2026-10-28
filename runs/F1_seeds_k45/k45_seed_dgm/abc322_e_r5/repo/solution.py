import sys
from heapq import heappush, heappop
from collections import defaultdict

def solve():
    line = input().split()
    N, K, P = int(line[0]), int(line[1]), int(line[2])
    
    plans = []
    for _ in range(N):
        line = input().split()
        cost = int(line[0])
        increases = [int(line[i+1]) for i in range(K)]
        plans.append((cost, increases))
    
    # Use Dijkstra's algorithm with states being (cost, parameters_tuple, used_plans_bitmask)
    # parameters_tuple: tuple of current parameter values
    # used_plans_bitmask: which plans have been used
    
    # Since N can be up to 100, using a bitmask might be problematic (2^100)
    # Instead, use (cost, parameters_tuple, frozenset of used plan indices)
    
    initial_params = tuple([0] * K)
    initial_used = frozenset()
    
    # Priority queue: (cost, params_tuple, used_plans_frozenset)
    pq = [(0, initial_params, initial_used)]
    
    # visited[params_tuple][used_plans_frozenset] = min_cost
    # Or visited[(params_tuple, used_plans_frozenset)] = min_cost
    visited = set()
    
    min_cost = float('inf')
    
    while pq:
        cost, params, used_plans = heappop(pq)
        
        # Check if we've reached the goal
        if all(p >= P for p in params):
            min_cost = min(min_cost, cost)
            continue
        
        # Skip if we've visited this state with lower cost
        state = (params, used_plans)
        if state in visited:
            continue
        visited.add(state)
        
        # Try adding each unused plan
        for plan_idx in range(N):
            if plan_idx in used_plans:
                continue
            
            plan_cost, increases = plans[plan_idx]
            new_params = tuple(params[j] + increases[j] for j in range(K))
            new_used = used_plans | frozenset([plan_idx])
            new_cost = cost + plan_cost
            
            # Only add to queue if we haven't visited this state or found a better path
            new_state = (new_params, new_used)
            if new_state not in visited:
                heappush(pq, (new_cost, new_params, new_used))
    
    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)

solve()
