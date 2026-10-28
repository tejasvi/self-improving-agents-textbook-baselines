# Write your solution here. Read from stdin, write to stdout.

def can_achieve(foods, X, target):
    """
    Check if we can achieve at least 'target' units of each vitamin
    within X calories.
    """
    # Separate foods by vitamin type
    vit1_foods = []
    vit2_foods = []
    vit3_foods = []
    
    for v, a, c in foods:
        if v == 1:
            vit1_foods.append((a, c))
        elif v == 2:
            vit2_foods.append((a, c))
        else:
            vit3_foods.append((a, c))
    
    # For each amount of vitamin 1 that costs at most X calories,
    # calculate minimum calories and check if we can get target of 2 and 3
    
    # DP for vitamin 1: dp1[i] = minimum calories to get at least i units
    max_vit = target * 2 + 100  # Upper bound on vitamin amount we care about
    dp1 = [float('inf')] * (max_vit + 1)
    dp1[0] = 0
    
    for amount, cost in vit1_foods:
        for i in range(max_vit, -1, -1):
            if dp1[i] < float('inf'):
                new_i = min(max_vit, i + amount)
                dp1[new_i] = min(dp1[new_i], dp1[i] + cost)
    
    # DP for vitamin 2: dp2[i] = minimum calories to get at least i units
    dp2 = [float('inf')] * (max_vit + 1)
    dp2[0] = 0
    
    for amount, cost in vit2_foods:
        for i in range(max_vit, -1, -1):
            if dp2[i] < float('inf'):
                new_i = min(max_vit, i + amount)
                dp2[new_i] = min(dp2[new_i], dp2[i] + cost)
    
    # DP for vitamin 3: dp3[i] = minimum calories to get at least i units
    dp3 = [float('inf')] * (max_vit + 1)
    dp3[0] = 0
    
    for amount, cost in vit3_foods:
        for i in range(max_vit, -1, -1):
            if dp3[i] < float('inf'):
                new_i = min(max_vit, i + amount)
                dp3[new_i] = min(dp3[new_i], dp3[i] + cost)
    
    # Check if we can achieve target for all three within X calories
    for i in range(target, max_vit + 1):
        if dp1[i] + dp2[target] + dp3[target] <= X:
            return True
    
    if dp1[target] + dp2[target] + dp3[target] <= X:
        return True
    
    return False


def solve():
    N, X = map(int, input().split())
    foods = []
    
    for _ in range(N):
        parts = list(map(int, input().split()))
        V, A, C = parts[0], parts[1], parts[2]
        foods.append((V, A, C))
    
    # Binary search on the answer
    left, right = 0, 200000
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
