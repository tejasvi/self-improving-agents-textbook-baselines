import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    # column c (0-based, by X) -> row r (0-based, by Y)
    row_of_col = [0] * n
    for i in range(n):
        x = int(data[1 + 2 * i]) - 1
        y = int(data[2 + 2 * i]) - 1
        row_of_col[x] = y
    col_of_row = [0] * n
    for c in range(n):
        col_of_row[row_of_col[c]] = c

    full = (1 << n) - 1
    # comp[c]: columns c' that are NE/SW comparable with c
    comp = [0] * n
    for c in range(n):
        m = 0
        rc = row_of_col[c]
        for d in range(n):
            if d != c and (d - c) * (row_of_col[d] - rc) > 0:
                m |= 1 << d
        comp[c] = m

    # PC[k] = columns < k
    PC = [(1 << k) - 1 for k in range(n + 1)]
    # PR[k] = columns of points whose row < k
    PR = [0] * (n + 1)
    for r in range(n):
        PR[r + 1] = PR[r] | (1 << col_of_row[r])

    def valid(box):
        b = box
        while b:
            low = b & -b
            j = low.bit_length() - 1
            if comp[j] & box == 0:
                return False
            b ^= low
        return True

    # empty chain: whole set must have no isolated point
    ans = 1 if valid(full) else 0

    dp = [0] * n
    for p in range(n):
        rp = row_of_col[p]
        val = 0
        # chain starts at p: cell 0 = columns < p, rows > rp
        box0 = PC[p] & (full ^ PR[rp + 1])
        if valid(box0):
            val = 1
        # predecessors q: columns < p, rows > rp
        for q in range(p):
            rq = row_of_col[q]
            if rq > rp and dp[q]:
                box = (PC[p] ^ PC[q + 1]) & (PR[rq] ^ PR[rp + 1])
                if valid(box):
                    val += dp[q]
        dp[p] = val % MOD
        # chain ends at p: cell m = columns > p, rows < rp
        if dp[p]:
            boxm = (full ^ PC[p + 1]) & PR[rp]
            if valid(boxm):
                ans += dp[p]
    print(ans % MOD)


main()
