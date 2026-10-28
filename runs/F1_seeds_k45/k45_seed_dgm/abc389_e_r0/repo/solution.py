# Write your solution here. Read from stdin, write to stdout.

def get_max_units_for_budget(price, budget):
    """Find max units k where k^2 * price <= budget"""
    if budget <= 0 or price <= 0:
        return 0
    
    lo, hi = 0, 10**9
    
    while lo < hi:
        mid = (lo + hi + 1) // 2
        cost = mid * mid * price
        if cost <= budget:
            lo = mid
        else:
            hi = mid - 1
    
    return lo

def min_cost_for_units(prices, total_units):
    """Find minimum cost to buy total_units"""
    if total_units == 0:
        return 0
    
    prices_sorted = sorted(prices)
    cost = 0
    remaining_units = total_units
    
    for price in prices_sorted:
        if remaining_units <= 0:
            break
        
        # Try different allocations for this product
        # We want to minimize cost while achieving the target
        # The key is: for a given number of units at different prices,
        # we should buy more from cheaper products
        
        # Simple greedy: buy as many as possible (up to remaining_units)
        # at the minimum additional cost
        
        # If we've allocated more to previous cheaper products,
        # we might not need many units from this product
        
        # Actually, the optimal strategy is to allocate greedily from cheapest
        # Buy as many as we can from this product, up to remaining_units
        
        units_to_buy = remaining_units  # Try to buy all remaining from here
        cost_this_product = units_to_buy * units_to_buy * price
        
        cost += cost_this_product
        remaining_units = 0
    
    return cost

def can_achieve_units(prices, target_units, budget):
    """Check if we can buy target_units within budget using greedy allocation"""
    if target_units == 0:
        return True
    
    prices_sorted = sorted(prices)
    remaining_budget = budget
    units_bought = 0
    
    for price in prices_sorted:
        if remaining_budget <= 0:
            break
        
        # Binary search: how many units to buy from this product?
        # We want to maximize units bought while keeping cost low
        # Greedy: buy as many as possible
        
        max_units = get_max_units_for_budget(price, remaining_budget)
        
        cost = max_units * max_units * price
        remaining_budget -= cost
        units_bought += max_units
        
        if units_bought >= target_units:
            return True
    
    return units_bought >= target_units

N, M = map(int, input().split())
P = list(map(int, input().split()))

# Binary search on the answer
lo, hi = 0, 2 * 10**9
answer = 0

while lo <= hi:
    mid = (lo + hi) // 2
    if can_achieve_units(P, mid, M):
        answer = mid
        lo = mid + 1
    else:
        hi = mid - 1

print(answer)
