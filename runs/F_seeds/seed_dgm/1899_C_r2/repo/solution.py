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
        a = list(map(int, a))
        # cur: best sum of a valid subarray ending at i
        cur = a[0]
        best = a[0]
        for i in range(1, n):
            x = a[i]
            if (x - a[i - 1]) & 1:  # parities differ: can extend
                cur = cur + x if cur + x > x else x
            else:
                cur = x
            if cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
