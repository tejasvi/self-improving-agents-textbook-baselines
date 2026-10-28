import sys


def achievable_fixed_counts(N):
    # Variable (non-fixed) cells form disjoint rectangles, each at least 2x2,
    # using disjoint row sets and column sets. F[r][c] is a bitset over the
    # number of variable cells achievable using at most r rows and c columns.
    F = [[0] * (N + 1) for _ in range(N + 1)]
    for r in range(N + 1):
        for c in range(N + 1):
            if r == 0 or c == 0:
                F[r][c] = 1  # zero variable cells
                continue
            s = F[r - 1][c] | F[r][c - 1]
            for a in range(2, r + 1):
                for b in range(2, c + 1):
                    s |= F[r - a][c - b] << (a * b)
            F[r][c] = s
    total = N * N
    bits = F[N][N]
    # convert variable counts to fixed counts
    result = [False] * (total + 1)
    for v in range(total + 1):
        if bits >> v & 1:
            result[total - v] = True
    return result


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    Q = int(data[1])
    ok = achievable_fixed_counts(N)
    out = []
    for i in range(Q):
        k = int(data[2 + i])
        out.append("Yes" if 0 <= k <= N * N and ok[k] else "No")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
