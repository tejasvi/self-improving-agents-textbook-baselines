# Write your solution here. Read from stdin, write to stdout.

import heapq

def solve():
    N, K, P = map(int, input().split())
    
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        params = tuple(line[1:K+1])
        plans.append((cost, params))
    
    # DP approach using Dijkstra's algorithm
    # State: tuple of parameter values (capped at P)
    # Goal: reach state where all parameters >= P
    
    # Initial state: all parameters are 0
    initial_state = tuple([0] * K)
    
    # Goal state: all parameters are at least P
    goal_state = tuple([P] * K)
    
    # Dictionary to store minimum cost to reach each state
    min_cost = {initial_state: 0}
    
    # Priority queue: (cost, state)
    pq = [(0, initial_state)]
    
    while pq:
        cost, state = heapq.heappop(pq)
        
        # Skip if we've found a better path to this state
        if cost > min_cost.get(state, float('inf')):
            continue
        
        # Check if we reached the goal
        if state == goal_state:
            print(cost)
            return
        
        # Try executing each plan from current state
        for plan_cost, plan_params in plans:
            # Calculate new state after executing this plan
            new_state = tuple([
                min(state[j] + plan_params[j], P)
                for j in range(K)
            ])
            
            new_cost = cost + plan_cost
            
            # Update if this is a better path to the new state
            if new_cost < min_cost.get(new_state, float('inf')):
                min_cost[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))
    
    # If we exit the loop without finding the goal, it's impossible
    print(-1)

solve()
