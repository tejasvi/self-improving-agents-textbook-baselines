import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    k = int(data[1])
    s = data[2]
    # Class of parity vector modulo (1,1,1): A->01, B->10, C->11 (A^B == C in quotient)
    code = {'A': 1, 'B': 2, 'C': 3}
    dp = {(0, (1, 0, 0, 0)): 1}
    for ch in s:
        letters = 'ABC' if ch == '?' else ch
        ndp = {}
        for (q, cnt), v in dp.items():
            for L in letters:
                nq = q ^ code[L]
                c = list(cnt)
                c[nq] += 1
                key = (nq, tuple(c))
                ndp[key] = (ndp.get(key, 0) + v) % MOD
        dp = ndp
    ans = 0
    for (q, cnt), v in dp.items():
        good = 0
        for x in cnt:
            good += x * (x - 1) // 2
        if good >= k:
            ans = (ans + v) % MOD
    print(ans)


main()
