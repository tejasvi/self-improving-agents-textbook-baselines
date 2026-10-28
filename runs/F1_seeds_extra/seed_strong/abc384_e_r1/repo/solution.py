import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    T = S[start]
    heap = []
    def push_neighbors(c):
        r, col = divmod(c, W)
        if r > 0 and not visited[c - W]:
            visited[c - W] = 1; heapq.heappush(heap, (S[c - W], c - W))
        if r < H - 1 and not visited[c + W]:
            visited[c + W] = 1; heapq.heappush(heap, (S[c + W], c + W))
        if col > 0 and not visited[c - 1]:
            visited[c - 1] = 1; heapq.heappush(heap, (S[c - 1], c - 1))
        if col < W - 1 and not visited[c + 1]:
            visited[c + 1] = 1; heapq.heappush(heap, (S[c + 1], c + 1))
    push_neighbors(start)
    while heap:
        s, c = heap[0]
        if s * X >= T:
            break
        heapq.heappop(heap)
        T += s
        push_neighbors(c)
    print(T)

main()
