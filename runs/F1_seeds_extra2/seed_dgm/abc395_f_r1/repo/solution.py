import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = []
    D = []
    idx = 2
    for _ in range(n):
        U.append(int(data[idx]))
        D.append(int(data[idx + 1]))
        idx += 2
    total = sum(U) + sum(D)
    hmax = min(U[i] + D[i] for i in range(n))

    def feasible(H):
        # u_i in [max(0, H-D_i), min(U_i, H)], |u_i - u_{i+1}| <= x
        a = max(0, H - D[0])
        b = min(U[0], H)
        for i in range(1, n):
            lo = H - D[i]
            if lo < 0:
                lo = 0
            hi = U[i] if U[i] < H else H
            a2 = a - x
            if a2 < lo:
                a2 = lo
            b2 = b + x
            if b2 > hi:
                b2 = hi
            if a2 > b2:
                return False
            a, b = a2, b2
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
