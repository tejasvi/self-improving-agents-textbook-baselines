import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    m = 3 ** n
    s = s[:m]
    # cost to make leaf value 0 / value 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    # root value by majority
    v = [int(ch) for ch in s]
    while len(v) > 1:
        v = [1 if a + b + c >= 2 else 0 for a, b, c in zip(v[0::3], v[1::3], v[2::3])]
    rootval = v[0]
    while len(c0) > 1:
        n0 = []
        n1 = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            n0.append(a + b + c - max(a, b, c))
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            n1.append(a + b + c - max(a, b, c))
        c0, c1 = n0, n1
    ans = c1[0] if rootval == 0 else c0[0]
    print(ans)


main()
