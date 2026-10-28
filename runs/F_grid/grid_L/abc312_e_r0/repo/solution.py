import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cubes = []
    idx = 1
    for _ in range(n):
        vals = [int(x) for x in data[idx:idx + 6]]
        idx += 6
        cubes.append(vals)  # x1,y1,z1,x2,y2,z2

    S = 101
    pairs = set()
    for a in range(3):
        b, c = [t for t in range(3) if t != a]
        bi, ci, ai = b, c, a
        # per plane v: left-owner (cuboid whose max along a == v), right-owner (min == v)
        left = [[0] * (S * S) for _ in range(S)]
        right = [[0] * (S * S) for _ in range(S)]
        for k, cb in enumerate(cubes, 1):
            lo_a, hi_a = cb[a], cb[a + 3]
            b1, b2 = cb[b], cb[b + 3]
            c1, c2 = cb[c], cb[c + 3]
            length = c2 - c1
            filler = [k] * length
            # max face at plane hi_a
            L = left[hi_a]
            for p in range(b1, b2):
                base = p * S + c1
                L[base:base + length] = filler
            R = right[lo_a]
            for p in range(b1, b2):
                base = p * S + c1
                R[base:base + length] = filler
        for v in range(S):
            L = left[v]
            R = right[v]
            for cell in range(S * S):
                i = L[cell]
                if i:
                    j = R[cell]
                    if j:
                        if i < j:
                            pairs.add((i, j))
                        elif j < i:
                            pairs.add((j, i))
    cnt = [0] * (n + 1)
    for i, j in pairs:
        cnt[i] += 1
        cnt[j] += 1
    sys.stdout.write("\n".join(str(cnt[i]) for i in range(1, n + 1)) + "\n")


main()
