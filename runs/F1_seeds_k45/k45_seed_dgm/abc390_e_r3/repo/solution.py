# Read input
N, X = map(int, input().split())
foods = []
for _ in range(N):
    V, A, C = map(int, input().split())
    foods.append((V, A, C))

# Separate foods by vitamin type
vitamin_foods = [[], [], []]
for V, A, C in foods:
    vitamin_foods[V - 1].append((A, C))

def get_best_for_calories(food_list, max_calories):
    """
    Get the best amount of a specific vitamin achievable with at most 
    max_calories for that vitamin.
    Returns a dict: max_calories_used -> max_amount
    """
    dp = [0] * (max_calories + 1)
    for amount, calories in food_list:
        for c in range(max_calories, calories - 1, -1):
            dp[c] = max(dp[c], dp[c - calories] + amount)
    return dp

# Precompute DP for each vitamin type
dp_vitamins = []
for i in range(3):
    dp_vitamins.append(get_best_for_calories(vitamin_foods[i], X))

answer = 0

# Try all possible calorie allocations
for c1 in range(X + 1):
    for c2 in range(X - c1 + 1):
        c3 = X - c1 - c2
        v1 = dp_vitamins[0][c1]
        v2 = dp_vitamins[1][c2]
        v3 = dp_vitamins[2][c3]
        answer = max(answer, min(v1, v2, v3))

print(answer)
