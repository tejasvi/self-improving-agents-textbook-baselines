import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    strength = S[P * W + Q]
    visited = [False] * (H * W)
    start = P * W + Q
    visited[start] = True
    heap = []

    def push_neighbors(idx):
        r, c = divmod(idx, W)
        if r > 0 and not visited[idx - W]:
            visited[idx - W] = True
            heapq.heappush(heap, (S[idx - W], idx - W))
        if r < H - 1 and not visited[idx + W]:
            visited[idx + W] = True
            heapq.heappush(heap, (S[idx + W], idx + W))
        if c > 0 and not visited[idx - 1]:
            visited[idx - 1] = True
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if c < W - 1 and not visited[idx + 1]:
            visited[idx + 1] = True
            heapq.heappush(heap, (S[idx + 1], idx + 1))

    push_neighbors(start)
    while heap:
        s, idx = heap[0]
        if s * X < strength:
            heapq.heappop(heap)
            strength += s
            push_neighbors(idx)
        else:
            break
    print(strength)

main()
