# Write your solution here. Read from stdin, write to stdout.

def solve(N, K, cakes):
    """
    Find the maximum total price of K pairs from N cakes.
    
    For K pairs, we need to select 2K cakes and pair them optimally.
    The price of a pair is max(sum of beauty, sum of tastiness, sum of popularity)
    """
    
    # Key insight: For each of the 3 dimensions, we can try a greedy approach:
    # - Sort cakes by that dimension
    # - Pair them in a way that maximizes total price
    # 
    # We'll try different pairing strategies for each dimension and pick the best.
    
    best_total = 0
    
    # Strategy 1: For each dimension, sort and pair greedily
    for dimension in range(3):
        # Sort indices by the specified dimension value
        sorted_indices = sorted(range(N), key=lambda i: cakes[i][dimension])
        
        # Strategy: pair smallest with largest
        total = 0
        pairs = []
        
        left = 0
        right = N - 1
        
        while len(pairs) < K:
            idx1 = sorted_indices[left]
            idx2 = sorted_indices[right]
            
            price = max(
                cakes[idx1][0] + cakes[idx2][0],
                cakes[idx1][1] + cakes[idx2][1],
                cakes[idx1][2] + cakes[idx2][2]
            )
            
            pairs.append((idx1, idx2, price))
            total += price
            
            left += 1
            right -= 1
        
        best_total = max(best_total, total)
    
    # Strategy 2: Sort by sum of all dimensions and pair
    sorted_indices = sorted(range(N), key=lambda i: sum(cakes[i]))
    
    total = 0
    left = 0
    right = N - 1
    
    for _ in range(K):
        idx1 = sorted_indices[left]
        idx2 = sorted_indices[right]
        
        price = max(
            cakes[idx1][0] + cakes[idx2][0],
            cakes[idx1][1] + cakes[idx2][1],
            cakes[idx1][2] + cakes[idx2][2]
        )
        
        total += price
        left += 1
        right -= 1
    
    best_total = max(best_total, total)
    
    # Strategy 3: Pair consecutively after sorting by each dimension
    for dimension in range(3):
        sorted_indices = sorted(range(N), key=lambda i: cakes[i][dimension])
        
        total = 0
        for i in range(0, 2*K, 2):
            idx1 = sorted_indices[i]
            idx2 = sorted_indices[i + 1]
            
            price = max(
                cakes[idx1][0] + cakes[idx2][0],
                cakes[idx1][1] + cakes[idx2][1],
                cakes[idx1][2] + cakes[idx2][2]
            )
            
            total += price
        
        best_total = max(best_total, total)
    
    return best_total


def main():
    T = int(input())
    for _ in range(T):
        N, K = map(int, input().split())
        cakes = []
        for _ in range(N):
            X, Y, Z = map(int, input().split())
            cakes.append((X, Y, Z))
        
        result = solve(N, K, cakes)
        print(result)


if __name__ == "__main__":
    main()
