import heapq

def can_buy_quantity(prices, quantity, budget):
    """
    Check if we can buy at least 'quantity' units within 'budget'.
    We greedily buy units one at a time from the product with lowest marginal cost.
    The marginal cost of buying the k-th unit of product i is (2k-1)*P_i.
    """
    # Use a min-heap: (marginal_cost, product_index, current_units)
    heap = [(p, i, 0) for i, p in enumerate(prices)]
    heapq.heapify(heap)
    
    total_cost = 0
    units_bought = 0
    
    while units_bought < quantity:
        # Get the product with lowest marginal cost
        marginal_cost, idx, current_units = heapq.heappop(heap)
        
        # Buy one more unit from this product
        next_units = current_units + 1
        total_cost += marginal_cost
        
        if total_cost > budget:
            return False
        
        units_bought += 1
        
        # Push back with updated marginal cost for next unit
        next_marginal_cost = (2 * next_units + 1) * prices[idx]
        heapq.heappush(heap, (next_marginal_cost, idx, next_units))
    
    return True

def solve():
    line1 = input().split()
    N = int(line1[0])
    M = int(line1[1])
    
    prices = list(map(int, input().split()))
    
    # Binary search on the answer
    left, right = 0, 10**9  # Upper bound
    
    while left < right:
        mid = (left + right + 1) // 2
        if can_buy_quantity(prices, mid, M):
            left = mid
        else:
            right = mid - 1
    
    print(left)

solve()
