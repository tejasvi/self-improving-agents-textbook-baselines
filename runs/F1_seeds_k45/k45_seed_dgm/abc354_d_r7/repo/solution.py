def cell_color(i, j):
    """
    Determine if cell [i, i+1] × [j, j+1] is black or white.
    Check the center point (i+0.5, j+0.5) and count boundary crossings from (0.5, 0.5).
    """
    
    # Count vertical lines x = n (integers) between 0.5 and i+0.5
    v_cross = i  # lines x=1, 2, ..., i if i > 0; lines x=0, -1, ... if i < 0
    
    # Count horizontal lines y = 2n (evens) between 0.5 and j+0.5
    if j >= 0:
        # Even lines at 0, 2, 4, ... up to 2*floor((j)/2)
        h_cross = j // 2
    else:
        # For negative j, count backward
        # From 0.5 down, we cross evens at 0, -2, -4, ...
        # Up to j+0.5
        h_cross = -((-j) // 2) - (1 if (-j) % 2 == 1 else 0)
    
    # Count diagonal lines x+y = 2n (evens) between 1 and i+j+1
    sum_val = i + j + 1
    if sum_val > 1:
        # Count evens in (1, i+j+1]
        first_even = 2
        last_even = sum_val if sum_val % 2 == 0 else sum_val - 1
        if first_even <= last_even:
            d_cross = (last_even - first_even) // 2 + 1
        else:
            d_cross = 0
    else:
        d_cross = 0
    
    parity = (v_cross + h_cross + d_cross) % 2
    return parity == 0  # black if even parity

A, B, C, D = map(int, input().split())

# We need to compute the total black area
# Multiply result by 2 to avoid floating point

total_twice_area = 0

# Process each unit cell
for i in range(A, C):
    for j in range(B, D):
        if cell_color(i, j):
            total_twice_area += 2

print(total_twice_area)
