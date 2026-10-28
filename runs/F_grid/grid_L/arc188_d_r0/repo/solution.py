import sys

def main():
    data = sys.stdin.read().split()
    MOD = 998244353
    n = int(data[0])
    A = [int(v) for v in data[1:1 + n]]
    B = [int(v) for v in data[1 + n:1 + 2 * n]]

    # blocks of A must be distinct and cover 1..n
    blk = [(v + 1) // 2 for v in A]
    if len(set(blk)) != n:
        print(0)
        return
    # x_i = blk[i]; u for block v: index i with blk[i] == v
    idx_of_block = [0] * (n + 1)
    for i in range(n):
        idx_of_block[blk[i]] = i
    odd = [A[i] % 2 == 1 for i in range(n)]

    nxt = [-1] * n
    prv = [-1] * n
    for j in range(n):
        if B[j] != -1:
            f = (B[j] + 1) // 2
            u = idx_of_block[f]
            nxt[u] = j
            prv[j] = u

    visited = [False] * n
    a = b = c = 0  # a: only odd, b: only even, c: both
    for s in range(n):
        if prv[s] != -1:
            continue
        has_o = has_e = False
        cur = s
        while cur != -1:
            visited[cur] = True
            if odd[cur]:
                has_o = True
            else:
                has_e = True
            cur = nxt[cur]
        if has_o and has_e:
            c += 1
        elif has_o:
            a += 1
        else:
            b += 1
    for s in range(n):
        if visited[s]:
            continue
        has_o = has_e = False
        cur = s
        while not visited[cur]:
            visited[cur] = True
            if odd[cur]:
                has_o = True
            else:
                has_e = True
            cur = nxt[cur]
        if not (has_o and has_e):
            print(0)
            return

    m = a + b + c
    fact = [1] * (m + 1)
    for i in range(1, m + 1):
        fact[i] = fact[i - 1] * i % MOD

    def comb(p, q):
        if q < 0 or q > p:
            return 0
        return 1 if q == 0 else p  # only q in {0,1} is used

    ans = 0
    for s in range(2):
        for t in range(2):
            if m - s - t < 0:
                continue
            term = comb(b, s) * comb(a, t) % MOD * fact[m - s - t] % MOD
            if (s + t) % 2:
                ans -= term
            else:
                ans += term
    print(ans % MOD)

main()
