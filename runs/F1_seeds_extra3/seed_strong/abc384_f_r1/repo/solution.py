import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = list(map(int, data[1:1 + n]))
    T = 25  # 2*max(A) < 2^25, so S_t = 0 for t >= 25
    # S_t = sum over unordered pairs i<=j with 2^t | (A_i+A_j) of (A_i+A_j)
    S = [0] * (T + 1)
    for t in range(T):
        mask = (1 << t) - 1
        cnt = {}
        sm = {}
        for a in A:
            r = a & mask
            if r in cnt:
                cnt[r] += 1
                sm[r] += a
            else:
                cnt[r] = 1
                sm[r] = a
        acc = 0  # sum over ordered pairs (i,j), including i==j, with cond of A_i
        for r, s in sm.items():
            cp = cnt.get((-r) & mask)
            if cp:
                acc += s * cp
        # diagonal correction: i==j pairs contribute 2A_i in S, acc gave A_i
        if t == 0:
            diag = sum(A)
        else:
            m2 = (1 << (t - 1)) - 1
            diag = 0
            for a in A:
                if a & m2 == 0:
                    diag += a
        S[t] = acc + diag
    ans = 0
    for t in range(T):
        ans += (S[t] - S[t + 1]) >> t
    print(ans)

main()
