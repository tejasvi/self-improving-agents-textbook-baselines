import sys


def main():
    data = sys.stdin.read().split()
    n, x = int(data[0]), int(data[1])
    procs = []
    idx = 2
    for _ in range(n):
        a, p, b, q = (int(v) for v in data[idx:idx + 4])
        idx += 4
        procs.append((a, p, b, q))

    def proc_cost(w, a, p, b, q):
        # Optimal mix (x units of S, y units of T) satisfies x < b or y < a,
        # since swapping b units of S <-> a units of T preserves capacity a*b.
        best = None
        # Case y in [0, a-1]: take minimal x for each y.
        for y in range(a):
            rem = w - y * b
            if rem < 0:
                rem = 0
            c = y * q + (-(-rem // a)) * p
            if best is None or c < best:
                best = c
            if rem == 0:
                break
        # Case x in [0, b-1]: take minimal y for each x.
        for s in range(b):
            rem = w - s * a
            if rem < 0:
                rem = 0
            c = s * p + (-(-rem // b)) * q
            if c < best:
                best = c
            if rem == 0:
                break
        return best

    def cost(w):
        total = 0
        for a, p, b, q in procs:
            total += proc_cost(w, a, p, b, q)
            if total > x:
                return total
        return total

    lo, hi = 0, 100 * x + 100  # capacity 0 always costs 0
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if cost(mid) <= x:
            lo = mid
        else:
            hi = mid - 1
    print(lo)


main()
