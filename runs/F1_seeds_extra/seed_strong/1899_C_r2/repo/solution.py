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
        cur = 0
        best = None
        prev_par = -1
        for tok in a:
            x = int(tok)
            par = x & 1
            if best is None:
                cur = x
            elif par != prev_par and cur > 0:
                cur += x
            else:
                cur = x
            prev_par = par
            if best is None or cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
