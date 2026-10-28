import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i], c1[i]: min number of changes to make node i evaluate to 0 / 1
    c0 = [0 if ch == "0" else 1 for ch in s]
    c1 = [1 if ch == "0" else 0 for ch in s]
    for _ in range(n):
        nc0 = []
        nc1 = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            nc0.append(a + b + c - max(a, b, c))  # two smallest costs
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            nc1.append(a + b + c - max(a, b, c))
        c0, c1 = nc0, nc1
    # The actual root value v has cost 0; flipping it requires the cost of the other value.
    if c0[0] == 0:
        ans = c1[0]
    else:
        ans = c0[0]
    print(ans)


main()
