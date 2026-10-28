# Write your solution here. Read from stdin, write to stdout.

def solve():
    N = int(input())
    D = list(map(int, input().split()))
    
    L1, C1, K1 = map(int, input().split())
    L2, C2, K2 = map(int, input().split())
    
    total_cost = 0
    
    # For each section, find the minimum cost to monitor it
    for d in D:
        min_cost = float('inf')
        
        # Try all possible combinations of sensor type 1 and type 2
        # n1 = number of type-1 sensors, n2 = number of type-2 sensors
        # We need n1*L1 + n2*L2 >= d
        
        for n1 in range(K1 + 1):
            # Calculate minimum n2 needed
            remaining = max(0, d - n1 * L1)
            if remaining == 0:
                n2 = 0
            else:
                n2 = (remaining + L2 - 1) // L2  # Ceiling division
            
            if n2 <= K2:
                cost = n1 * C1 + n2 * C2
                min_cost = min(min_cost, cost)
        
        if min_cost == float('inf'):
            print(-1)
            return
        
        total_cost += min_cost
    
    print(total_cost)

solve()
