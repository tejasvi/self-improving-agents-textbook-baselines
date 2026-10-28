import sys


def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0])
    W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353

    # Padded grid: (H+2) x (W+2), green = 1
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        row = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if row[j] == 35:  # '#'
                green[base + j] = 1

    label = [0] * N  # 0 = unlabeled
    C = 0
    for s in range(N):
        if green[s] and not label[s]:
            C += 1
            label[s] = C
            dq = [s]
            while dq:
                v = dq.pop()
                for u in (v - 1, v + 1, v - W2, v + W2):
                    if green[u] and not label[u]:
                        label[u] = C
                        dq.append(u)

    R = 0
    sum_k = 0
    for i in range(1, H + 1):
        base = i * W2
        for j in range(1, W + 1):
            p = base + j
            if green[p]:
                continue
            R += 1
            a = label[p - 1]
            b = label[p + 1]
            c = label[p - W2]
            d = label[p + W2]
            k = 0
            seen = []
            for x in (a, b, c, d):
                if x and x not in seen:
                    seen.append(x)
            k = len(seen)
            sum_k += k

    # Sum over red cells of (C - k + 1) = R*(C+1) - sum_k
    total = R * (C + 1) - sum_k
    ans = total % MOD * pow(R % MOD, MOD - 2, MOD) % MOD
    print(ans)


main()
