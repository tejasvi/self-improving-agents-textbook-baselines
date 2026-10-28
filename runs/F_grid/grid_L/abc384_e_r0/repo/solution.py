import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    strength = S[start]
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
        if s * X < strength:
            heapq.heappop(heap)
            visited[idx] = 1
            strength += s
            push_neighbors(idx)
        else:
            break
    print(strength)

main()
