import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    a = list(map(int, data[1:1 + n]))
    K = 26  # s <= 2e7 < 2^25, so T_k = 0 for k >= 25
    T = [0] * (K + 2)
    for k in range(K + 1):
        M = 1 << k
        mask = M - 1
        cnt = {}
        sm = {}
        diag_cnt = 0
        diag_sum = 0
        for x in a:
            r = x & mask
            cnt[r] = cnt.get(r, 0) + 1
            sm[r] = sm.get(r, 0) + x
            if (2 * x) & mask == 0:
                diag_cnt += 1
                diag_sum += 2 * x
        O = 0  # ordered-pair sum of (A_i + A_j) with residues summing to 0 mod M
        for r, c in cnt.items():
            t = (-r) & mask
            ct = cnt.get(t)
            if ct is None:
                continue
            O += sm[r] * ct + c * sm[t]
        T[k] = (O + diag_sum) // 2
    # ans = sum_k (T_k - T_{k+1}) / 2^k ; scale by 2^K
    total = 0
    for k in range(K + 1):
        total += (T[k] - T[k + 1]) << (K - k)
    print(total >> K)


main()
