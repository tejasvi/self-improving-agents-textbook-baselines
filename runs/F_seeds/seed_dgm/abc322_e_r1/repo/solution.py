import sys


def main():
    data = sys.stdin.read().split()
    idx = 0
    n = int(data[idx]); idx += 1
    k = int(data[idx]); idx += 1
    p = int(data[idx]); idx += 1
    items = []
    for _ in range(n):
        c = int(data[idx]); idx += 1
        a = tuple(int(x) for x in data[idx:idx + k])
        idx += k
        items.append((c, a))

    start = tuple([0] * k)
    target = tuple([p] * k)
    dp = {start: 0}
    for c, a in items:
        new_dp = dict(dp)
        for state, cost in dp.items():
            ns = tuple(min(p, s + x) for s, x in zip(state, a))
            nc = cost + c
            old = new_dp.get(ns)
            if old is None or nc < old:
                new_dp[ns] = nc
        dp = new_dp

    ans = dp.get(target, -1)
    print(ans)


if __name__ == "__main__":
    main()
