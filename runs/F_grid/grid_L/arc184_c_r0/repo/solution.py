import sys


def solve(N, A, L=100):
    # Crease j (1-indexed) is a mountain fold iff the bit just above the
    # lowest set bit of j is 1 (checked against both samples).
    # Digit DP over bits of i (LSB first); x_k = i + A_k.
    # State (bitmasks over k):
    #   C : carry into the current bit
    #   U : x_k's bits so far are all 0
    #   P : lowest set bit of x_k is the previous bit
    # Value = number of mountain creases counted so far.
    FULL = (1 << N) - 1
    abits = []
    for t in range(L + 1):
        m = 0
        for k, a in enumerate(A):
            if (a >> t) & 1:
                m |= 1 << k
        abits.append(m)

    dp = {(0, FULL, 0, False): 0}
    for t in range(L):
        Ab = abits[t]
        ndp = {}
        for (C, U, P, nz), val in dp.items():
            for s in (0, 1):
                S = FULL if s else 0
                b = Ab ^ S ^ C              # bit t of x_k
                newC = (Ab | C) if s else (Ab & C)
                nb0 = FULL & ~b
                gain = bin(P & b).count("1")
                nU = U & nb0
                nP = U & b
                key = (newC, nU, nP, nz or bool(s))
                nv = val + gain
                if ndp.get(key, -1) < nv:
                    ndp[key] = nv
        dp = ndp

    best = -1
    for (C, U, P, nz), val in dp.items():
        # C == 0: x_k < 2^L for all k. nz: i != 0.
        if C == 0 and nz:
            best = max(best, val)
    return best


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:1 + N]]
    print(solve(N, A))


if __name__ == "__main__":
    main()
