import sys
import heapq


def main():
    data = sys.stdin.buffer.read().split()
    idx = 0
    H = int(data[idx]); idx += 1
    W = int(data[idx]); idx += 1
    X = int(data[idx]); idx += 1
    P = int(data[idx]) - 1; idx += 1
    Q = int(data[idx]) - 1; idx += 1
    S = [0] * (H * W)
    for k in range(H * W):
        S[k] = int(data[idx + k])
    start = P * W + Q
    cur = S[start]
    absorbed = bytearray(H * W)
    absorbed[start] = 1
    heap = []

    def push_neighbors(c):
        r, col = divmod(c, W)
        if r > 0 and not absorbed[c - W]:
            heapq.heappush(heap, (S[c - W], c - W))
        if r < H - 1 and not absorbed[c + W]:
            heapq.heappush(heap, (S[c + W], c + W))
        if col > 0 and not absorbed[c - 1]:
            heapq.heappush(heap, (S[c - 1], c - 1))
        if col < W - 1 and not absorbed[c + 1]:
            heapq.heappush(heap, (S[c + 1], c + 1))

    push_neighbors(start)
    while heap:
        s, c = heap[0]
        if absorbed[c]:
            heapq.heappop(heap)
            continue
        if s * X >= cur:
            break
        heapq.heappop(heap)
        absorbed[c] = 1
        cur += s
        push_neighbors(c)
    print(cur)


main()
