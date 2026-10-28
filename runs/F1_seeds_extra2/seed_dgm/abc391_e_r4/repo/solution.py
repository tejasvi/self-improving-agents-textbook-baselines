import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    s = s[:m]
    # c0[i], c1[i]: min flips to make node value 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [0 if ch == '1' else 1 for ch in s]
    # current root value via majority reduction
    cur = [int(ch) for ch in s]
    while len(cur) > 1:
        cur = [1 if cur[i] + cur[i + 1] + cur[i + 2] >= 2 else 0
               for i in range(0, len(cur), 3)]
    root = cur[0]
    while len(c0) > 1:
        n0 = []
        n1 = []
        for i in range(0, len(c0), 3):
            a, b, c = c0[i], c0[i + 1], c0[i + 2]
            n0.append(a + b + c - max(a, b, c))
            a, b, c = c1[i], c1[i + 1], c1[i + 2]
            n1.append(a + b + c - max(a, b, c))
        c0, c1 = n0, n1
    ans = c1[0] if root == 0 else c0[0]
    print(ans)


main()
