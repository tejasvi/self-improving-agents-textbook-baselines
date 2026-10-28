import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])[:3 ** n]
    # c0[i] / c1[i]: min flips to make subtree i evaluate to 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 - x for x in c0]
    vals = [1 if ch == '1' else 0 for ch in s]
    while len(c0) > 1:
        n0 = []
        n1 = []
        for a, b, c in zip(c0[0::3], c0[1::3], c0[2::3]):
            n0.append(a + b + c - max(a, b, c))
        for a, b, c in zip(c1[0::3], c1[1::3], c1[2::3]):
            n1.append(a + b + c - max(a, b, c))
        c0, c1 = n0, n1
        vals = [(a + b + c) // 2 for a, b, c in zip(vals[0::3], vals[1::3], vals[2::3])]
    print(c1[0] if vals[0] == 0 else c0[0])


main()
