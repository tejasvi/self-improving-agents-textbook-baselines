import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    size = 3 ** n
    s = s[:size]
    # c0[i], c1[i]: min changes to make node i evaluate to 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [0 if ch == '1' else 1 for ch in s]
    cur = None
    for _ in range(n):
        m = len(c0) // 3
        n0 = [0] * m
        n1 = [0] * m
        for i in range(m):
            a, b, c = c0[3 * i], c0[3 * i + 1], c0[3 * i + 2]
            # sum of two smallest
            t = a + b + c - max(a, b, c)
            n0[i] = t
            a, b, c = c1[3 * i], c1[3 * i + 1], c1[3 * i + 2]
            n1[i] = a + b + c - max(a, b, c)
        c0, c1 = n0, n1
    # current root value: majority determined by cost comparison (cost 0 side)
    cur = 0 if c0[0] == 0 else 1
    # cost to flip root = cost to make it the opposite value
    ans = c1[0] if cur == 0 else c0[0]
    print(ans)


main()
