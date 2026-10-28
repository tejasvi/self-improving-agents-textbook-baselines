import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    A = data[1:1 + n]
    B = data[1 + n:1 + 2 * n]
    C = [int(x) for x in data[1 + 2 * n:1 + 3 * n]]

    # Unique ranks (1..n) by (C, index) so that ties form a strict total order.
    order = sorted(range(n), key=lambda i: (C[i], i))
    rank = [0] * n
    for r, i in enumerate(order, 1):
        rank[i] = r

    off_cnt = [0] * (n + 1)   # Fenwick: count of "A=1,B=0" elements by rank
    off_sum = [0] * (n + 1)   # Fenwick: sum of C
    on_cnt = [0] * (n + 1)    # Fenwick: count of "A=0,B=1" elements by rank
    on_sum = [0] * (n + 1)

    def add(cnt, sm, pos, v):
        while pos <= n:
            cnt[pos] += 1
            sm[pos] += v
            pos += pos & -pos

    def prefix(cnt, sm, pos):
        c = 0
        s = 0
        while pos > 0:
            c += cnt[pos]
            s += sm[pos]
            pos -= pos & -pos
        return c, s

    W0 = 0          # total weight of A (initial)
    Wab = 0         # weight of positions with A=1,B=1
    stay = []       # (rank, C) of positions with A=1,B=1
    T_off = 0       # number of elements in off-set
    T_on = 0        # number of elements in on-set
    S_off_total = 0 # sum of C over off-set
    F_off = 0       # sum over off-set e of (sum of C over off-set elements with rank >= rank(e))
    F_on = 0        # sum over on-set e of (sum of C over on-set elements with rank <= rank(e))

    def insert_off(r, c):
        # returns increase of F_off when inserting element (r, c)
        nonlocal T_off, S_off_total, F_off
        cl, sl = prefix(off_cnt, off_sum, r)          # old elements with rank <= r
        delta = c * (cl + 1) + (S_off_total - sl)     # new element + old elements with rank > r
        F_off += delta
        T_off += 1
        S_off_total += c
        add(off_cnt, off_sum, r, c)

    def insert_on(r, c):
        nonlocal T_on, F_on
        _, sl = prefix(on_cnt, on_sum, r)             # old elements with rank <= r
        cl, _ = prefix(on_cnt, on_sum, r - 1)         # old elements with rank < r
        ge_old = T_on - cl                            # old elements with rank >= r
        F_on += c * (ge_old + 1) + sl                 # new element + old elements with rank < r
        T_on += 1
        add(on_cnt, on_sum, r, c)

    for i in range(n):
        a = A[i] == b'1'
        b = B[i] == b'1'
        c = C[i]
        r = rank[i]
        if a:
            W0 += c
        if a and not b:
            insert_off(r, c)
        elif b and not a:
            insert_on(r, c)
        elif a and b:
            stay.append((r, c))
            Wab += c

    def cost(T_o, F_o, T_n, F_n, base):
        # off phase: remove in decreasing rank; cur after each removal = W0 - removed
        # on phase: add in increasing rank; cur after each add = base + added
        return T_o * W0 - F_o + T_n * base + F_n

    # Stay-1 positions chosen to be toggled, taken in decreasing rank order.
    stay.sort(reverse=True)

    best = cost(T_off, F_off, T_on, F_on, Wab)
    base = Wab
    for r, c in stay:
        # Toggling this position off then on adds it to both phases.
        insert_off(r, c)
        insert_on(r, c)
        base -= c
        cur = cost(T_off, F_off, T_on, F_on, base)
        if cur < best:
            best = cur

    print(best)


if __name__ == "__main__":
    main()
