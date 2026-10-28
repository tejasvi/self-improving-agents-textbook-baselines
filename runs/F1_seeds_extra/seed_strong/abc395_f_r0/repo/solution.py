import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0]); x = int(data[1])
    U = [int(v) for v in data[2:2 + 2 * n:2]]
    D = [int(v) for v in data[3:3 + 2 * n:2]]
    total = sum(U) + sum(D)

    def feasible(h):
        # u_i in [max(0,h-D_i), min(U_i,h)], |u_i - u_{i+1}| <= x
        lo = 0
        hi = 0
        first = True
        for i in range(n):
            l = h - D[i]
            if l < 0:
                l = 0
            r = U[i] if U[i] < h else h
            if first:
                first = False
            else:
                lo -= x
                hi += x
                if l < lo:
                    l = lo
                if r > hi:
                    r = hi
            if l > r:
                return False
            lo = l
            hi = r
        return True

    lo_h = 0
    hi_h = min(U[i] + D[i] for i in range(n))
    # feasible(0) is always true (all zeros); find max feasible h
    while lo_h < hi_h:
        mid = (lo_h + hi_h + 1) // 2
        if feasible(mid):
            lo_h = mid
        else:
            hi_h = mid - 1
    print(total - n * lo_h)

main()
