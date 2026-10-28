import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i]: min cost to make node i evaluate to 0; c1[i]: to evaluate to 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [0 if ch == '1' else 1 for ch in s]
    # root value
    cur = s
    for _ in range(n):
        nc0 = []
        nc1 = []
        nv = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            # sum of two smallest
            if a > b:
                a, b = b, a
            if c < a:
                nc0.append(a + c)
            elif c < b:
                nc0.append(a + c)
            else:
                nc0.append(a + b)
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            if a > b:
                a, b = b, a
            if c < a:
                nc1.append(c + a)
            elif c < b:
                nc1.append(a + c)
            else:
                nc1.append(a + b)
        c0, c1 = nc0, nc1
    root = 1 if c1[0] == 0 else 0
    # root value r: cost to flip = f(root, 1-r)
    ans = c0[0] if root == 1 else c1[0]
    print(ans)


main()
