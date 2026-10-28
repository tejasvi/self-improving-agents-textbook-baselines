import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    # state: bitmask over j=1..N, bit j-1 = q[j]-q[j-1] of LCS row
    trans = []
    for mask in range(1 << N):
        p = [0] * (N + 1)
        for j in range(1, N + 1):
            p[j] = p[j - 1] + ((mask >> (j - 1)) & 1)
        cnt = {}
        for c in range(26):
            ch = chr(97 + c)
            q = [0] * (N + 1)
            for j in range(1, N + 1):
                v = q[j - 1]
                if p[j] > v:
                    v = p[j]
                if S[j - 1] == ch and p[j - 1] + 1 > v:
                    v = p[j - 1] + 1
                q[j] = v
            nm = 0
            for j in range(1, N + 1):
                if q[j] - q[j - 1]:
                    nm |= 1 << (j - 1)
            cnt[nm] = cnt.get(nm, 0) + 1
        trans.append(list(cnt.items()))
    dp = [0] * (1 << N)
    dp[0] = 1
    for _ in range(M):
        nd = [0] * (1 << N)
        for s in range(1 << N):
            v = dp[s]
            if v:
                for t, w in trans[s]:
                    nd[t] = (nd[t] + v * w) % MOD
        dp = nd
    ans = [0] * (N + 1)
    for s in range(1 << N):
        if dp[s]:
            ans[bin(s).count("1")] = (ans[bin(s).count("1")] + dp[s]) % MOD
    print(" ".join(map(str, ans)))

main()
