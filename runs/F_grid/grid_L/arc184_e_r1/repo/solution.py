import sys

MOD = 998244353


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    m = int(data[1])
    s = b"".join(data[2:2 + n * m])

    # Each nonzero row a(z) = z^v * u(z), u(0)=1, L = m - v.
    # Orbit under the operation: z^v * u * (1+z)^{-x} mod z^L.
    # Reduce u = r * t^{-x_s} with canonical r (t = 1+z, order p = 2^K, K = ceil(log2 L)).
    # Then f(a,b) = (y_a - y_b) mod p where y = (-x) mod p, for groups keyed by (L, r).
    groups = {}
    gbase = []   # offset into flat Fenwick array
    gp = []      # modulus p (power of two) for group
    gcnt = []
    gsum = []
    fen_total = 0
    rows = []    # (group id, y)

    for i in range(n):
        seg = s[i * m:(i + 1) * m]
        full = int(seg[::-1], 2)
        if full == 0:
            continue
        v = (full & -full).bit_length() - 1
        L = m - v
        cur = full >> v
        mask = (1 << L) - 1
        K = (L - 1).bit_length()
        x = 0
        for k in range(K):
            sh = 1 << k
            if (cur >> sh) & 1:
                cur ^= (cur << sh) & mask
                x += sh
        key = (L, cur)
        g = groups.get(key)
        if g is None:
            g = len(gp)
            groups[key] = g
            p = 1 << K
            gbase.append(fen_total)
            gp.append(p)
            gcnt.append(0)
            gsum.append(0)
            fen_total += p + 1
        rows.append((g, (-x) % gp[g]))

    # Fenwick tree (1-indexed per group) over flat array.
    fen = [0] * (fen_total + 1)
    total = 0  # exact integer accumulation
    for g, y in rows:
        p = gp[g]
        base = gbase[g]
        # count earlier values < y in this group: prefix query over indices 1..y
        less = 0
        idx = y
        while idx > 0:
            less += fen[base + idx]
            idx &= idx - 1
        # linear part: sum over earlier a of (y_a - y)
        total += gsum[g] - gcnt[g] * y
        # wrap part: + p for each earlier a with y_a < y
        total += p * less
        gcnt[g] += 1
        gsum[g] += y
        # update index y+1 within group size p
        idx = y + 1
        while idx <= p:
            fen[base + idx] += 1
            idx += idx & (-idx)

    print(total % MOD)


main()
