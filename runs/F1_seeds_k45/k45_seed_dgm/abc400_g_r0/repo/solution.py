# Write your solution here. Read from stdin, write to stdout.

def solve():
    T = int(input())
    for _ in range(T):
        N, K = map(int, input().split())
        cakes = []
        for i in range(N):
            x, y, z = map(int, input().split())
            cakes.append((x, y, z))
        
        best_total = 0
        
        # Strategy 1: Sort by X and pair greedily
        best_total = max(best_total, greedy_pairing(cakes, 0, K))
        
        # Strategy 2: Sort by Y and pair greedily
        best_total = max(best_total, greedy_pairing(cakes, 1, K))
        
        # Strategy 3: Sort by Z and pair greedily
        best_total = max(best_total, greedy_pairing(cakes, 2, K))
        
        print(best_total)

def greedy_pairing(cakes, attr_idx, K):
    """Sort by attribute and pair consecutive cakes"""
    # Create indexed list and sort by specified attribute
    indexed = [(cakes[i][attr_idx], i, cakes[i]) for i in range(len(cakes))]
    indexed.sort(reverse=True)
    
    used = [False] * len(cakes)
    total = 0
    pairs_made = 0
    
    i = 0
    while pairs_made < K and i < len(indexed):
        if not used[indexed[i][1]]:
            # Found first cake, find best match
            cake1_idx = indexed[i][1]
            cake1 = indexed[i][2]
            used[cake1_idx] = True
            
            # Find next unused cake
            best_j = -1
            for j in range(i + 1, len(indexed)):
                if not used[indexed[j][1]]:
                    best_j = j
                    break
            
            if best_j != -1:
                cake2_idx = indexed[best_j][1]
                cake2 = indexed[best_j][2]
                used[cake2_idx] = True
                
                price = max(
                    cake1[0] + cake2[0],
                    cake1[1] + cake2[1],
                    cake1[2] + cake2[2]
                )
                total += price
                pairs_made += 1
            else:
                # Can't find a pair
                break
        i += 1
    
    # Return 0 if we couldn't make K pairs
    return total if pairs_made == K else 0

solve()
