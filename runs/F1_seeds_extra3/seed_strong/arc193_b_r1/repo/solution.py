import sys
MOD = 998244353
def solve_dp(N, s):
    k = s.count('1')
    total = 0
    for T in range(0, k+1):
        # state: (P, maxP, minP, Q, maxQ, minQ) with P0=0, Q0=0
        cur = {(0, 0, 0, 0, 0, 0): 1}
        for i in range(N):
            si = 1 if s[i] == '1' else 0
            nxt = {}
            for (P, mxP, mnP, Q, mxQ, mnQ), c in cur.items():
                for z in range(-1, 2 + si):
                    P2 = P + z; Q2 = Q + z - si
                    mxP2 = max(mxP, P2); mnP2 = min(mnP, P2)
                    mxQ2 = max(mxQ, Q2); mnQ2 = min(mnQ, Q2)
                    # pairwise constraints: maxP-P<=1, P-minP<=T+1, Q-minQ<=1, maxQ-Q<=k+1-T
                    if mxP2 - P2 > 1 or P2 - mnP2 > T + 1: continue
                    if Q2 - mnQ2 > 1 or mxQ2 - Q2 > k + 1 - T: continue
                    key = (P2, mxP2, mnP2, Q2, mxQ2, mnQ2)
                    nxt[key] = (nxt.get(key, 0) + c)
            cur = nxt
        for (P, mxP, mnP, Q, mxQ, mnQ), c in cur.items():
            if P == T:
                total += c
    return total % MOD
if __name__ == "__main__":
    data = sys.stdin.read().split()
    print(solve_dp(int(data[0]), data[1]))
