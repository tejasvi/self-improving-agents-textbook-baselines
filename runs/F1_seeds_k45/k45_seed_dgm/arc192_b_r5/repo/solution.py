n = int(input())
a = list(map(int, input().split()))

# The game ends when all N indices have been visited at least once
# With sum(a_i) total operations and N indices to visit,
# there are sum(a_i) - N "extra" operations that don't add new indices to S
# The game ends after sum(a_i) - N moves
# Fennec wins if this is odd, Snuke wins if even

total = sum(a)
moves = total - n

if moves % 2 == 1:
    print("Fennec")
else:
    print("Snuke")
