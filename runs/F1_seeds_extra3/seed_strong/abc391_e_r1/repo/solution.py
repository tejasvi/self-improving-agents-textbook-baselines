import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c[v][i]: min flips so node i evaluates to v
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 - x for x in c0]
    vals = [1 if ch == '1' else 0 for ch in s]
    while len(vals) > 1:
        # majority values, and min-cost-to-set-to-0 / 1 (sum of two smallest of three)
        vals = [1 if x + y + z >= 2 else 0 for x, y, z in zip(vals[0::3], vals[1::3], vals[2::3])]
        n0 = [x + y + z - max(x, y, z) for x, y, z in zip(c0[0::3], c0[1::3], c0[2::3])]
        n1 = [x + y + z - max(x, y, z) for x, y, z in zip(c1[0::3], c1[1::3], c1[2::3])]
        c0, c1 = n0, n1
    # cost to flip root value
    print(c1[0] if vals[0] == 0 else c0[0])

main()
