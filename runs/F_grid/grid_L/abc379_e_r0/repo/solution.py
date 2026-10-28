import sys

def main():
    try:
        sys.set_int_max_str_digits(0)
    except AttributeError:
        pass
    data = sys.stdin.read().split()
    n = int(data[0])
    s = data[1]
    c = [(ord(s[t]) - 48) * (t + 1) for t in range(n)]
    lin = sum(c)  # sum of d_i * i (1-indexed), equals sum of c_t

    # Q(l, r) = sum_{t in [l,r)} c_t * 10^(r-1-t)
    # Q(l, r) = Q(l, m) * 10^(r-m) + Q(m, r)
    def build(l, r):
        if r - l <= 32:
            q = 0
            for t in range(l, r):
                q = q * 10 + c[t]
            return q, r - l
        m = (l + r) // 2
        ql, _ = build(l, m)
        qr, lr = build(m, r)
        return ql * pow(10, r - m) + qr, r - l

    q, _ = build(0, n)
    V = q * 10  # term t has exponent N - t = (N-1-t) + 1
    ans = (V - lin) // 9
    sys.stdout.write(str(ans) + "\n")

main()
