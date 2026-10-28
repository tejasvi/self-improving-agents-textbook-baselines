import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)
    hmax = min(u + d for u, d in zip(U, D))

    def feasible(H):
        # allowed interval for u_i: [max(0, H-D_i), min(U_i, H)]
        lo = H - D[0]
        if lo < 0:
            lo = 0
        hi = U[0] if U[0] < H else H
        L, R = lo, hi
        for i in range(1, n):
            d = D[i]
            lo = H - d
            if lo < 0:
                lo = 0
            hi = U[i] if U[i] < H else H
            t = L - x
            L = lo if lo > t else t
            t = R + x
            R = hi if hi < t else t
            if L > R:
                return False
        return True

    lo, hi = 0, hmax  # H=0 always feasible
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1
    print(total - n * lo)

main()
