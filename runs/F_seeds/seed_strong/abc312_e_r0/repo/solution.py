import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 6 * n]))
    boxes = []
    for i in range(n):
        b = vals[6 * i:6 * i + 6]
        boxes.append((b[0], b[1], b[2], b[3], b[4], b[5]))

    S = 101
    S2 = S * S
    SIZE = S * S2
    pairs = set()
    for k in range(3):
        # axis k is the plane normal; p, q are the other two axes
        p_ax = (k + 1) % 3
        q_ax = (k + 2) % 3
        minArr = [-1] * SIZE
        info = []
        for i, b in enumerate(boxes):
            lo = b[k]
            hi = b[k + 3]
            plo = b[p_ax]
            phi = b[p_ax + 3]
            qlo = b[q_ax]
            qhi = b[q_ax + 3]
            info.append((lo, hi, plo, phi, qlo, qhi))
            w = qhi - qlo
            filler = [i] * w
            lb = lo * S2
            for p in range(plo, phi):
                off = p * S + qlo
                minArr[lb + off: lb + off + w] = filler
        for i in range(n):
            lo, hi, plo, phi, qlo, qhi = info[i]
            hb = hi * S2
            for p in range(plo, phi):
                off = hb + p * S
                seg = minArr[off + qlo: off + qhi]
                for j in set(seg):
                    if j >= 0 and j != i:
                        a, c = (i, j) if i < j else (j, i)
                        pairs.add(a * n + c)
    deg = [0] * n
    for code in pairs:
        a, c = divmod(code, n)
        deg[a] += 1
        deg[c] += 1
    sys.stdout.write("\n".join(map(str, deg)) + "\n")


main()
