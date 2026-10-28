import sys


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    Q = int(data[1])
    Ks = [int(x) for x in data[2:2 + Q]]

    # poss[r][c]: bitset of achievable "non-fixed cell counts" using
    # at most r rows and at most c columns. Non-fixed cells form a union of
    # disjoint a x b rectangles (a, b >= 2) occupying disjoint row/column sets.
    poss = [[0] * (N + 1) for _ in range(N + 1)]
    for r in range(N + 1):
        for c in range(N + 1):
            if r == 0 and c == 0:
                poss[r][c] = 1
                continue
            v = 0
            if r > 0:
                v |= poss[r - 1][c]
            if c > 0:
                v |= poss[r][c - 1]
            for a in range(2, r + 1):
                for b in range(2, c + 1):
                    v |= poss[r - a][c - b] << (a * b)
            poss[r][c] = v
    reach = poss[N][N]

    out = []
    for K in Ks:
        if K < 0 or K > N * N:
            out.append("No")
            continue
        x = N * N - K
        out.append("Yes" if (reach >> x) & 1 else "No")
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
