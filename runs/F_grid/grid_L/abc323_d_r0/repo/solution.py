import sys
from collections import defaultdict


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    groups = defaultdict(list)  # odd part -> list of (exponent, count)
    for i in range(n):
        s = int(data[1 + 2 * i])
        c = int(data[2 + 2 * i])
        k = 0
        while s % 2 == 0:
            s //= 2
            k += 1
        groups[s].append((k, c))

    answer = 0
    for m, items in groups.items():
        items.sort()
        cur_exp = None
        cnt = 0
        for k, c in items:
            if cur_exp is not None:
                gap = k - cur_exp
                # move carry from cur_exp up to k
                while gap > 0 and cnt > 0:
                    answer += cnt & 1
                    cnt >>= 1
                    gap -= 1
            cur_exp = k
            cnt += c
        # finalize remaining carry at the last level
        while cnt > 0:
            answer += cnt & 1
            cnt >>= 1
    print(answer)


main()
