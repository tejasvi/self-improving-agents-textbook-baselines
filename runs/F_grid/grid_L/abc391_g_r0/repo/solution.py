import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    M = int(data[1])
    S = data[2]
    MOD = 998244353

    # State: bitmask d over j=1..N, d_j = L[j]-L[j-1] in {0,1}, bit (j-1).
    # L is the LCS row of current T-prefix against S[:j].
    def row_from_mask(mask):
        L = [0] * (N + 1)
        for j in range(1, N + 1):
            L[j] = L[j - 1] + ((mask >> (j - 1)) & 1)
        return L

    trans = [[0] * 26 for _ in range(1 << N)]
    for mask in range(1 << N):
        L = row_from_mask(mask)
        for c in range(26):
            ch = chr(ord('a') + c)
            Lp = [0] * (N + 1)
            for j in range(1, N + 1):
                v = L[j]
                if Lp[j - 1] > v:
                    v = Lp[j - 1]
                if S[j - 1] == ch and L[j - 1] + 1 > v:
                    v = L[j - 1] + 1
                Lp[j] = v
            nm = 0
            for j in range(1, N + 1):
                if Lp[j] - Lp[j - 1]:
                    nm |= 1 << (j - 1)
            trans[mask][c] = nm

    dp = [0] * (1 << N)
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * (1 << N)
        for mask in range(1 << N):
            v = dp[mask]
            if v == 0:
                continue
            tr = trans[mask]
            for c in range(26):
                nm = tr[c]
                ndp[nm] = (ndp[nm] + v) % MOD
        dp = ndp

    ans = [0] * (N + 1)
    for mask in range(1 << N):
        ans[bin(mask).count('1')] = (ans[bin(mask).count('1')] + dp[mask]) % MOD
    print(' '.join(map(str, ans)))

main()
