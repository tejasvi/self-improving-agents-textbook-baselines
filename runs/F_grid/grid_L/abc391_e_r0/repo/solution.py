import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i]/c1[i]: min changes to make node i evaluate to 0 / 1
    c0 = [0 if ch == "0" else 1 for ch in s]
    c1 = [0 if ch == "1" else 1 for ch in s]
    # current root value computed by majority directly
    cur = [int(ch) for ch in s]
    while len(c0) > 1:
        nc0 = []
        nc1 = []
        ncur = []
        for i in range(0, len(c0), 3):
            a0, b0, d0 = c0[i], c0[i + 1], c0[i + 2]
            a1, b1, d1 = c1[i], c1[i + 1], c1[i + 2]
            x0 = sorted((a0, b0, d0))
            x1 = sorted((a1, b1, d1))
            nc0.append(x0[0] + x0[1])
            nc1.append(x1[0] + x1[1])
            ncur.append(1 if cur[i] + cur[i + 1] + cur[i + 2] >= 2 else 0)
        c0, c1, cur = nc0, nc1, ncur
    if cur[0] == 1:
        ans = c0[0]
    else:
        ans = c1[0]
    print(ans)


main()
