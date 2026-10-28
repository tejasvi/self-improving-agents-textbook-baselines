def min_cost_for_units(total_units, prices):
    """
    Find the minimum cost to buy exactly total_units units.
    Uses the optimal allocation: k_i = lambda / (2*P_i) for all i.
    """
    n = len(prices)
    
    # All products should contribute proportionally to 1/price
    # k_i = c / sqrt(P_i) for some constant c
    # sum(k_i) = total_units => sum(c / sqrt(P_i)) = total_units
    # => c = total_units / sum(1/sqrt(P_i))
    
    inv_sqrt_prices = [1.0 / (p ** 0.5) for p in prices]
    sum_inv_sqrt = sum(inv_sqrt_prices)
    c = total_units / sum_inv_sqrt
    
    # Calculate cost
    cost = 0
    for p, inv_sqrt_p in zip(prices, inv_sqrt_prices):
        k = c * inv_sqrt_p
        cost += k * k * p
    
    return cost


def can_buy(total_units, prices, budget):
    """
    Check if we can buy exactly total_units units within the budget.
    """
    cost = min_cost_for_units(total_units, prices)
    return cost <= budget


def solve(n, m, prices):
    """
    Binary search on the answer: total number of units.
    """
    # Upper bound
    min_price = min(prices)
    upper_bound = int((m / min_price) ** 0.5) + 10
    
    left, right = 0, upper_bound
    
    answer = 0
    while left <= right:
        mid = (left + right) // 2
        if can_buy(mid, prices, m):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    return answer


# Read input
n, m = map(int, input().split())
prices = list(map(int, input().split()))

# Solve and print answer
print(solve(n, m, prices))
