import sys

def main():
    data = sys.stdin.buffer.read().split()
    H = int(data[0]); W = int(data[1])
    rows = data[2:2 + H]
    MOD = 998244353
    W2 = W + 2
    N = (H + 2) * W2
    green = bytearray(N)
    for i in range(H):
        r = rows[i]
        base = (i + 1) * W2 + 1
        for j in range(W):
            if r[j] == 35:  # '#'
                green[base + j] = 1
    label = [0] * N
    C = 0
    dirs = (1, -1, W2, -W2)
    for p in range(N):
        if green[p] and not label[p]:
            C += 1
            label[p] = C
            stack = [p]
            while stack:
                q = stack.pop()
                for d in dirs:
                    t = q + d
                    if green[t] and not label[t]:
                        label[t] = C
                        stack.append(t)
    total = 0
    red_cnt = 0
    for i in range(1, H + 1):
        base = i * W2
        for p in range(base + 1, base + W + 1):
            if not green[p]:
                red_cnt += 1
                a = label[p - 1]
                b = label[p + 1]
                c = label[p - W2]
                e = label[p + W2]
                s = 0
                if a: s += 1
                if b and b != a: s += 1
                if c and c != a and c != b: s += 1
                if e and e != a and e != b and e != c: s += 1
                total += C + 1 - s
    ans = total % MOD * pow(red_cnt % MOD, MOD - 2, MOD) % MOD
    print(ans)

main()
