# Write your solution here. Read from stdin, write to stdout.

def solve_case(n, k, cakes):
    """
    Solve one test case.
    n: number of cakes
    k: number of pairs to form
    cakes: list of (x, y, z) tuples
    """
    
    def pair_price(i, j):
        """Calculate price of pairing cake i and cake j"""
        x_sum = cakes[i][0] + cakes[j][0]
        y_sum = cakes[i][1] + cakes[j][1]
        z_sum = cakes[i][2] + cakes[j][2]
        return max(x_sum, y_sum, z_sum)
    
    def greedy_select_pairs(score_func):
        """
        Greedily select K pairs based on score_func.
        score_func: a function that takes (i, j) and returns a score for that pair.
        Returns the actual total price of the selected pairs.
        """
        # Generate all possible pairs with their scores
        pairs = []
        for i in range(n):
            for j in range(i + 1, n):
                score = score_func(i, j)
                pairs.append((score, i, j))
        
        # Sort pairs by score in descending order
        pairs.sort(reverse=True)
        
        # Greedily select K non-overlapping pairs
        used = [False] * n
        total_price = 0
        pairs_formed = 0
        
        for score, i, j in pairs:
            if not used[i] and not used[j]:
                used[i] = True
                used[j] = True
                # Add the actual price of this pair
                total_price += pair_price(i, j)
                pairs_formed += 1
                if pairs_formed == k:
                    break
        
        return total_price
    
    max_total = 0
    
    # Try different objective functions for selecting pairs
    
    # 1. Maximize X dimension sum
    total = greedy_select_pairs(lambda i, j: cakes[i][0] + cakes[j][0])
    max_total = max(max_total, total)
    
    # 2. Maximize Y dimension sum
    total = greedy_select_pairs(lambda i, j: cakes[i][1] + cakes[j][1])
    max_total = max(max_total, total)
    
    # 3. Maximize Z dimension sum
    total = greedy_select_pairs(lambda i, j: cakes[i][2] + cakes[j][2])
    max_total = max(max_total, total)
    
    # 4. The actual objective: maximize the actual pair prices
    total = greedy_select_pairs(pair_price)
    max_total = max(max_total, total)
    
    return max_total


def main():
    t = int(input())
    for _ in range(t):
        n, k = map(int, input().split())
        cakes = []
        for _ in range(n):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        result = solve_case(n, k, cakes)
        print(result)


if __name__ == "__main__":
    main()
