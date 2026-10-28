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
        cur = None
        prev_parity = -1
        for tok in a:
            x = int(tok)
            p = x & 1
            if cur is None or p == prev_parity:
                cur = x
            else:
                cur = cur + x if cur > 0 else x
            prev_parity = p
            if best is None or cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
