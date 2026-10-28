import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [0] * (H * W)
    idx = 5
    for k in range(H * W):
        S[k] = int(data[idx + k])
    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    cur = S[start]
    heap = []

    def push_neighbors(c):
        i, j = divmod(c, W)
        if i > 0 and not visited[c - W]:
            heapq.heappush(heap, (S[c - W], c - W))
        if i < H - 1 and not visited[c + W]:
            heapq.heappush(heap, (S[c + W], c + W))
        if j > 0 and not visited[c - 1]:
            heapq.heappush(heap, (S[c - 1], c - 1))
        if j < W - 1 and not visited[c + 1]:
            heapq.heappush(heap, (S[c + 1], c + 1))

    push_neighbors(start)
    while heap:
        s, c = heapq.heappop(heap)
        if visited[c]:
            continue
        if X * s >= cur:
            break
        visited[c] = 1
        cur += s
        push_neighbors(c)
    print(cur)


main()
