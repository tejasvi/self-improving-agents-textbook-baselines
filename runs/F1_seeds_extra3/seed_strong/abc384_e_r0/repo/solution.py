import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = data[5:5 + H * W]
    S = [int(v) for v in S]
    visited = bytearray(H * W)
    start = P * W + Q
    cur = S[start]
    visited[start] = 1
    heap = []
    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not visited[idx - W]:
            heapq.heappush(heap, (S[idx - W], idx - W))
        if i < H - 1 and not visited[idx + W]:
            heapq.heappush(heap, (S[idx + W], idx + W))
        if j > 0 and not visited[idx - 1]:
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if j < W - 1 and not visited[idx + 1]:
            heapq.heappush(heap, (S[idx + 1], idx + 1))
    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if visited[idx]:
            heapq.heappop(heap)
            continue
        if X * s < cur:
            heapq.heappop(heap)
            visited[idx] = 1
            cur += s
            push_neighbors(idx)
        else:
            break
    print(cur)

main()
