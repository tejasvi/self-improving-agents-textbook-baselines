import heapq

def solve():
    N, W = map(int, input().split())
    items = []
    for _ in range(N):
        w, v = map(int, input().split())
        items.append((w, v))
    
    # Use a max heap (negate values for min heap)
    # Each entry is (-marginal_happiness, item_type, count)
    # where count is how many items of this type we've already taken
    heap = []
    
    # Initialize: for each type, add the first item's marginal happiness
    for i in range(N):
        w, v = items[i]
        # Marginal happiness of taking the first item of type i is v - 2*0 = v
        marginal = v
        heapq.heappush(heap, (-marginal, i, 0))
    
    total_weight = 0
    total_happiness = 0
    item_counts = [0] * N
    
    # Greedy approach: always pick the item with highest marginal happiness
    while heap:
        neg_marginal, item_type, prev_count = heapq.heappop(heap)
        marginal = -neg_marginal
        w, v = items[item_type]
        
        # Check if we can add this item
        if total_weight + w <= W:
            # Add this item
            total_weight += w
            item_counts[item_type] += 1
            total_happiness += marginal
            
            # Add the next item of this type to the heap
            # If we've taken k items, the marginal happiness of the (k+1)-th item is v - 2*k
            next_marginal = v - 2 * item_counts[item_type]
            if next_marginal > 0:  # Only add if marginal happiness is positive
                heapq.heappush(heap, (-next_marginal, item_type, item_counts[item_type]))
    
    print(total_happiness)

solve()
