import sys
import os
import subprocess
import tempfile

C_SRC = r"""
#include <stdio.h>
#include <string.h>
#define INF 1000000000000000LL
static long long d[20][20];
static long long dp[1<<20][20];
int main(void){
    int n, m;
    if (scanf("%d %d", &n, &m) != 2) return 0;
    for (int i = 0; i < n; i++) for (int j = 0; j < n; j++) d[i][j] = (i==j)?0:INF;
    for (int i = 0; i < m; i++) {
        int u, v; long long w;
        if (scanf("%d %d %lld", &u, &v, &w) != 3) return 1;
        u--; v--;
        if (w < d[u][v]) d[u][v] = w;
    }
    for (int k = 0; k < n; k++)
        for (int i = 0; i < n; i++) {
            for (int j = 0; j < n; j++) {
                long long c = d[i][k] + d[k][j];
                if (c < d[i][j]) d[i][j] = c;
            }
        }
    int full = (1<<n) - 1;
    for (int mask = 0; mask <= full; mask++)
        for (int v = 0; v < n; v++) dp[mask][v] = INF;
    for (int v = 0; v < n; v++) dp[1<<v][v] = 0;
    for (int mask = 1; mask <= full; mask++) {
        for (int v = 0; v < n; v++) {
            if (!(mask >> v & 1)) continue;
            long long cur = dp[mask][v];
            if (cur >= INF / 2) continue;
            for (int u = 0; u < n; u++) {
                if (mask >> u & 1) continue;
                long long c = cur + d[v][u];
                int nm = mask | (1<<u);
                if (c < dp[nm][u]) dp[nm][u] = c;
            }
        }
    }
    long long best = INF;
    for (int v = 0; v < n; v++) if (dp[full][v] < best) best = dp[full][v];
    if (best >= INF / 2) printf("No\n");
    else printf("%lld\n", best);
    return 0;
}
"""


def solve_c(data):
    tmpdir = tempfile.mkdtemp()
    src = os.path.join(tmpdir, "a.c")
    exe = os.path.join(tmpdir, "a.out")
    with open(src, "w") as f:
        f.write(C_SRC)
    subprocess.run(["gcc", "-O3", "-o", exe, src], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, timeout=30)
    res = subprocess.run([exe], input=data.encode(), stdout=subprocess.PIPE, timeout=30, check=True)
    return res.stdout.decode().strip()


def solve_py(data):
    it = iter(data.split())
    n = int(next(it)); m = int(next(it))
    INF = float('inf')
    d = [[INF] * n for _ in range(n)]
    for i in range(n):
        d[i][i] = 0
    for _ in range(m):
        u = int(next(it)) - 1; v = int(next(it)) - 1; w = int(next(it))
        if w < d[u][v]:
            d[u][v] = w
    for k in range(n):
        dk = d[k]
        for i in range(n):
            dik = d[i][k]
            if dik == INF:
                continue
            di = d[i]
            for j in range(n):
                c = dik + dk[j]
                if c < di[j]:
                    di[j] = c
    full = (1 << n) - 1
    dp = [None] * (full + 1)
    for mask in range(full + 1):
        dp[mask] = [INF] * n
    for v in range(n):
        dp[1 << v][v] = 0
    for mask in range(1, full + 1):
        row = dp[mask]
        for v in range(n):
            cur = row[v]
            if cur == INF:
                continue
            dv = d[v]
            for u in range(n):
                if mask >> u & 1 or dv[u] == INF:
                    continue
                nm = mask | (1 << u)
                c = cur + dv[u]
                if c < dp[nm][u]:
                    dp[nm][u] = c
    best = min(dp[full])
    return "No" if best == INF else str(best)


def main():
    data = sys.stdin.read()
    try:
        out = solve_c(data)
    except Exception:
        out = solve_py(data)
    print(out)


main()
