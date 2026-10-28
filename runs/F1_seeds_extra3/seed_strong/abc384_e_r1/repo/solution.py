import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [0] * (H * W)
    idx = 5
    for i in range(H * W):
        S[i] = int(data[idx]); idx += 1
    start = P * W + Q
    cur = S[start]
    visited = bytearray(H * W)
    visited[start] = 1
    heap = []

    def push_neighbors(c):
        r, col = divmod(c, W)
        if r > 0 and not visited[c - W]:
            visited[c - W] = 1
            heapq.heappush(heap, (S[c - W], c - W))
        if r < H - 1 and not visited[c + W]:
            visited[c + W] = 1
            heapq.heappush(heap, (S[c + W], c + W))
        if col > 0 and not visited[c - 1]:
            visited[c - 1] = 1
            heapq.heappush(heap, (S[c - 1], c - 1))
        if col < W - 1 and not visited[c + 1]:
            visited[c + 1] = 1
            heapq.heappush(heap, (S[c + 1], c + 1))

    push_neighbors(start)
    while heap:
        s, c = heap[0]
        if X * s < cur:
            heapq.heappop(heap)
            cur += s
            push_neighbors(c)
        else:
            break
    print(cur)

main()
