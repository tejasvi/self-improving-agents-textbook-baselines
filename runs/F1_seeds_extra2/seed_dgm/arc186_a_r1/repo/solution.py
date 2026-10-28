import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    Q = int(data[1])
    Ks = [int(x) for x in data[2:2 + Q]]
    M = N * N

    # S[r][c]: bitset of achievable free-cell counts using at most r rows
    # and at most c columns, where free cells form disjoint a x b blocks
    # (a, b >= 2) occupying distinct rows and columns.
    S = [[0] * (N + 1) for _ in range(N + 1)]
    for r in range(N + 1):
        for c in range(N + 1):
            if r == 0 and c == 0:
                S[r][c] = 1
                continue
            v = 0
            if r > 0:
                v |= S[r - 1][c]
            if c > 0:
                v |= S[r][c - 1]
            for a in range(2, r + 1):
                for b in range(2, c + 1):
                    v |= S[r - a][c - b] << (a * b)
            S[r][c] = v
    reach = S[N][N]

    out = []
    for K in Ks:
        free = M - K
        if 0 <= free <= M and (reach >> free) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
