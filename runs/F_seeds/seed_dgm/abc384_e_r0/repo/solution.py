import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]

    visited = [False] * (H * W)
    start = P * W + Q
    visited[start] = True
    T = S[start]
    heap = []

    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not visited[idx - W]:
            visited[idx - W] = True
            heapq.heappush(heap, (S[idx - W], idx - W))
        if i < H - 1 and not visited[idx + W]:
            visited[idx + W] = True
            heapq.heappush(heap, (S[idx + W], idx + W))
        if j > 0 and not visited[idx - 1]:
            visited[idx - 1] = True
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if j < W - 1 and not visited[idx + 1]:
            visited[idx + 1] = True
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if s * X < T:
            heapq.heappop(heap)
            T += s
            push_neighbors(idx)
        else:
            break

    print(T)


main()
