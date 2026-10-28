import sys
import heapq

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1]); X = int(data[2])
    P = int(data[3]) - 1; Q = int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    start = P * W + Q
    total = S[start]
    absorbed = [False] * (H * W)
    absorbed[start] = True
    heap = []
    def push_neighbors(idx):
        i, j = divmod(idx, W)
        if i > 0 and not absorbed[idx - W]:
            heapq.heappush(heap, (S[idx - W], idx - W))
        if i < H - 1 and not absorbed[idx + W]:
            heapq.heappush(heap, (S[idx + W], idx + W))
        if j > 0 and not absorbed[idx - 1]:
            heapq.heappush(heap, (S[idx - 1], idx - 1))
        if j < W - 1 and not absorbed[idx + 1]:
            heapq.heappush(heap, (S[idx + 1], idx + 1))
    push_neighbors(start)
    while heap:
        s, idx = heapq.heappop(heap)
        if absorbed[idx]:
            continue
        if s * X >= total:
            break
        absorbed[idx] = True
        total += s
        push_neighbors(idx)
    print(total)

main()
