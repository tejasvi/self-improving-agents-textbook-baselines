import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    P = [int(x) for x in data[1:1 + n]]
    Q = [int(x) for x in data[1 + n:1 + 2 * n]]
    # a[i]: rank of row i (1-indexed position of i in P); b[j]: rank of column j in Q
    a = [0] * (n + 1)
    b = [0] * (n + 1)
    for pos, v in enumerate(P, 1):
        a[v] = pos
    for pos, v in enumerate(Q, 1):
        b[v] = pos
    out = []
    for i in range(1, n + 1):
        ai = a[i]
        out.append(''.join('1' if ai + b[j] > n else '0' for j in range(1, n + 1)))
    sys.stdout.write('\n'.join(out) + '\n')


main()
