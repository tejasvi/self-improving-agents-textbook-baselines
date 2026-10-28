import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    start = P * W + Q
    cur = S[start]
    visited = bytearray(H * W)
    visited[start] = 1
    heap = []

    def push_neighbors(idx):
        r, c = divmod(idx, W)
        if r > 0 and not visited[idx - W]:
            heapq.heappush(heap, (S[idx - W], idx - W))
        if r < H - 1 and not visited[idx + W]:
            heapq.heappush(heap, (S[idx + W], idx + W))
        if c > 0 and not visited[idx - 1]:
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if c < W - 1 and not visited[idx + 1]:
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heapq.heappop(heap)
        if visited[idx]:
            continue
        if X * s >= cur:
            break
        visited[idx] = 1
        cur += s
        push_neighbors(idx)
    print(cur)


main()
