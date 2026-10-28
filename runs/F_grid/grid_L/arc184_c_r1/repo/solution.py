import sys

# Crease n (1-indexed) is a mountain fold iff, writing n = 2^v * m with m odd,
# m % 4 == 3, i.e. bit (v+1) of n is set.
#
# We choose x >= 1 with x + A_N < 2^B (B = 100) and maximize
#   f(x) = sum_k [crease (x + A_k) is a mountain].
# Digit DP over the bits of x from low to high. For each k we track the carry
# into the current bit of x + A_k, and a status:
#   Z: no set bit seen yet, P: lowest set bit was at the previous position
#   (the next bit is decisive), D: decisive bit already processed.
# All per-k quantities are stored as bitmasks over k, so each transition is a
# handful of big-integer operations. Only O(N) distinct states occur per level.


def solve(N, A, B=100):
    full = (1 << N) - 1
    abits = []
    for j in range(B):
        m = 0
        for k in range(N):
            if (A[k] >> j) & 1:
                m |= 1 << k
        abits.append(m)

    # state: (carry, P, D, nz) ; Z = full & ~(P | D)
    dp = {(0, 0, 0, 0): 0}
    for j in range(B):
        a = abits[j]
        ndp = {}
        for (c, P, D, nz), val in dp.items():
            Z = full & ~(P | D)
            for b in (0, 1):
                if b == 0:
                    nbit = a ^ c
                    ncar = a & c
                else:
                    nbit = full & ~(a ^ c)
                    ncar = a | c
                gain = bin(P & nbit).count("1")
                nP = Z & nbit
                nD = D | P
                key = (ncar, nP, nD, nz | b)
                nval = val + gain
                if ndp.get(key, -1) < nval:
                    ndp[key] = nval
        dp = ndp
    best = 0
    for (c, P, D, nz), val in dp.items():
        if nz and c == 0:
            best = max(best, val)
    return best


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:1 + N]]
    print(solve(N, A))


if __name__ == "__main__":
    main()
