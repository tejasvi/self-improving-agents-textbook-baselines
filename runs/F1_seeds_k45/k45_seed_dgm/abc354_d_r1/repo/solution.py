import sys
from math import floor

def is_black(x, y):
    """
    Determine if a point (x, y) is in a black region.
    
    The pattern is determined by:
    - x dividing line at integers
    - y dividing line at even integers
    - x+y dividing line at even integers
    
    Color alternates based on which "cell" we're in.
    Cell (ix, iy, id) where:
    - ix = floor(x)
    - iy = floor(y/2)
    - id = floor((x+y)/2)
    """
    ix = floor(x)
    iy = floor(y / 2)
    id_val = floor((x + y) / 2)
    
    # The parity determines the color
    # (0.5, 0.5) is black, so parity of (0, 0, 0) should give black
    # (0 + 0 + 0) % 2 = 0, so even parity = black
    return (ix + iy + id_val) % 2 == 0

def count_black_area(A, B, C, D):
    """
    Count the black area in the rectangle [A, C] x [B, D].
    
    The key insight is that the wallpaper has a periodic structure.
    We can decompose the rectangle into unit rectangles and sum their contributions.
    """
    
    # Let's think about this differently
    # The area can be computed using a formula or by integrating
    
    # For efficiency with large coordinates (up to 10^9), we need a formula
    # not an iterative approach
    
    # The pattern repeats with period:
    # - Period 2 in both x and y directions (considering the constraints)
    
    # Actually, let's think about the fundamental domain
    # The minimal repeating unit involves:
    # - x lines: period 1 in x
    # - y lines: period 2 in y  
    # - x+y lines: period 2 in x+y direction
    
    # So the pattern might repeat in a 2x2 or similar block
    
    # Let me use a different approach: compute exactly using integration
    
    total_area = 0
    
    # We need to integrate over the rectangle
    # For each vertical strip between consecutive x values, compute the black area
    
    # Identify all critical x values (both integer x and x from x+y=2k lines)
    x_vals = set()
    x_vals.add(A)
    x_vals.add(C)
    
    # Add all integer x in range
    for i in range(floor(A), floor(C) + 1):
        if A < i < C:
            x_vals.add(i)
    
    # Add all x from x+y = 2k for critical y values
    y_vals = set()
    y_vals.add(B)
    y_vals.add(D)
    for j in range(floor(B/2), floor(D/2) + 2):
        y = 2 * j
        if B < y < D:
            y_vals.add(y)
    
    # For each x + y = 2k that's even
    for y in y_vals:
        for k in range(floor((A+B)/2), floor((C+D)/2) + 2):
            x = 2*k - y
            if A < x < C:
                x_vals.add(x)
    
    x_vals = sorted(x_vals)
    y_vals = sorted([B, D] + [y for j in range(floor(B/2)-1, floor(D/2)+2) for y in [2*j] if B < 2*j < D])
    y_vals = sorted(set(y_vals))
    
    # For each rectangle [x_i, x_{i+1}] x [y_j, y_{j+1}]
    # Check if it's black and add area
    
    for i in range(len(x_vals) - 1):
        x1, x2 = x_vals[i], x_vals[i+1]
        for j in range(len(y_vals) - 1):
            y1, y2 = y_vals[j], y_vals[j+1]
            
            # Check if the center is black
            if is_black((x1 + x2) / 2, (y1 + y2) / 2):
                total_area += (x2 - x1) * (y2 - y1)
    
    return total_area

# Read input
A, B, C, D = map(int, input().split())

# Compute and print answer
area = count_black_area(A, B, C, D)
print(int(area * 2))
