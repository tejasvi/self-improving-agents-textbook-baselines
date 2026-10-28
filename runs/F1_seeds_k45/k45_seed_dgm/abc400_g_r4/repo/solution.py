def solve(n, k, cakes):
    """
    Solve the cake pairing problem.
    
    Args:
    n: number of cakes
    k: number of pairs needed
    cakes: list of (x, y, z) tuples for each cake
    
    Returns:
    maximum total price of k pairs
    """
    
    # Memoization dictionary: tuple of available cake indices -> max price
    memo = {}
    
    def get_price(i, j):
        """Get the price of pairing cake i with cake j"""
        x = cakes[i][0] + cakes[j][0]
        y = cakes[i][1] + cakes[j][1]
        z = cakes[i][2] + cakes[j][2]
        return max(x, y, z)
    
    def dp(available, pairs_left):
        """
        Find the maximum price using the available cakes and needing pairs_left more pairs.
        available is a tuple of cake indices still available.
        """
        if pairs_left == 0:
            return 0
        
        if len(available) < 2 * pairs_left:
            return float('-inf')
        
        # Create a hashable key for memoization
        key = (available, pairs_left)
        if key in memo:
            return memo[key]
        
        available_list = list(available)
        max_price = float('-inf')
        
        # Try pairing the first available cake with each other available cake
        first = available_list[0]
        for i in range(1, len(available_list)):
            second = available_list[i]
            price = get_price(first, second)
            
            # Create new available set without these two cakes
            new_available = tuple(c for j, c in enumerate(available_list) if j != 0 and j != i)
            
            remaining = dp(new_available, pairs_left - 1)
            if remaining != float('-inf'):
                max_price = max(max_price, price + remaining)
        
        memo[key] = max_price
        return max_price
    
    available = tuple(range(n))
    return dp(available, k)


def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        cakes = []
        for _ in range(n):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        result = solve(n, k, cakes)
        print(result)


if __name__ == "__main__":
    main()
