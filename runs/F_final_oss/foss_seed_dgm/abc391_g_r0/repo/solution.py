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
    # Precompute all possible states (dp columns). Since N <= 10, we can generate on the fly.
    zero_state = tuple([0]*(N+1))
    # Precompute transitions for each state and each character (0-25)
    from collections import defaultdict
    # We'll build transition dict lazily as states appear.
    transitions = {}
    def get_transition(state, ch):
        # ch is a character (string of length 1)
        key = (state, ch)
        if key in transitions:
            return transitions[key]
        dp = state
        new = [0]*(N+1)
        for i in range(1, N+1):
            if S[i-1] == ch:
                new[i] = dp[i-1] + 1
            else:
                a = dp[i]
                b = new[i-1]
                new[i] = a if a >= b else b
        new_state = tuple(new)
        transitions[key] = new_state
        return new_state

    cur = defaultdict(int)
    cur[zero_state] = 1
    letters = [chr(ord('a') + i) for i in range(26)]
    for _ in range(M):
        nxt = defaultdict(int)
        for state, cnt in cur.items():
            for ch in letters:
                ns = get_transition(state, ch)
                nxt[ns] = (nxt[ns] + cnt) % MOD
        cur = nxt
    # Aggregate answers by LCS length k = state[N]
    ans = [0]*(N+1)
    for state, cnt in cur.items():
        k = state[N]
        ans[k] = (ans[k] + cnt) % MOD
    print(' '.join(str(x) for x in ans))

if __name__ == "__main__":
    solve()
