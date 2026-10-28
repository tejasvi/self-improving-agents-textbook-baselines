import sys
from collections import Counter


def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos])
        pos += 1
        cnt = Counter(data[pos:pos + n])
        pos += n
        # Equal values always work; the only extra pair is {1, 2},
        # since x / 2^x is equal for x = 1 and x = 2.
        total = 0
        for v in cnt.values():
            total += v * (v - 1) // 2
        c1 = cnt.get(b"1", 0)
        c2 = cnt.get(b"2", 0)
        total += c1 * c2
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
