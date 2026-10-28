import sys
from collections import Counter

def main():
    data = sys.stdin.buffer.read().split()
    t = int(data[0])
    pos = 1
    out = []
    for _ in range(t):
        n = int(data[pos]); pos += 1
        cnt = Counter(data[pos:pos + n]); pos += n
        # Keys are bytes; normalize via int to handle e.g. leading zeros (not expected)
        c = {}
        for k, v in cnt.items():
            c[int(k)] = c.get(int(k), 0) + v
        ans = 0
        for v in c.values():
            ans += v * (v - 1) // 2
        # f(x) = x / 2^x is equal only for x=1 and x=2 (among positive integers)
        ans += c.get(1, 0) * c.get(2, 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

main()
