import sys


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    vals = list(map(int, data[1:1 + 6 * n]))
    boxes = []
    for i in range(n):
        b = vals[6 * i:6 * i + 6]
        boxes.append((b[0], b[1], b[2], b[3], b[4], b[5]))
    ans = [0] * n
    M = 101
    for k in range(3):
        p_ax = (k + 1) % 3
        q_ax = (k + 2) % 3
        lo = [[] for _ in range(M)]
        hi = [[] for _ in range(M)]
        for i, b in enumerate(boxes):
            lo[b[k]].append(i)
            hi[b[k + 3]].append(i)
        for c in range(M):
            if not lo[c] or not hi[c]:
                continue
            Glo = [[-1] * 100 for _ in range(100)]
            Ghi = [[-1] * 100 for _ in range(100)]
            for G, group in ((Glo, lo[c]), (Ghi, hi[c])):
                for i in group:
                    b = boxes[i]
                    p1, p2 = b[p_ax], b[p_ax + 3]
                    q1, q2 = b[q_ax], b[q_ax + 3]
                    seg = [i] * (q2 - q1)
                    for p in range(p1, p2):
                        G[p][q1:q2] = seg
            # boxes whose min face is on plane c query boxes whose max face is on c
            for j in lo[c]:
                b = boxes[j]
                s = set()
                q1, q2 = b[q_ax], b[q_ax + 3]
                for p in range(b[p_ax], b[p_ax + 3]):
                    s.update(Ghi[p][q1:q2])
                s.discard(-1)
                ans[j] += len(s)
            for i in hi[c]:
                b = boxes[i]
                s = set()
                q1, q2 = b[q_ax], b[q_ax + 3]
                for p in range(b[p_ax], b[p_ax + 3]):
                    s.update(Glo[p][q1:q2])
                s.discard(-1)
                ans[i] += len(s)
    sys.stdout.write("\n".join(map(str, ans)) + "\n")


main()
