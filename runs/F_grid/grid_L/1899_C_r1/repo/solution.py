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
        NEG = float("-inf")
        best = NEG
        cur = NEG
        prev_par = -1
        for x in a:
            v = int(x)
            par = v & 1
            if cur != NEG and par != prev_par:
                cur = cur + v if cur > 0 else v
            else:
                cur = v
            prev_par = par
            if cur > best:
                best = cur
        out.append(str(best))
    sys.stdout.write("\n".join(out) + "\n")


main()
