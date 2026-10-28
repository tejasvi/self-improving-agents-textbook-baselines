import math

def min_cost_for_k_units(k, prices):
    """
    Calculate minimum cost to buy exactly k units given prices.
    """
    n = len(prices)
    
    # Try different strategies: use only the m cheapest products
    min_cost = float('inf')
    
    sorted_prices = sorted(prices)
    
    for m in range(1, n + 1):
        # Use only the m cheapest products
        # Optimal distribution: x_i ∝ 1/sqrt(p_i)
        # But easier: binary search on how many from cheapest, rest distributed among others
        
        # Actually, let's use a simpler approach:
        # For m products with prices p_1, ..., p_m (sorted),
        # compute optimal allocation using ratios
        
        inv_sqrt_p = [1.0 / math.sqrt(p) for p in sorted_prices[:m]]
        total_inv_sqrt = sum(inv_sqrt_p)
        
        # Allocation in continuous case
        allocations = [k * inv_sqrt_p[i] / total_inv_sqrt for i in range(m)]
        
        # Round to nearest integers while maintaining sum = k
        int_allocations = [int(a) for a in allocations]
        diff = k - sum(int_allocations)
        
        # Adjust for rounding errors by adding 1 to products where we lose most
        indices = list(range(m))
        indices.sort(key=lambda i: allocations[i] - int_allocations[i], reverse=True)
        
        for i in range(diff):
            int_allocations[indices[i]] += 1
        
        # Calculate cost
        cost = sum(int_allocations[i] ** 2 * sorted_prices[i] for i in range(m))
        min_cost = min(min_cost, cost)
    
    return min_cost

def solve():
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    
    # Binary search on the answer
    min_price = min(prices)
    left, right = 0, int((m / min_price) ** 0.5) + 2
    
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        cost = min_cost_for_k_units(mid, prices)
        
        if cost <= m:
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
