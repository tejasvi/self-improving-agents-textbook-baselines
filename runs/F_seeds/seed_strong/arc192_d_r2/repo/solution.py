import sys

MOD = 998244353


def prime_factors(A):
    primes = set()
    for a in A:
        x = a
        d = 2
        while d * d <= x:
            if x % d == 0:
                primes.add(d)
                while x % d == 0:
                    x //= d
            d += 1
        if x > 1:
            primes.add(x)
    return sorted(primes)


def solve_prime(p, ex):
    # Sum over sequences e_0..e_{N-1} >= 0 with min e = 0, |e_i - e_{i+1}| = ex[i],
    # of p^{sum e_i}. Decompose by k = first index with e_k = 0.
    N = len(ex) + 1
    S = sum(ex)
    pw = [1] * (S + 1)
    for k in range(1, S + 1):
        pw[k] = pw[k - 1] * p % MOD

    def combine(dp, a):
        # out[w] = dp[w+a] + dp[w-a] (a>0), then multiplied by pw[w]
        if a == 0:
            return [x * y % MOD for x, y in zip(dp, pw)]
        if a > S:
            return [0] * (S + 1)
        up = dp[a:] + [0] * a
        down = [0] * a + dp[:S + 1 - a]
        return [(u + d) * q % MOD for u, d, q in zip(up, down, pw)]

    # Right DP: Rv_j[v] = p^v * sum_{|w-v|=ex[j]} Rv_{j+1}[w]; Rv_{N-1}[v] = p^v.
    # Needed scalars: Rval[k] = Rv_{k+1}[ex[k]] for k < N-1, and 1 for k = N-1.
    Rval = [1] * N
    cur = pw[:]  # Rv_{N-1}
    for j in range(N - 2, -1, -1):
        # cur is Rv_{j+1}
        Rval[j] = cur[ex[j]]
        if j > 0:
            cur = combine(cur, ex[j])

    # Left DP: Lv_j[v] for v>=1 with all e_i >= 1 for i<=j, weight p^{v} and e_j=v.
    # Lv_0[v] = p^v for v>=1, 0 at v=0. Lval[k] = Lv_{k-1}[ex[k-1]] (k>=1), 1 for k=0.
    total = 0
    cur = pw[:]
    cur[0] = 0  # Lv_0
    for k in range(N):
        if k == 0:
            Lval = 1
        else:
            Lval = cur[ex[k - 1]]
        total = (total + Lval * Rval[k]) % MOD
        if 1 <= k < N - 1:
            # cur = L_{k-1} -> L_k via ex[k-1]; e_k >= 1 required
            nxt = combine(cur, ex[k - 1])
            nxt[0] = 0
            cur = nxt
    return total


def solve(N, A):
    ans = 1
    for p in prime_factors(A):
        ex = []
        for a in A:
            e = 0
            x = a
            while x % p == 0:
                x //= p
                e += 1
            ex.append(e)
        ans = ans * solve_prime(p, ex) % MOD
    return ans


def main():
    data = sys.stdin.read().split()
    N = int(data[0])
    A = [int(x) for x in data[1:N]]
    print(solve(N, A))


if __name__ == "__main__":
    main()
