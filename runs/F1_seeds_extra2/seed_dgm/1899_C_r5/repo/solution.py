import sys


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        pos += 1
        a = data[pos:pos + n]
        pos += n
        # cur: best sum of alternating-parity subarray ending at current index
        cur = int(a[0])
        best = cur
        prev_par = int(a[0]) & 1
        for i in range(1, n):
            x = int(a[i])
            p = x & 1
            if p != prev_par:
                cand = cur + x
                cur = cand if cand > x else x
            else:
                cur = x
            prev_par = p
            if cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
