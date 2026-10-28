import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i], c1[i]: min flips to make node i equal 0 / 1
    c0 = [0 if ch == "0" else 1 for ch in s]
    c1 = [1 if ch == "0" else 0 for ch in s]
    val = [1 if ch == "1" else 0 for ch in s]
    for _ in range(n):
        L = len(val)
        nc0 = [0] * (L // 3)
        nc1 = [0] * (L // 3)
        nv = [0] * (L // 3)
        for g in range(L // 3):
            i = 3 * g
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            # sum of two smallest
            if a > b:
                a, b = b, a
            if c < a:
                nc0[g] = c + a
            elif c < b:
                nc0[g] = a + c
            else:
                nc0[g] = a + b
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            if a > b:
                a, b = b, a
            if c < a:
                nc1[g] = c + a
            elif c < b:
                nc1[g] = a + c
            else:
                nc1[g] = a + b
            nv[g] = 1 if val[i] + val[i + 1] + val[i + 2] >= 2 else 0
        c0, c1, val = nc0, nc1, nv
    root = val[0]
    ans = c1[0] if root == 0 else c0[0]
    print(ans)


main()
