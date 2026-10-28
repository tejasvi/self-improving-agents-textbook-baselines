import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    q = int(data[1])
    ks = [int(x) for x in data[2:2 + q]]

    # A cell is free (not fixed) iff it lies in one of disjoint "free" blocks,
    # each block being an r x c submatrix with r, c >= 2, blocks using disjoint
    # rows and columns. reach[a][b] is a bitmask of achievable free counts
    # using at most a rows and at most b columns.
    reach = [[0] * (n + 1) for _ in range(n + 1)]
    for a in range(n + 1):
        for b in range(n + 1):
            if a == 0 or b == 0:
                reach[a][b] = 1  # only 0 free cells
                continue
            val = reach[a - 1][b] | reach[a][b - 1]
            for r in range(2, a + 1):
                for c in range(2, b + 1):
                    val |= reach[a - r][b - c] << (r * c)
            reach[a][b] = val
    best = reach[n][n]

    out = []
    total = n * n
    for k in ks:
        free = total - k
        if 0 <= free <= total and (best >> free) & 1:
            out.append("Yes")
        else:
            out.append("No")
    sys.stdout.write("\n".join(out) + "\n")


main()
