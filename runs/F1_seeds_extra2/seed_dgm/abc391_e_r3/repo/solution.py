import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()[:3 ** n]
    # c0[i] / c1[i]: min flips so that node i evaluates to 0 / 1.
    # A leaf costs 0 for its own value and 1 for the other.
    # A gate forces v by making at least two of its three children v:
    # cost = sum of the two smallest child costs = total - max.
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [1 - x for x in c0]
    for _ in range(n):
        k = len(c0) // 3
        n0 = [0] * k
        n1 = [0] * k
        for i in range(k):
            a = 3 * i
            x, y, z = c0[a], c0[a + 1], c0[a + 2]
            n0[i] = x + y + z - max(x, y, z)
            x, y, z = c1[a], c1[a + 1], c1[a + 2]
            n1[i] = x + y + z - max(x, y, z)
        c0, c1 = n0, n1
    # Actual root value is the one that costs 0 to force.
    if c0[0] == 0:
        ans = c1[0]
    else:
        ans = c0[0]
    print(ans)


main()
