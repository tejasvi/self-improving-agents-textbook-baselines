import heapq

def can_buy(prices, M, target_units):
    """
    Check if we can buy target_units with cost <= M.
    Use greedy approach: for each unit, buy from the product with lowest marginal cost.
    """
    n = len(prices)
    # heap: (marginal_cost_for_next_unit, units_of_this_product_bought, price_index)
    heap = [(prices[i], 0, i) for i in range(n)]
    heapq.heapify(heap)
    
    total_cost = 0
    units_bought = 0
    
    for _ in range(target_units):
        # Get the product with lowest marginal cost
        marginal_cost, k, idx = heapq.heappop(heap)
        
        # Cost to buy one more unit from this product
        # Total cost of k units: k^2 * P[idx]
        # Total cost of (k+1) units: (k+1)^2 * P[idx]
        # Marginal cost: (k+1)^2 * P[idx] - k^2 * P[idx] = (2k + 1) * P[idx]
        cost_one_more = (2 * k + 1) * prices[idx]
        
        if total_cost + cost_one_more > M:
            # Can't afford this unit - not enough budget
            return False
        
        total_cost += cost_one_more
        k += 1
        units_bought += 1
        
        # Push back with updated marginal cost for next unit
        next_marginal_cost = (2 * k + 1) * prices[idx]
        heapq.heappush(heap, (next_marginal_cost, k, idx))
    
    return True


def solve(N, M, prices):
    """
    Binary search on the answer (total number of units).
    """
    min_price = min(prices)
    # Upper bound: if we buy all from cheapest, k^2 * min_price <= M
    # k <= sqrt(M / min_price)
    # Add some buffer for safety
    left, right = 0, int((M / min_price) ** 0.5) + 10
    
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_buy(prices, M, mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return answer


# Read input
N, M = map(int, input().split())
prices = list(map(int, input().split()))

# Solve and print
print(solve(N, M, prices))
