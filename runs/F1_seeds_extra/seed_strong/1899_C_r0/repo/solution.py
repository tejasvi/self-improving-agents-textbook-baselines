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
        for tok in a:
            x = int(tok)
            p = x & 1
            if best is None:
                cur = x
            elif p != prev_par:
                cur = cur + x if cur > 0 else x
            else:
                cur = x
            prev_par = p
            if best is None or cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
