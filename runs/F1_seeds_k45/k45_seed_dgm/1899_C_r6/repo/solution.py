def solve():
    t = int(input())
    
    for _ in range(t):
        n = int(input())
        a = list(map(int, input().split()))
        
        # dp_odd: max sum ending at current position with odd parity
        # dp_even: max sum ending at current position with even parity
        dp_odd = float('-inf')
        dp_even = float('-inf')
        
        max_sum = float('-inf')
        
        for i in range(n):
            # Current element's parity
            if a[i] % 2 == 1:  # odd
                # Can extend from even or start new
                new_dp_odd = max(a[i], dp_even + a[i])
                dp_odd = new_dp_odd
            else:  # even
                # Can extend from odd or start new
                new_dp_even = max(a[i], dp_odd + a[i])
                dp_even = new_dp_even
            
            # Update maximum
            if a[i] % 2 == 1:
                max_sum = max(max_sum, dp_odd)
            else:
                max_sum = max(max_sum, dp_even)
        
        print(max_sum)

solve()
