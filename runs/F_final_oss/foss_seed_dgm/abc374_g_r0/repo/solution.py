#!/usr/bin/env python3
import sys

def solve():
    input = sys.stdin.readline
    N_line = input().strip()
    if not N_line:
        return
    N = int(N_line)
    # graph over 26 uppercase letters
    adj = [[] for _ in range(26)]
    used_node = [False]*26
    edges = []
    for _ in range(N):
        s = input().strip()
        if not s:
            continue
        u = ord(s[0]) - 65
        v = ord(s[1]) - 65
        adj[u].append(v)
        edges.append((u, v))
        used_node[u] = used_node[v] = True

    # Kosaraju's algorithm for SCCs
    sys.setrecursionlimit(10000)
    visited = [False]*26
    order = []
    def dfs(u):
        visited[u] = True
        for w in adj[u]:
            if not visited[w]:
                dfs(w)
        order.append(u)
    for i in range(26):
        if used_node[i] and not visited[i]:
            dfs(i)
    # reverse graph
    radj = [[] for _ in range(26)]
    for u, v in edges:
        radj[v].append(u)
    comp = [-1]*26
    def rdfs(u, cid):
        comp[u] = cid
        for w in radj[u]:
            if comp[w] == -1:
                rdfs(w, cid)
    cid = 0
    for u in reversed(order):
        if comp[u] == -1:
            rdfs(u, cid)
            cid += 1
    # If there are no edges, answer is 0 (but constraints N>=1)
    # Build condensation DAG indegree/outdegree per component
    indeg = [0]*cid
    outdeg = [0]*cid
    comp_used = [False]*cid
    for u, v in edges:
        cu, cv = comp[u], comp[v]
        comp_used[cu] = comp_used[cv] = True
        if cu != cv:
            outdeg[cu] += 1
            indeg[cv] += 1
    # Count components that actually have at least one incident edge (i.e., appear in edges)
    comps = [i for i in range(cid) if comp_used[i]]
    if len(comps) == 1:
        print(1)
        return
    sources = sum(1 for i in comps if indeg[i] == 0)
    sinks = sum(1 for i in comps if outdeg[i] == 0)
    print(max(sources, sinks))

if __name__ == "__main__":
    solve()
