import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    P = [int(x) for x in data[1:1 + n]]
    Q = [int(x) for x in data[1 + n:1 + 2 * n]]
    # r[i]: 1-based rank of row i in P; c[j]: 1-based rank of column j in Q
    r = [0] * (n + 1)
    c = [0] * (n + 1)
    for k, p in enumerate(P, 1):
        r[p] = k
    for k, q in enumerate(Q, 1):
        c[q] = k
    # B[a][b] = 1 iff a + b >= n + 1 (rows and columns strictly increasing)
    out = []
    for i in range(1, n + 1):
        a = r[i]
        row = ''.join('1' if a + c[j] >= n + 1 else '0' for j in range(1, n + 1))
        out.append(row)
    sys.stdout.write('\n'.join(out) + '\n')


if __name__ == '__main__':
    main()
