import sys


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    K = 500000  # only starting values X <= K matter for queries
    size = K + 1  # Fenwick indices 1..K+1
    tree = [0] * (size + 1)
    LOG = 1
    while (1 << LOG) <= size:
        LOG += 1

    def add(i, v):
        while i <= size:
            tree[i] += v
            i += i & (-i)

    def prefix(i):
        s = 0
        while i > 0:
            s += tree[i]
            i -= i & (-i)
        return s

    # h(X) = X + sum_{j<=X} d[j]; initially d == 0 (h(X) = X).
    for _ in range(n):
        L = int(data[idx]); R = int(data[idx + 1]); idx += 2
        # a = smallest X in [1..K] with h(X) >= L  -> largest pos with h(pos) < L, plus 1
        pos = 0
        acc = 0
        step = 1 << (LOG - 1)
        while step:
            np_ = pos + step
            if np_ <= K:
                t = acc + tree[np_]
                if np_ + t < L:
                    pos = np_
                    acc = t
            step >>= 1
        a = pos + 1
        # b = largest X with h(X) <= R
        pos = 0
        acc = 0
        step = 1 << (LOG - 1)
        while step:
            np_ = pos + step
            if np_ <= K:
                t = acc + tree[np_]
                if np_ + t <= R:
                    pos = np_
                    acc = t
            step >>= 1
        b = pos
        if a <= b:
            add(a, 1)
            add(b + 1, -1)

    q = int(data[idx]); idx += 1
    out = []
    for _ in range(q):
        x = int(data[idx]); idx += 1
        out.append(x + prefix(x))
    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
