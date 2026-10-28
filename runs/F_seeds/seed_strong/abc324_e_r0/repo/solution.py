import sys

def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    T = data[1]
    S = data[2:2 + n]
    L = len(T)

    # a_i: longest prefix of T greedily matched as subsequence of S_i
    a = [0] * n
    for i, s in enumerate(S):
        p = 0
        for c in s:
            if p < L and T[p] == c:
                p += 1
                if p == L:
                    break
        a[i] = p

    # b_j: longest suffix of T greedily matched (from the right) in S_j
    cnt = [0] * (L + 2)
    for j, s in enumerate(S):
        q = L  # T[q:] matched so far
        for c in reversed(s):
            if q > 0 and T[q - 1] == c:
                q -= 1
                if q == 0:
                    break
        cnt[L - q] += 1

    # suf[v] = number of j with b_j >= v
    suf = [0] * (L + 2)
    run = 0
    for v in range(L, -1, -1):
        run += cnt[v]
        suf[v] = run

    ans = 0
    for i in range(n):
        ans += suf[L - a[i]]
    print(ans)

main()
