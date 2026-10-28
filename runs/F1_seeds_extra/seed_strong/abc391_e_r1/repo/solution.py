import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = "".join(data[1:])
    m = 3 ** n
    s = s[:m]
    # c0[i], c1[i]: min cost for the current node to output 0 / 1
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 if ch == '0' else 0 for ch in s]
    for _ in range(n):
        n0 = []
        n1 = []
        ap0 = n0.append
        ap1 = n1.append
        it0 = iter(c0)
        it1 = iter(c1)
        for a, b, c in zip(it0, it0, it0):
            ap0(a + b + c - max(a, b, c))
        for a, b, c in zip(it1, it1, it1):
            ap1(a + b + c - max(a, b, c))
        c0, c1 = n0, n1
    # The current root value has cost 0; the answer is the cost of flipping it.
    if c0[0] == 0:
        ans = c1[0]
    else:
        ans = c0[0]
    print(ans)


main()
