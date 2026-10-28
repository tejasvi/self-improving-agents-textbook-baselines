def min_cost_for_total(total, P):
    """
    Given a target total number of units and prices,
    compute the minimum cost to buy exactly that total.
    
    We use the fact that at optimality, marginal costs should be balanced.
    For each product i with k_i units, the marginal cost of the next unit is (2*k_i + 1) * P_i.
    
    We greedily allocate units to the product with minimum marginal cost.
    """
    N = len(P)
    k = [0] * N  # current units of each product
    cost = 0
    
    for _ in range(total):
        # Find product with minimum marginal cost
        min_idx = 0
        min_marginal = (2 * k[0] + 1) * P[0]
        
        for i in range(1, N):
            marginal = (2 * k[i] + 1) * P[i]
            if marginal < min_marginal:
                min_marginal = marginal
                min_idx = i
        
        # Buy one more unit of that product
        cost += min_marginal
        k[min_idx] += 1
    
    return cost


def main():
    N, M = map(int, input().split())
    P = list(map(int, input().split()))
    
    # Binary search on the total number of units
    # Find maximum T such that min_cost_for_total(T, P) <= M
    
    left, right = 0, 2 * 10**9  # Upper bound estimate
    
    # Refine upper bound
    min_price = min(P)
    # Maximum possible: if we buy all from cheapest, k^2 * min_price <= M
    # k <= sqrt(M / min_price)
    right = int((M / min_price) ** 0.5) + 2
    
    while left < right:
        mid = (left + right + 1) // 2
        cost = min_cost_for_total(mid, P)
        
        if cost <= M:
            left = mid
        else:
            right = mid - 1
    
    print(left)


if __name__ == "__main__":
    main()
