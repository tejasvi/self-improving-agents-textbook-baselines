n = int(input())
a = list(map(int, input().split()))

total_sum = sum(a)
max_a = max(a)

diff = total_sum - max_a

# If diff is even, Snuke wins
# If diff is odd and N is odd, Fennec wins
# If diff is odd and N is even, Snuke wins

if diff % 2 == 0:
    print("Snuke")
else:  # diff % 2 == 1
    if n % 2 == 1:
        print("Fennec")
    else:
        print("Snuke")
