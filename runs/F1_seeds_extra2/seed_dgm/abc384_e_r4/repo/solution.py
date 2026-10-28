import sys, heapq

def main():
    data = sys.stdin.buffer.read().split()
    H, W, X = int(data[0]), int(data[1]), int(data[2])
    P, Q = int(data[3]) - 1, int(data[4]) - 1
    S = [int(v) for v in data[5:5 + H * W]]
    absorbed = [False] * (H * W)
    start = P * W + Q
    total = S[start]
    absorbed[start] = True
    heap = []

    def push_neighbors(cell):
        i, j = divmod(cell, W)
        if i > 0 and not absorbed[cell - W]:
            heapq.heappush(heap, (S[cell - W], cell - W))
        if i < H - 1 and not absorbed[cell + W]:
            heapq.heappush(heap, (S[cell + W], cell + W))
        if j > 0 and not absorbed[cell - 1]:
            heapq.heappush(heap, (S[cell - 1], cell - 1))
        if j < W - 1 and not absorbed[cell + 1]:
            heapq.heappush(heap, (S[cell + 1], cell + 1))

    push_neighbors(start)
    while heap:
        s, c = heapq.heappop(heap)
        if absorbed[c]:
            continue
        if X * s < total:
            absorbed[c] = True
            total += s
            push_neighbors(c)
        else:
            break
    print(total)

main()
