# Write your solution here. Read from stdin, write to stdout.

def can_achieve(foods, X, target):
    """
    Check if we can achieve at least 'target' units of each vitamin within X calories.
    
    Strategy:
    - Use DP to find minimum calories needed for each (v1, v2) pair
    - Then check if remaining calories can afford at least 'target' units of v3
    """
    # Separate foods by vitamin type
    v1_foods = [f for f in foods if f[0] == 1]
    v2_foods = [f for f in foods if f[0] == 2]
    v3_foods = [f for f in foods if f[0] == 3]
    
    # DP for vitamin 1: dp1[cal] = max units of v1 with exactly cal calories
    dp1 = [0] * (X + 1)
    for amount, cal in v1_foods:
        for c in range(X, cal - 1, -1):
            dp1[c] = max(dp1[c], dp1[c - cal] + amount)
    
    # DP for vitamin 2: dp2[cal] = max units of v2 with exactly cal calories
    dp2 = [0] * (X + 1)
    for amount, cal in v2_foods:
        for c in range(X, cal - 1, -1):
            dp2[c] = max(dp2[c], dp2[c - cal] + amount)
    
    # DP for vitamin 3: dp3[cal] = max units of v3 with exactly cal calories
    dp3 = [0] * (X + 1)
    for amount, cal in v3_foods:
        for c in range(X, cal - 1, -1):
            dp3[c] = max(dp3[c], dp3[c - cal] + amount)
    
    # Check all combinations
    for cal1 in range(X + 1):
        if dp1[cal1] < target:
            continue
        for cal2 in range(X + 1 - cal1):
            if dp2[cal2] < target:
                continue
            cal3 = X - cal1 - cal2
            if dp3[cal3] >= target:
                return True
    
    return False

def solve():
    N, X = map(int, input().split())
    foods = []
    for _ in range(N):
        V, A, C = map(int, input().split())
        foods.append((V, A, C))
    
    # Binary search on the answer
    left, right = 0, 2 * 10**5
    answer = 0
    
    while left <= right:
        mid = (left + right) // 2
        if can_achieve(foods, X, mid):
            answer = mid
            left = mid + 1
        else:
            right = mid - 1
    
    print(answer)

solve()
