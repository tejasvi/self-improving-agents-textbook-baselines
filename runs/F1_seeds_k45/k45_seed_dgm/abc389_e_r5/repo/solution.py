# Write your solution here. Read from stdin, write to stdout.

def can_buy(k, prices, budget):
    """
    Check if we can buy exactly k units total with cost <= budget.
    Greedy approach: buy from cheapest products first.
    """
    sorted_prices = sorted(prices)
    total_cost = 0
    remaining = k
    
    for price in sorted_prices:
        if remaining == 0:
            break
        
        # Check if we can buy all remaining from this product
        cost_if_all = remaining * remaining * price
        if total_cost + cost_if_all <= budget:
            total_cost += cost_if_all
            remaining = 0
        else:
            # Binary search for how many we can buy from this product
            left, right = 0, remaining
            best = 0
            while left <= right:
                mid = (left + right) // 2
                cost = mid * mid * price
                if total_cost + cost <= budget:
                    best = mid
                    left = mid + 1
                else:
                    right = mid - 1
            
            if best > 0:
                cost_added = best * best * price
                total_cost += cost_added
                remaining -= best
            
            # If we can't buy any more from this product, 
            # we also can't buy from more expensive products
            if best == 0:
                break
            
    return remaining == 0 and total_cost <= budget

def solve():
    n, m = map(int, input().split())
    prices = list(map(int, input().split()))
    
    # Binary search on the answer
    # Upper bound: if we buy from cheapest product only
    min_price = min(prices)
    upper_bound = int((m / min_price) ** 0.5) + 1000
    
    left, right = 0, upper_bound
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_buy(mid, prices, m):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
