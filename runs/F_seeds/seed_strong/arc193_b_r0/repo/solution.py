import sys

MOD = 998244353


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1].strip()
    k = s.count('1')
    hi = n + k  # sum of rim in-degrees must lie in [n, n+k]
    sv = [1 if c == '1' else 0 for c in s]

    # Backtracking over rim in-degrees d_0..d_{n-1}, d_i in [0, 2+s_i].
    # Arc constraint: for each arc starting at i of length L (1..n-1), the sum
    # over the arc lies in [L-1, L+1+s(arc)]. Checked incrementally on the
    # prefix for arcs starting at 0 and wrap-around checked at the end.
    # Prefix-sum check for arcs [0, j] only is incomplete; full check at leaf.
    count = 0
    d = [0] * n

    def valid_full(dv):
        for i in range(n):
            tot = 0
            sc = 0
            for L in range(1, n):
                j = (i + L - 1) % n
                tot += dv[j]
                sc += sv[j]
                if tot < L - 1 or tot > L + 1 + sc:
                    return False
        return True

    def rec(pos, total):
        nonlocal count
        if pos == n:
            if n <= total <= hi and valid_full(d):
                count += 1
            return
        for v in range(0, 3 + sv[pos]):
            if total + v > hi:
                break
            d[pos] = v
            rec(pos + 1, total + v)
        d[pos] = 0

    rec(0, 0)
    print(count % MOD)


main()
