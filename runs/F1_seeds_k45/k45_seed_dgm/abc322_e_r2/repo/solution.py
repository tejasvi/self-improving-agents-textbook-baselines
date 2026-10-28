import heapq
from collections import defaultdict

def solve():
    # Read input
    N, K, P = map(int, input().split())
    plans = []
    for _ in range(N):
        line = list(map(int, input().split()))
        cost = line[0]
        improvements = line[1:]
        plans.append((cost, improvements))
    
    # Use Dijkstra's algorithm to find minimum cost to reach each state
    # State is a tuple of parameter values (capped at P for each parameter)
    # We only care about reaching P for each parameter
    
    initial_state = tuple([0] * K)
    
    # Priority queue: (cost, state)
    pq = [(0, initial_state)]
    
    # Dictionary to track minimum cost to reach each state
    visited = {}
    visited[initial_state] = 0
    
    # Target state: all parameters at least P
    target = tuple([P] * K)
    
    min_cost = float('inf')
    
    while pq:
        cost, state = heapq.heappop(pq)
        
        # If we reached the target state, update answer
        if state == target:
            min_cost = cost
            break
        
        # Skip if we've found a better path to this state
        if visited.get(state, float('inf')) < cost:
            continue
        
        # Try executing each plan
        for plan_cost, improvements in plans:
            # Calculate new state
            new_state = tuple([
                min(state[j] + improvements[j], P) 
                for j in range(K)
            ])
            
            new_cost = cost + plan_cost
            
            # If this is a better path to the new state, add to queue
            if new_cost < visited.get(new_state, float('inf')):
                visited[new_state] = new_cost
                heapq.heappush(pq, (new_cost, new_state))
    
    if min_cost == float('inf'):
        print(-1)
    else:
        print(min_cost)

solve()
