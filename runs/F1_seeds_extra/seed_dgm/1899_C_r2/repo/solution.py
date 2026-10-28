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
        prev_par = 0
        for i in range(n):
            x = int(a[i])
            par = x & 1
            if i == 0 or par == prev_par:
                cur = x
            else:
                cur = cur + x if cur > 0 else x
            # cur is max sum of alternating subarray ending at i
            # (extend only if previous ending sum is positive, else restart)
            prev_par = par
            if best is None or cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
