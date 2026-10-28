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
        # Keys are bytes; normalize to int for comparison
        c = {int(k): v for k, v in cnt.items()}
        # b_i^{b_j} == b_j^{b_i} <=> a_i / 2^{a_i} == a_j / 2^{a_j}
        # f(x) = x / 2^x is injective for x >= 2, f(1) = f(2) = 1/2
        total = 0
        for v in c.values():
            total += v * (v - 1) // 2
        total += c.get(1, 0) * c.get(2, 0)
        out.append(str(total))
    sys.stdout.write("\n".join(out) + "\n")


if __name__ == "__main__":
    main()
