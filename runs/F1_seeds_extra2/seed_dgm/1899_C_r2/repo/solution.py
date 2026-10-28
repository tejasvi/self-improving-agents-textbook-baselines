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
        prev = None
        prev_par = None
        for x in a:
            v = int(x)
            par = v & 1
            if prev is None or prev_par == par:
                cur = v
            else:
                cur = prev + v if prev > 0 else v
            if best is None or cur > best:
                best = cur
            prev = cur
            prev_par = par
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
