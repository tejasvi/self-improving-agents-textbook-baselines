# Write your solution here. Read from stdin, write to stdout.

def solve_case(n, k, cakes):
    """
    Find the maximum total price of K pairs from N cakes.
    
    Each cake has (beauty, tastiness, popularity).
    Price of a pair is max(X_a + X_b, Y_a + Y_b, Z_a + Z_b).
    """
    
    def pair_price(i, j):
        """Calculate price of pairing cake i with cake j"""
        x_sum = cakes[i][0] + cakes[j][0]
        y_sum = cakes[i][1] + cakes[j][1]
        z_sum = cakes[i][2] + cakes[j][2]
        return max(x_sum, y_sum, z_sum)
    
    # Use memoization with bitmask DP
    memo = {}
    
    def dp(used_mask, pairs_left):
        """
        Find max price using DP with bitmask.
        used_mask: bitmask of which cakes are already used
        pairs_left: how many more pairs we need to form
        Returns: maximum total price
        """
        if pairs_left == 0:
            return 0
        
        if (used_mask, pairs_left) in memo:
            return memo[(used_mask, pairs_left)]
        
        result = -1  # Initialize to invalid
        
        # Find first unused cake to pair with
        first = -1
        for i in range(n):
            if not (used_mask & (1 << i)):
                first = i
                break
        
        if first == -1:
            # No more cakes available
            return -float('inf') if pairs_left > 0 else 0
        
        # Try pairing with each other unused cake
        for second in range(first + 1, n):
            if not (used_mask & (1 << second)):
                price = pair_price(first, second)
                new_mask = used_mask | (1 << first) | (1 << second)
                remaining = dp(new_mask, pairs_left - 1)
                if remaining >= 0:
                    result = max(result, price + remaining)
        
        memo[(used_mask, pairs_left)] = result
        return result
    
    return dp(0, k)


def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        cakes = []
        for _ in range(n):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        answer = solve_case(n, k, cakes)
        print(answer)


if __name__ == "__main__":
    main()
