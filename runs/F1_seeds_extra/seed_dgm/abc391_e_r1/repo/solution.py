import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    s = s[:m]
    # c0[i]: min changes to make node i evaluate to 0; c1 similarly
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [0 if ch == '1' else 1 for ch in s]
    for _ in range(n):
        nc0 = []
        nc1 = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            nc0.append(a + b + c - max(a, b, c))
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            nc1.append(a + b + c - max(a, b, c))
        c0, c1 = nc0, nc1
    # Recompute root value via majority of the original string
    vals = [1 if ch == '1' else 0 for ch in s]
    for _ in range(n):
        vals = [1 if (vals[i] + vals[i + 1] + vals[i + 2]) >= 2 else 0
                for i in range(0, len(vals), 3)]
    rv = vals[0]
    ans = c1[0] if rv == 0 else c0[0]
    print(ans)


main()
