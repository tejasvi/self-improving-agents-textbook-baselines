# Write your solution here. Read from stdin, write to stdout.
import sys
MOD = 998244353

def solve():
    data = sys.stdin.read().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2].strip()
    S_int = [ord(c) - ord('a') for c in S]
    # State: tuple of length N+1, dp values for prefixes of S
    from collections import deque, defaultdict
    start_state = tuple([0] * (N + 1))
    state_to_idx = {start_state: 0}
    states = [start_state]
    q = deque([start_state])
    # Precompute transitions mapping after we have all states
    while q:
        st = q.popleft()
        # generate next states for all 26 chars
        for c in range(26):
            # compute next state
            prev = st
            new = [0] * (N + 1)
            for i in range(1, N + 1):
                val = prev[i]
                if new[i-1] > val:
                    val = new[i-1]
                if S_int[i-1] == c:
                    cand = prev[i-1] + 1
                    if cand > val:
                        val = cand
                new[i] = val
            nxt = tuple(new)
            if nxt not in state_to_idx:
                state_to_idx[nxt] = len(states)
                states.append(nxt)
                q.append(nxt)
    S_cnt = len(states)
    # Build transition multiplicities
    trans = [defaultdict(int) for _ in range(S_cnt)]
    for idx, st in enumerate(states):
        for c in range(26):
            prev = st
            new = [0] * (N + 1)
            for i in range(1, N + 1):
                val = prev[i]
                if new[i-1] > val:
                    val = new[i-1]
                if S_int[i-1] == c:
                    cand = prev[i-1] + 1
                    if cand > val:
                        val = cand
                new[i] = val
            nxt = tuple(new)
            nxt_idx = state_to_idx[nxt]
            trans[idx][nxt_idx] += 1
    # DP over length M
    dp = [0] * S_cnt
    dp[0] = 1
    for _ in range(M):
        ndp = [0] * S_cnt
        for idx, val in enumerate(dp):
            if val == 0:
                continue
            for nxt_idx, mult in trans[idx].items():
                ndp[nxt_idx] = (ndp[nxt_idx] + val * mult) % MOD
        dp = ndp
    # Aggregate answers by LCS length (dp[N])
    ans = [0] * (N + 1)
    for idx, cnt in enumerate(dp):
        if cnt == 0:
            continue
        lcs_len = states[idx][N]
        ans[lcs_len] = (ans[lcs_len] + cnt) % MOD
    print(' '.join(str(x % MOD) for x in ans))

if __name__ == "__main__":
    solve()
