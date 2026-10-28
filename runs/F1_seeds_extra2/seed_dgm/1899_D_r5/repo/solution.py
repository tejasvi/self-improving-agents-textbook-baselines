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
        # b_i^{b_j} == b_j^{b_i}  <=>  a_i / 2^{a_i} == a_j / 2^{a_j}
        # Equal a always works; the only distinct pair with equal value is (1, 2).
        total = 0
        for c in cnt.values():
            total += c * (c - 1) // 2
        ones = cnt.get(b"1", 0)
        twos = cnt.get(b"2", 0)
        total += ones * twos
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
