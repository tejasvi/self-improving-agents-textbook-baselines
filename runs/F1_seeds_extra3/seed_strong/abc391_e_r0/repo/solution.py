import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    L = 3 ** n
    s = s[:L]
    # cost to make leaf equal to 0 / 1
    c0 = [0 if ch == "0" else 1 for ch in s]
    c1 = [1 - x for x in c0]
    vals = [1 if ch == "1" else 0 for ch in s]
    for _ in range(n):
        # root value by majority
        vals = [1 if (a + b + d) >= 2 else 0
                for a, b, d in zip(vals[0::3], vals[1::3], vals[2::3])]
        new0 = []
        new1 = []
        for group, out in ((c0, new0), (c1, new1)):
            a = group[0::3]
            b = group[1::3]
            d = group[2::3]
            out.extend(
                x + y + z - max(x, y, z)
                for x, y, z in zip(a, b, d)
            )
        c0, c1 = new0, new1
    root = vals[0]
    # minimum changes to flip root value
    ans = c1[0] if root == 0 else c0[0]
    print(ans)


main()
