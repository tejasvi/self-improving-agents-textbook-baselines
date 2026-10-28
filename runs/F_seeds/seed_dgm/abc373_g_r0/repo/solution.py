import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 4 * n]))
    P = [(vals[2 * i], vals[2 * i + 1]) for i in range(n)]
    off = 2 * n
    Q = [(vals[off + 2 * i], vals[off + 2 * i + 1]) for i in range(n)]
    R = list(range(n))

    def cross_o(a, b, c):
        return (b[0] - a[0]) * (c[1] - a[1]) - (b[1] - a[1]) * (c[0] - a[0])

    def crosses(i, j):
        p1, q1 = P[i], Q[R[i]]
        p2, q2 = P[j], Q[R[j]]
        o1 = cross_o(p1, q1, p2)
        o2 = cross_o(p1, q1, q2)
        if (o1 > 0) == (o2 > 0):
            return False
        o3 = cross_o(p2, q2, p1)
        o4 = cross_o(p2, q2, q1)
        return (o3 > 0) != (o4 > 0)

    # Swapping partners of crossing segments strictly decreases total length,
    # so this terminates with a non-crossing matching.
    changed = True
    while changed:
        changed = False
        for i in range(n):
            for j in range(i + 1, n):
                if crosses(i, j):
                    R[i], R[j] = R[j], R[i]
                    changed = True

    print(" ".join(str(r + 1) for r in R))


main()
