import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    m = int(data[1])
    pts = []
    for k in range(m):
        a = int(data[2 + 2 * k])
        b = int(data[3 + 2 * k])
        pts.append((a, b))
    R = {a for a, _ in pts}
    C = {b for _, b in pts}
    S = {a + b for a, b in pts}
    D = {a - b for a, b in pts}

    # Free rows x free cols
    F = (n - len(R)) * (n - len(C))

    def count_family(vals, is_sum):
        # Count pairs (i,j), i not in R, j not in C, with i+j=s (is_sum)
        # or i-j=d (not is_sum), over 1<=i,j<=n.
        total = 0
        for v in vals:
            if is_sum:
                lo = max(1, v - n)
                hi = min(n, v - 1)
            else:
                lo = max(1, 1 + v)
                hi = min(n, n + v)
            if lo > hi:
                continue
            L = hi - lo + 1
            # i in R within range
            rows_in = sum(1 for r in R if lo <= r <= hi)
            # i such that j=f(i) in C, within range (i determined by c)
            cols_in = 0
            for c in C:
                i = (v - c) if is_sum else (c + v)
                if lo <= i <= hi:
                    cols_in += 1
            # both i in R and f(i) in C
            both = 0
            for r in R:
                if lo <= r <= hi:
                    j = (v - r) if is_sum else (r - v)
                    if j in C:
                        both += 1
            total += L - rows_in - cols_in + both
        return total

    A = count_family(S, True)
    B = count_family(D, False)

    # Pairs with i+j in S and i-j in D, both free
    AB = 0
    for s in S:
        for d in D:
            if (s + d) % 2:
                continue
            i = (s + d) // 2
            j = (s - d) // 2
            if 1 <= i <= n and 1 <= j <= n and i not in R and j not in C:
                AB += 1

    print(F - A - B + AB)


main()
