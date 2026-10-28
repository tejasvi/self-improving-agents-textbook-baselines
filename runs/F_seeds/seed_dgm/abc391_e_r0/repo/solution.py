import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    m = 3 ** n
    s = s[:m]
    # cost[v] lists: cost to make each node evaluate to v
    c0 = [0 if ch == '0' else 1 for ch in s]
    c1 = [0 if ch == '1' else 1 for ch in s]
    for _ in range(n):
        n0 = []
        n1 = []
        for i in range(0, len(c0), 3):
            a0, b0, d0 = c0[i], c0[i + 1], c0[i + 2]
            a1, b1, d1 = c1[i], c1[i + 1], c1[i + 2]
            # two smallest sums
            n0.append(a0 + b0 + d0 - max(a0, b0, d0))
            n1.append(a1 + b1 + d1 - max(a1, b1, d1))
        c0, c1 = n0, n1
    # Root value under majority
    val = 1 if c1[0] < c0[0] else 0
    # Cost to flip root value = cost to make it the opposite
    print(c0[0] if val == 1 else c1[0])


main()
