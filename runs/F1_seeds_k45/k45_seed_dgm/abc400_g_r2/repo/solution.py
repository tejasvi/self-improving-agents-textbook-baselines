def solve():
    N, K = map(int, input().split())
    cakes = []
    for i in range(N):
        x, y, z = map(int, input().split())
        cakes.append((x, y, z, i))
    
    max_total = 0
    
    # Try different strategies: prioritize each attribute
    for priority_attr in range(3):
        # For each attribute, try greedy pairing
        # Sort by the priority attribute (descending)
        sorted_cakes = sorted(enumerate(cakes), key=lambda c: c[1][priority_attr], reverse=True)
        
        # Greedy: pair highest with second highest, third with fourth, etc.
        used = [False] * N
        pairs = []
        
        for i in range(len(sorted_cakes)):
            if used[sorted_cakes[i][0]]:
                continue
            # Find the best unpaired cake to pair with
            best_j = -1
            best_price = -1
            for j in range(i + 1, len(sorted_cakes)):
                if used[sorted_cakes[j][0]]:
                    continue
                idx_i = sorted_cakes[i][0]
                idx_j = sorted_cakes[j][0]
                cake_i = cakes[idx_i]
                cake_j = cakes[idx_j]
                price = max(cake_i[0] + cake_j[0], cake_i[1] + cake_j[1], cake_i[2] + cake_j[2])
                if price > best_price:
                    best_price = price
                    best_j = j
            
            if best_j != -1:
                idx_i = sorted_cakes[i][0]
                idx_j = sorted_cakes[best_j][0]
                used[idx_i] = True
                used[idx_j] = True
                pairs.append(best_price)
                if len(pairs) == K:
                    break
        
        if len(pairs) == K:
            total = sum(pairs)
            max_total = max(max_total, total)
    
    # Also try a different approach: use DP for small N
    if N <= 20:
        # Use bitmask DP to try all possible pairings
        from functools import lru_cache
        
        def get_pair_price(i, j):
            cake_i = cakes[i]
            cake_j = cakes[j]
            return max(cake_i[0] + cake_j[0], cake_i[1] + cake_j[1], cake_i[2] + cake_j[2])
        
        @lru_cache(maxsize=None)
        def dp(mask, pairs_left):
            if pairs_left == 0:
                return 0
            
            best = 0
            for i in range(N):
                if mask & (1 << i):
                    continue
                for j in range(i + 1, N):
                    if mask & (1 << j):
                        continue
                    price = get_pair_price(i, j)
                    new_mask = mask | (1 << i) | (1 << j)
                    total = price + dp(new_mask, pairs_left - 1)
                    best = max(best, total)
            
            return best
        
        max_total = max(max_total, dp(0, K))
    
    print(max_total)

T = int(input())
for _ in range(T):
    solve()
