# Solution for "Many LCS" problem.
# We compute the number of length‑M strings over the 26 lowercase letters whose
# longest common subsequence with a given string S (|S| = N, N ≤ 10) has length exactly k.
# The answer for each k = 0..N is required modulo MOD = 998244353.

import sys
from collections import deque, defaultdict

MOD = 998244353

def solve() -> None:
    data = sys.stdin.read().strip().split()
    if not data:
        return
    N = int(data[0])
    M = int(data[1])
    S = data[2]

    # ---------- Helper: transition of LCS DP vector ----------
    # For a processed prefix T of the unknown string, we keep a vector dp[0..N]
    # where dp[i] = LCS length between T and S[:i].
    # When we add a new character c, the new vector ndp can be computed in O(N)
    # using the classic DP recurrence.
    def next_state(state, ch):
        prev = state
        ndp = [0] * (N + 1)
        # ndp[0] stays 0
        for i in range(1, N + 1):
            if S[i - 1] == ch:
                ndp[i] = prev[i - 1] + 1
            else:
                a = prev[i]
                b = ndp[i - 1]
                ndp[i] = a if a >= b else b
        return tuple(ndp)

    # ---------- Build the automaton (all reachable states) ----------
    start = tuple([0] * (N + 1))
    # BFS to discover all states reachable by any sequence of characters.
    state_list = []          # index -> state tuple
    index_of = {}            # state tuple -> index
    trans = []               # for each state index, list of 26 next state indices

    q = deque()
    q.append(start)
    index_of[start] = 0
    state_list.append(start)
    trans.append([0] * 26)  # placeholder

    while q:
        cur = q.popleft()
        cur_idx = index_of[cur]
        cur_trans = []
        for code in range(26):
            ch = chr(ord('a') + code)
            nxt = next_state(cur, ch)
            if nxt not in index_of:
                idx = len(state_list)
                index_of[nxt] = idx
                state_list.append(nxt)
                trans.append([0] * 26)  # placeholder for future expansions
                q.append(nxt)
            cur_trans.append(index_of[nxt])
        trans[cur_idx] = cur_trans

    S_cnt = len(state_list)
    # ---------- Dynamic programming over length M ----------
    # dp[i] = number of strings leading to state i after processing some prefix.
    dp = [0] * S_cnt
    dp[0] = 1  # start state
    for _ in range(M):
        ndp = [0] * S_cnt
        for idx, cnt in enumerate(dp):
            if cnt == 0:
                continue
            nxts = trans[idx]
            # unroll the 26 additions
            for nxt_idx in nxts:
                ndp[nxt_idx] = (ndp[nxt_idx] + cnt) % MOD
        dp = ndp

    # ---------- Collect answers ----------
    ans = [0] * (N + 1)
    for idx, cnt in enumerate(dp):
        if cnt:
            lcs_len = state_list[idx][N]
            ans[lcs_len] = (ans[lcs_len] + cnt) % MOD
    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()
