import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    visited = bytearray(H * W)
    start = P * W + Q
    visited[start] = 1
    strength = S[start]
    heap = []

    def push_neighbors(cell):
        r, c = divmod(cell, W)
        if r > 0 and not visited[cell - W]:
            heapq.heappush(heap, (S[cell - W], cell - W))
        if r < H - 1 and not visited[cell + W]:
            heapq.heappush(heap, (S[cell + W], cell + W))
        if c > 0 and not visited[cell - 1]:
            heapq.heappush(heap, (S[cell - 1], cell - 1))
        if c < W - 1 and not visited[cell + 1]:
            heapq.heappush(heap, (S[cell + 1], cell + 1))

    push_neighbors(start)
    while heap:
        s, cell = heap[0]
        if visited[cell]:
            heapq.heappop(heap)
            continue
        if s * X >= strength:
            break
        heapq.heappop(heap)
        visited[cell] = 1
        strength += s
        push_neighbors(cell)
    print(strength)

main()
