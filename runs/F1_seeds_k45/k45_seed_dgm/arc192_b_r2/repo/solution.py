n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)
free_moves = total_sum - n

# If free_moves is odd, Fennec makes the last move and wins
# If free_moves is even, Snuke makes the last move and wins
if free_moves % 2 == 1:
    print("Fennec")
else:
    print("Snuke")
