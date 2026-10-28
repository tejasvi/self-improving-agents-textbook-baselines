def solve():
    N, Q = map(int, input().split())
    H = [0] + list(map(int, input().split()))  # 1-indexed
    
    for _ in range(Q):
        l, r = map(int, input().split())
        count = 0
        
        # Check each building to the east of r
        for k in range(r + 1, N + 1):
            # Check if building k can be seen from both l and r
            
            # Can be seen from l if no building taller than H[k] between l and k
            can_see_from_l = True
            for i in range(l + 1, k):
                if H[i] > H[k]:
                    can_see_from_l = False
                    break
            
            if not can_see_from_l:
                continue
            
            # Can be seen from r if no building taller than H[k] between r and k
            can_see_from_r = True
            for i in range(r + 1, k):
                if H[i] > H[k]:
                    can_see_from_r = False
                    break
            
            if can_see_from_r:
                count += 1
        
        print(count)

solve()
