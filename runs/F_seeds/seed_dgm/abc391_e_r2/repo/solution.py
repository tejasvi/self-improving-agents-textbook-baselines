import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    vals = [1 if ch == '1' else 0 for ch in s[:m]]
    # c0[i]: min flips to make node i equal 0; c1[i]: min flips to make it 1
    c0 = vals[:]
    c1 = [1 - v for v in vals]
    for _ in range(n):
        nv = []
        nc0 = []
        nc1 = []
        for i in range(0, len(vals), 3):
            a, b, c = vals[i], vals[i + 1], vals[i + 2]
            nv.append(1 if a + b + c >= 2 else 0)
            x, y, z = c0[i], c0[i + 1], c0[i + 2]
            nc0.append(x + y + z - max(x, y, z))
            x, y, z = c1[i], c1[i + 1], c1[i + 2]
            nc1.append(x + y + z - max(x, y, z))
        vals, c0, c1 = nv, nc0, nc1
    # Flipping the root's value requires making it the opposite value.
    ans = c0[0] if vals[0] == 1 else c1[0]
    print(ans)


main()
