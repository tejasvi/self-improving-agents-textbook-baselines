def solve():
    T = int(input())
    
    for _ in range(T):
        N, K = map(int, input().split())
        cakes = []
        for i in range(N):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        # Calculate price of a pair
        def pair_price(i, j):
            x_sum = cakes[i][0] + cakes[j][0]
            y_sum = cakes[i][1] + cakes[j][1]
            z_sum = cakes[i][2] + cakes[j][2]
            return max(x_sum, y_sum, z_sum)
        
        # Use memoization with tuple-based used set
        memo = {}
        
        def dp(used_tuple, pairs_count):
            if pairs_count == K:
                return 0
            
            key = (used_tuple, pairs_count)
            if key in memo:
                return memo[key]
            
            used_set = set(used_tuple)
            
            result = 0
            
            # Find first unused cake
            first_unused = -1
            for i in range(N):
                if i not in used_set:
                    first_unused = i
                    break
            
            if first_unused == -1:
                return 0
            
            # Try pairing with other unused cakes
            for j in range(first_unused + 1, N):
                if j not in used_set:
                    price = pair_price(first_unused, j)
                    new_used = tuple(sorted(list(used_set) + [first_unused, j]))
                    result = max(result, price + dp(new_used, pairs_count + 1))
            
            memo[key] = result
            return result
        
        answer = dp(tuple(), 0)
        print(answer)

solve()
