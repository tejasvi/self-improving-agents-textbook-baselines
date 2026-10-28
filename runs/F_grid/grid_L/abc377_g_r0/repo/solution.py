import sys


def main():
    data = sys.stdin.read().split()
    n = int(data[0])
    strs = data[1:1 + n]

    INF = float("inf")
    children = [{}]          # trie: list of dicts child char -> node index
    min_len = [INF]          # min length of strings whose path passes through node

    out = []
    for s in strs:
        L = len(s)
        # query: walk trie along s
        best = L
        node = 0
        d = 0
        # root candidate (d = 0)
        if min_len[0] < INF:
            best = min(best, L + min_len[0])
        for ch in s:
            nxt = children[node].get(ch)
            if nxt is None:
                break
            node = nxt
            d += 1
            cand = L + min_len[node] - 2 * d
            if cand < best:
                best = cand
        out.append(best)

        # insert s
        node = 0
        if L < min_len[0]:
            min_len[0] = L
        for ch in s:
            nxt = children[node].get(ch)
            if nxt is None:
                nxt = len(children)
                children.append({})
                min_len.append(INF)
                children[node][ch] = nxt
            node = nxt
            if L < min_len[node]:
                min_len[node] = L

    sys.stdout.write("\n".join(map(str, out)) + "\n")


main()
