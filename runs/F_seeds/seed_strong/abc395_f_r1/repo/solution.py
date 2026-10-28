import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)
    hmax = min(u + d for u, d in zip(U, D))

    def feasible(h):
        # interval for tooth i: [max(0, h-D_i), min(U_i, h)]
        l = max(0, h - D[0]); r = min(U[0], h)
        if l > r:
            return False
        for i in range(1, n):
            u = U[i]; d = D[i]
            lo = h - d
            if lo < 0:
                lo = 0
            hi = u if u < h else h
            t = l - x
            if t > lo:
                lo = t
            t = r + x
            if t < hi:
                hi = t
            if lo > hi:
                return False
            l = lo; r = hi
        return True

    lo, hi = 0, hmax
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)

main()
