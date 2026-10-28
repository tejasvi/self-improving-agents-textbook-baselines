import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    M = 500000  # starting values range over 1..M
    tree = [0] * (M + 2)
    LOG = 1
    while LOG * 2 <= M:
        LOG *= 2

    def add(i, v):
        while i <= M:
            tree[i] += v
            i += i & (-i)

    def last_below(bound):
        # largest p in [0, M] with p + prefix(p) < bound (A is monotone)
        pos = 0
        s = 0
        step = LOG
        while step:
            np_ = pos + step
            if np_ <= M:
                t = s + tree[np_]
                if np_ + t < bound:
                    pos = np_
                    s = t
            step >>= 1
        return pos

    for _ in range(n):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        # a = first x with A[x] >= L ; b = last x with A[x] <= R
        a = last_below(L) + 1
        b = last_below(R + 1)
        if a <= b:
            add(a, 1)
            if b + 1 <= M:
                add(b + 1, -1)

    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        x = int(data[idx]); idx += 1
        s = 0
        i = x
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        out.append(x + s)
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
