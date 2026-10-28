import sys

def main():
    data = sys.stdin.read().split()
    N = int(data[0]); M = int(data[1]); S = data[2]
    MOD = 998244353
    S_len = N
    # Row f[0..N] with f[j]-f[j-1] in {0,1}; bit (j-1) set iff f[j]-f[j-1]==1.
    def decode(mask):
        f = [0] * (S_len + 1)
        for j in range(1, S_len + 1):
            f[j] = f[j - 1] + ((mask >> (j - 1)) & 1)
        return f

    def encode(f):
        mask = 0
        for j in range(1, S_len + 1):
            if f[j] - f[j - 1]:
                mask |= 1 << (j - 1)
        return mask

    num_states = 1 << S_len
    letters = [chr(ord('a') + i) for i in range(26)]
    trans = [[0] * 26 for _ in range(num_states)]
    for mask in range(num_states):
        f = decode(mask)
        for ci, c in enumerate(letters):
            g = [0] * (S_len + 1)
            for j in range(1, S_len + 1):
                g[j] = max(g[j - 1], f[j])
                if S[j - 1] == c:
                    g[j] = max(g[j], f[j - 1] + 1)
            trans[mask][ci] = encode(g)

    dp = [0] * num_states
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * num_states
        for mask in range(num_states):
            v = dp[mask]
            if v:
                row = trans[mask]
                for ci in range(26):
                    t = row[ci]
                    ndp[t] += v
        dp = [x % MOD for x in ndp]

    ans = [0] * (S_len + 1)
    for mask in range(num_states):
        ans[bin(mask).count('1')] = (ans[bin(mask).count('1')] + dp[mask]) % MOD
    print(' '.join(map(str, ans)))

main()
