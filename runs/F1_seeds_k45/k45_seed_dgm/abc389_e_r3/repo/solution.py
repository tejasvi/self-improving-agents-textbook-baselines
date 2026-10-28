# Write your solution here. Read from stdin, write to stdout.

def can_buy_k_units(k, prices, M):
    """Check if we can buy exactly k units with budget at most M"""
    # Sort prices to buy from cheapest first (greedy approach)
    sorted_prices = sorted(prices)
    
    total_cost = 0
    remaining_units = k
    
    for price in sorted_prices:
        if remaining_units == 0:
            break
        
        # Binary search for maximum units we can buy from this product
        # given the remaining budget and units
        left, right = 0, remaining_units
        best_units = 0
        
        while left <= right:
            mid = (left + right) // 2
            cost_for_mid = mid * mid * price
            if total_cost + cost_for_mid <= M:
                best_units = mid
                left = mid + 1
            else:
                right = mid - 1
        
        cost = best_units * best_units * price
        total_cost += cost
        remaining_units -= best_units
    
    return total_cost <= M

def solve(N, M, prices):
    """Find maximum units we can buy with budget M"""
    # Binary search on the answer
    # Upper bound: if we could buy from the cheapest product only with cost k^2*p = M,
    # then k = sqrt(M/p). Since we have N products, we can roughly estimate sqrt(M/min(p))
    # But to be safe, let's use a simple upper bound
    min_price = min(prices)
    
    # Maximum possible: if all money goes to cheapest product, we can buy sqrt(M/min_price) units
    # But with multiple products we might do better, so add a safety margin
    right = int((M / min_price) ** 0.5) + 10
    
    left = 0
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        
        if can_buy_k_units(mid, prices, M):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return answer

# Read input
N, M = map(int, input().split())
prices = list(map(int, input().split()))

# Solve and print answer
print(solve(N, M, prices))
