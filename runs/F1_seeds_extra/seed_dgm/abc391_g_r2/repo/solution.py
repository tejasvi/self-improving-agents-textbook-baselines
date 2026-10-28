import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0]); m = int(data[1]); s = data[2]
    MOD = 998244353
    S = 1 << n

    # state: bitmask b, bit j-1 = dp[j] - dp[j-1] for j=1..n
    trans = [[0] * 26 for _ in range(S)]
    for b in range(S):
        dp = [0] * (n + 1)
        for j in range(1, n + 1):
            dp[j] = dp[j - 1] + ((b >> (j - 1)) & 1)
        for c in range(26):
            ch = chr(97 + c)
            nd = [0] * (n + 1)
            for j in range(1, n + 1):
                v = nd[j - 1]
                if dp[j] > v:
                    v = dp[j]
                if s[j - 1] == ch and dp[j - 1] + 1 > v:
                    v = dp[j - 1] + 1
                nd[j] = v
            nb = 0
            for j in range(1, n + 1):
                if nd[j] - nd[j - 1]:
                    nb |= 1 << (j - 1)
            trans[b][c] = nb

    cnt = [0] * S
    cnt[0] = 1
    for _ in range(m):
        new = [0] * S
        for b in range(S):
            v = cnt[b]
            if v:
                tb = trans[b]
                for c in range(26):
                    t = tb[c]
                    new[t] += v
        cnt = [x % MOD for x in new]

    ans = [0] * (n + 1)
    for b in range(S):
        if cnt[b]:
            ans[bin(b).count("1")] = (ans[bin(b).count("1")] + cnt[b]) % MOD
    print(" ".join(map(str, ans)))

main()
