import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = [int(x) for x in data[1:1 + n]]
    maxs = 2 * max(a)
    # S[v] = sum over pairs i<=j with 2^v | (A_i+A_j) of (A_i+A_j)
    S = [0] * (maxs.bit_length() + 2)
    for v in range(len(S) - 1):
        M = 1 << v
        mask = M - 1
        cnt = {}
        sm = {}
        diag_sum = 0  # sum of 2*A_i over i with 2*A_i ≡ 0 mod M
        for x in a:
            r = x & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + x
            if (2 * x) & mask == 0:
                diag_sum += 2 * x
        ordered_sum = 0
        for r, c in cnt.items():
            q = (-r) & mask
            cq = cnt.get(q)
            if cq:
                ordered_sum += sm[r] * cq + c * sm[q]
        # ordered pair counts are not needed; only sums over unordered i<=j
        S[v] = (ordered_sum + diag_sum) // 2
    ans = 0
    for v in range(len(S) - 1):
        ans += (S[v] - S[v + 1]) >> v
    print(ans)


main()
