import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = [int(x) for x in data[1:1 + n]]
    maxs = 2 * max(A)

    # f(s) = s - sum_{k>=1} [2^k | s] * s / 2^k
    # For each M = 2^k, compute T_M = sum over pairs i<=j with M | (A_i+A_j) of (A_i+A_j)
    # Then answer = sum_k sign_k * T_{2^k} / 2^k, with sign +1 for k=0, -1 otherwise.
    ans = 0
    M = 1
    k = 0
    while M <= maxs:
        mask = M - 1
        S = {}
        C = {}
        for a in A:
            r = a & mask
            if r in S:
                S[r] += a
                C[r] += 1
            else:
                S[r] = a
                C[r] = 1
        ordered = 0
        for r, s in S.items():
            p = (M - r) & mask
            cp = C.get(p)
            if cp:
                ordered += s * cp
        # ordered counts all ordered pairs incl. i=j, sum of A_i (not A_i+A_j):
        # sum over ordered (i,j) of (A_i+A_j) = 2 * sum_r S_r * C_{-r}
        ordered *= 2
        # diagonal: i=j with 2A_i = s, contributes 2A_i once in unordered sum
        diag = 0
        for a in A:
            if (2 * a) & mask == 0:
                diag += 2 * a
        total = (ordered + diag) // 2  # sum over unordered i<=j with M | s of s
        term = total // M
        if k == 0:
            ans += term
        else:
            ans -= term
        M <<= 1
        k += 1
    print(ans)


main()
