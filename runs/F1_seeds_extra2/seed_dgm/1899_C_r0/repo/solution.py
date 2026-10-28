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
        best = None
        cur = 0
        prev_par = -1
        for idx in range(n):
            x = int(a[idx])
            par = x & 1
            if idx == 0 or par == prev_par:
                cur = x
            else:
                cur = cur + x if cur > 0 else x
            # cur tracks best alternating subarray ending here
            if best is None or cur > best:
                best = cur
            prev_par = par
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
