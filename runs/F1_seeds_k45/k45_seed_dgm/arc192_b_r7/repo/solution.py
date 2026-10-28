n = int(input())
a = list(map(int, input().split()))

# Calculate sum of (A_i - 1)
extra_moves = sum(a) - n

# If the sum of extra moves is odd, Fennec wins (first player)
# If the sum of extra moves is even, Snuke wins (second player)
if extra_moves % 2 == 1:
    print("Fennec")
else:
    print("Snuke")
