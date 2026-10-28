from itertools import combinations

def solve(N, K, cakes):
    """
    Find the maximum total price of K pairs.
    
    cakes: list of (X, Y, Z) tuples
    """
    # For small N, we can try all possible pairings
    # We need to select 2K cakes and pair them optimally
    
    max_total = 0
    
    # Generate all combinations of 2K cakes from N cakes
    for selected_indices in combinations(range(N), 2 * K):
        selected_cakes = [cakes[i] for i in selected_indices]
        
        # Now we need to pair these 2K cakes optimally
        # Try all possible pairings of these 2K cakes
        best_pairing = find_best_pairing(selected_cakes)
        max_total = max(max_total, best_pairing)
    
    return max_total


def find_best_pairing(cakes):
    """
    Given a list of cakes (already selected), find the best pairing.
    Uses dynamic programming with memoization.
    """
    n = len(cakes)
    
    def get_pair_price(i, j):
        x = cakes[i][0] + cakes[j][0]
        y = cakes[i][1] + cakes[j][1]
        z = cakes[i][2] + cakes[j][2]
        return max(x, y, z)
    
    # Use bitmask DP
    # dp[mask] = maximum price using cakes indicated by the mask
    dp = {}
    
    def rec(mask):
        if mask == 0:
            return 0
        
        if mask in dp:
            return dp[mask]
        
        result = 0
        # Find the first available cake
        first = -1
        for i in range(n):
            if mask & (1 << i):
                first = i
                break
        
        # Try pairing it with all other available cakes
        for j in range(first + 1, n):
            if mask & (1 << j):
                new_mask = mask ^ (1 << first) ^ (1 << j)
                price = get_pair_price(first, j) + rec(new_mask)
                result = max(result, price)
        
        dp[mask] = result
        return result
    
    initial_mask = (1 << n) - 1
    return rec(initial_mask)


T = int(input())
for _ in range(T):
    N, K = map(int, input().split())
    cakes = []
    for _ in range(N):
        x, y, z = map(int, input().split())
        cakes.append((x, y, z))
    
    print(solve(N, K, cakes))
