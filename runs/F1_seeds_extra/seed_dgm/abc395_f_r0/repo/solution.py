import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    x = int(data[1])
    U = [0] * n
    D = [0] * n
    for i in range(n):
        U[i] = int(data[2 + 2 * i])
        D[i] = int(data[3 + 2 * i])

    total = sum(U) + sum(D)

    def feasible(H):
        # Reachable set of U' values is always an interval [a, b].
        a = b = 0
        for i in range(n):
            L = H - D[i]
            if L < 0:
                L = 0
            R = U[i] if U[i] < H else H
            if i == 0:
                a, b = L, R
            else:
                a -= x
                b += x
                if a < L:
                    a = L
                if b > R:
                    b = R
            if a > b:
                return False
        return True

    # Feasibility is monotone in H; H = 0 is always feasible.
    lo = 0
    hi = min(U[i] + D[i] for i in range(n))
    while lo < hi:
        mid = (lo + hi + 1) // 2
        if feasible(mid):
            lo = mid
        else:
            hi = mid - 1

    # Each tooth pair costs exactly U_i + D_i - H after reduction.
    print(total - n * lo)


main()
