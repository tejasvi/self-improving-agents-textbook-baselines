import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    S = 101
    S2 = S * S
    S3 = S2 * S
    pairs = set()
    vals = list(map(int, data[1:1 + 6 * n]))
    for k in range(3):
        P = [0] * S3  # id of cuboid whose max face on axis k lies in this cell's plane
        M = [0] * S3  # id of cuboid whose min face lies in this cell's plane
        # axis k contributes stride; other two axes u<v
        # index = x*S2 + y*S + z ; plane coordinate on axis k
        o = [d for d in range(3) if d != k]
        su = S2 if o[0] == 0 else (S if o[0] == 1 else 1)
        sv = S2 if o[1] == 0 else (S if o[1] == 1 else 1)
        sk = S2 if k == 0 else (S if k == 1 else 1)
        for c in range(n):
            b = 6 * c
            lo = vals[b:b + 3]
            hi = vals[b + 3:b + 6]
            cid = c + 1
            lu, lv = lo[o[0]], lo[o[1]]
            hu, hv = hi[o[0]], hi[o[1]]
            w = hv - lv
            row = [cid] * w
            for arr, plane in ((P, hi[k]), (M, lo[k])):
                base = plane * sk
                for u in range(lu, hu):
                    st = base + u * su + lv * sv
                    arr[st:st + (w - 1) * sv + 1:sv] = row
        for p, m in zip(P, M):
            if p and m:
                if p < m:
                    pairs.add((p, m))
                else:
                    pairs.add((m, p))
    deg = [0] * (n + 1)
    for a, b in pairs:
        deg[a] += 1
        deg[b] += 1
    sys.stdout.write("\n".join(str(x) for x in deg[1:]) + "\n")

main()
