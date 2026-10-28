import sys

def main():
    data = sys.stdin.buffer.read().split()
    n = int(data[0])
    t = [0] * n
    x = [0] * n
    for i in range(n):
        t[i] = data[1 + 2 * i][0] - 48
        x[i] = int(data[2 + 2 * i])
    m = max(x) + 1
    need = [0] * m
    pick = [0] * n
    # backward greedy: match each monster with nearest earlier unmatched potion
    for i in range(n - 1, -1, -1):
        if t[i] == 2:
            need[x[i]] += 1
        else:
            if need[x[i]] > 0:
                need[x[i]] -= 1
                pick[i] = 1
    # check feasibility and compute K
    inv = [0] * m
    cur = 0
    K = 0
    for i in range(n):
        if t[i] == 1:
            if pick[i]:
                inv[x[i]] += 1
                cur += 1
                if cur > K:
                    K = cur
        else:
            if inv[x[i]] == 0:
                print(-1)
                return
            inv[x[i]] -= 1
            cur -= 1
    out = [str(K), " ".join(str(pick[i]) for i in range(n) if t[i] == 1)]
    sys.stdout.write("\n".join(out) + "\n")

main()
