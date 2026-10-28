import sys


def main():
    data = sys.stdin.read().split()
    n, m, a, b = int(data[0]), int(data[1]), int(data[2]), int(data[3])
    segs = []
    idx = 4
    for _ in range(m):
        segs.append((int(data[idx]), int(data[idx + 1])))
        idx += 2
    segs.sort()

    mask = (1 << b) - 1
    # bits k in [a-1, b-1] are the window offsets for positions p+1-i, i in [a, b]
    sel = 0
    for k in range(a - 1, b):
        sel |= 1 << k

    def step(w):
        # one step to a good square
        new = 1 if (w & sel) else 0
        return ((w << 1) | new) & mask

    # images of basis vectors under one good step
    img0 = [step(1 << k) for k in range(b)]

    def apply(img, w):
        r = 0
        k = 0
        while w:
            if w & 1:
                r |= img[k]
            w >>= 1
            k += 1
        return r

    LOG = max(1, n.bit_length() + 1)
    pows = [img0]
    for _ in range(1, LOG):
        prev = pows[-1]
        pows.append([apply(prev, prev[k]) for k in range(b)])

    def advance(w, d):
        j = 0
        while d and w:
            if d & 1:
                w = apply(pows[j], w)
            d >>= 1
            j += 1
        return w

    w = 1  # window of square 1: bit0 = reachable(p), p = 1
    p = 1
    for L, R in segs:
        w = advance(w, (L - 1) - p)
        p = L - 1
        length = R - L + 1
        w = (w << length) & mask
        p = R
        if w == 0:
            print("No")
            return
    w = advance(w, n - p)
    print("Yes" if (w & 1) else "No")


main()
