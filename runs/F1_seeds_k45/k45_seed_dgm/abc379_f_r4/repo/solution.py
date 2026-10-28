# Read input
N, Q = map(int, input().split())
H = [0] + list(map(int, input().split()))  # 1-indexed

# For each query
for _ in range(Q):
    l, r = map(int, input().split())
    
    # Count buildings to the east of r that can be seen from both l and r
    count = 0
    
    # Check each building to the east of r
    for k in range(r + 1, N + 1):
        # Check if building k can be seen from building l
        can_see_from_l = True
        for i in range(l + 1, k):
            if H[i] > H[k]:
                can_see_from_l = False
                break
        
        # Check if building k can be seen from building r
        can_see_from_r = True
        for i in range(r + 1, k):
            if H[i] > H[k]:
                can_see_from_r = False
                break
        
        # If visible from both, count it
        if can_see_from_l and can_see_from_r:
            count += 1
    
    print(count)
