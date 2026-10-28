# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def solve():
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    s_vals = [ord(c) - 97 for c in S]

    # initial state: dp array of length N+1 all zeros
    init_state = tuple([0] * (N + 1))
    # DP dictionaries: mapping state -> count
    cur = {init_state: 1}
    # cache transitions for (state, char)
    trans_cache = {}

    for _ in range(M):
        nxt = {}
        for state, cnt in cur.items():
            for ch in range(26):
                key = (state, ch)
                if key in trans_cache:
                    ns = trans_cache[key]
                else:
                    # compute next dp
                    dp = list(state)
                    newdp = [0] * (N + 1)
                    for i in range(1, N + 1):
                        # Option 1: skip character in S (i.e., keep dp[i])
                        val = dp[i]
                        # Option 2: use result from previous i (newdp[i-1])
                        if newdp[i-1] > val:
                            val = newdp[i-1]
                        # Option 3: match if characters equal
                        if s_vals[i-1] == ch:
                            cand = dp[i-1] + 1
                            if cand > val:
                                val = cand
                        newdp[i] = val
                    ns = tuple(newdp)
                    trans_cache[key] = ns
                nxt[ns] = (nxt.get(ns, 0) + cnt) % MOD
        cur = nxt

    # aggregate answers by final LCS length (dp[N])
    ans = [0] * (N + 1)
    for state, cnt in cur.items():
        k = state[-1]
        ans[k] = (ans[k] + cnt) % MOD

    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()
