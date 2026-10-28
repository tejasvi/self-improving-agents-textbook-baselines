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
        # Keys are byte strings; normalise to int for the 1/2 special case.
        ones = 0
        twos = 0
        total = 0
        for k, c in cnt.items():
            v = int(k)
            total += c * (c - 1) // 2
            if v == 1:
                ones = c
            elif v == 2:
                twos = c
        # x/2^x equal for x=1 and x=2 only (among equal-valued pairs otherwise)
        total += ones * twos
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
