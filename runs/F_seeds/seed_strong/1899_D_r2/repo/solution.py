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
        # Equal exponents always work; the only cross pair is {1, 2}
        # since f(x) = x / 2^x takes equal values only at x=1 and x=2.
        ans = 0
        for c in cnt.values():
            ans += c * (c - 1) // 2
        ans += cnt.get(b"1", 0) * cnt.get(b"2", 0)
        out.append(str(ans))
    sys.stdout.write("\n".join(out) + "\n")

main()
