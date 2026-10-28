def solve():
    n = int(input())
    a = list(map(int, input().split()))
    
    # dp_odd: max sum ending at current position with odd last element
    # dp_even: max sum ending at current position with even last element
    dp_odd = None
    dp_even = None
    
    max_sum = a[0]
    
    for i in range(n):
        # Check parity of current element
        is_odd = a[i] % 2 != 0
        
        new_odd = None
        new_even = None
        
        if is_odd:
            # Current element is odd
            # We can either start new or extend from even
            if dp_even is not None:
                new_odd = max(a[i], dp_even + a[i])
            else:
                new_odd = a[i]
            dp_odd = new_odd
        else:
            # Current element is even
            # We can either start new or extend from odd
            if dp_odd is not None:
                new_even = max(a[i], dp_odd + a[i])
            else:
                new_even = a[i]
            dp_even = new_even
        
        # Update the overall maximum
        if new_odd is not None:
            max_sum = max(max_sum, new_odd)
        if new_even is not None:
            max_sum = max(max_sum, new_even)
    
    return max_sum

t = int(input())
for _ in range(t):
    print(solve())
