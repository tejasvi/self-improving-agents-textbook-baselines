import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)
    cap = min(u + d for u, d in zip(U, D))
    pairs = list(zip(U, D))

    def feasible(H):
        L = -(1 << 62)
        R = 1 << 62
        for u, d in pairs:
            lo = H - d
            if lo < 0:
                lo = 0
            hi = u if u < H else H
            nl = L - x
            if nl < lo:
                nl = lo
            nr = R + x
            if nr > hi:
                nr = hi
            if nl > nr:
                return False
            L = nl
            R = nr
        return True

    lo, hi = 0, cap
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)

main()
