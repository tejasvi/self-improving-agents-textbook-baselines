n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)
extra_moves = total_sum - n

if extra_moves % 2 == 1:
    print("Fennec")
else:
    print("Snuke")
