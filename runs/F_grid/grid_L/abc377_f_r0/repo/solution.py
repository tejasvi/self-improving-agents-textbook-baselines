import sys


def main():
    data = sys.stdin.read().split()
    n, m = int(data[0]), int(data[1])
    pts = [(int(data[2 + 2 * k]), int(data[3 + 2 * k])) for k in range(m)]
    R = sorted({a for a, _ in pts})
    C = sorted({b for _, b in pts})
    Rset = set(R)
    Cset = set(C)
    S = sorted({a + b for a, b in pts})
    D = sorted({a - b for a, b in pts})

    def count_in(sorted_list, lo, hi):
        if lo > hi:
            return 0
        import bisect
        return bisect.bisect_right(sorted_list, hi) - bisect.bisect_left(sorted_list, lo)

    # free cells: rows not in R and columns not in C
    free_rc = (n - len(R)) * (n - len(C))

    # anti-diagonals i+j = s
    sum_anti = 0
    for s in S:
        lo = max(1, s - n)
        hi = min(n, s - 1)
        if lo > hi:
            continue
        total = hi - lo + 1
        total -= count_in(R, lo, hi)
        total -= count_in(C, s - hi, s - lo)
        for i in R:
            if lo <= i <= hi and (s - i) in Cset:
                total += 1
        sum_anti += total

    # diagonals i-j = d
    sum_diag = 0
    for d in D:
        lo = max(1, 1 + d)
        hi = min(n, n + d)
        if lo > hi:
            continue
        total = hi - lo + 1
        total -= count_in(R, lo, hi)
        total -= count_in(C, lo - d, hi - d)
        for i in R:
            if lo <= i <= hi and (i - d) in Cset:
                total += 1
        sum_diag += total

    # cells on both an anti-diagonal in S and a diagonal in D, free of rows/cols
    both = 0
    for s in S:
        for d in D:
            if (s + d) % 2:
                continue
            i = (s + d) // 2
            j = (s - d) // 2
            if 1 <= i <= n and 1 <= j <= n and i not in Rset and j not in Cset:
                both += 1

    union_diag = sum_anti + sum_diag - both
    print(free_rc - union_diag)


main()
