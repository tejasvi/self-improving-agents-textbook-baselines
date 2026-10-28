import sys

def main():
    data = sys.stdin.buffer.read().split()
    H, W, N = int(data[0]), int(data[1]), int(data[2])
    holes = [set() for _ in range(H + 1)]
    p = 3
    for _ in range(N):
        a = int(data[p]); b = int(data[p + 1]); p += 2
        holes[a].add(b)
    prev = [0] * (W + 1)  # 1-based, prev[0] = 0 sentinel
    total = 0
    for i in range(1, H + 1):
        hs = holes[i]
        # A[j] = min(prev[j], prev[j-1]) for j in 1..W, vectorized via map
        A = list(map(min, prev[1:], prev[:-1]))  # A[k] corresponds to j = k+1
        cur = [0] * (W + 1)
        c = 0
        if hs:
            for j in range(1, W + 1):
                if j in hs:
                    c = 0
                else:
                    a = A[j - 1]
                    c = (c if c < a else a) + 1
                cur[j] = c
        else:
            for j in range(1, W + 1):
                a = A[j - 1]
                c = (c if c < a else a) + 1
                cur[j] = c
        total += sum(cur)
        prev = cur
    print(total)

main()
