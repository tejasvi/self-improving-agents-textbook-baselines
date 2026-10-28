import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    cnt = {}
    for i in range(n):
        s = int(data[1 + 2 * i])
        c = int(data[2 + 2 * i])
        cnt[s] = cnt.get(s, 0) + c
    heap = list(cnt.keys())
    heapq.heapify(heap)
    ans = 0
    while heap:
        x = heapq.heappop(heap)
        c = cnt.pop(x)
        ans += c & 1
        half = c >> 1
        if half:
            y = x * 2
            if y in cnt:
                cnt[y] += half
            else:
                cnt[y] = half
                heapq.heappush(heap, y)
    print(ans)


main()
