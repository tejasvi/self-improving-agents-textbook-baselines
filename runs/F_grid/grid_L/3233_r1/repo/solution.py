class Solution:
    def maxPartitionsAfterOperations(self, s: str, k: int) -> int:
        n = len(s)
        a = [ord(ch) - 97 for ch in s]

        # e[j]: exclusive end of the longest prefix of s[j:] with <= k distinct letters
        e = [n] * (n + 1)
        cnt = [0] * 26
        distinct = 0
        r = 0
        for j in range(n):
            while r < n:
                c = a[r]
                if cnt[c] == 0:
                    if distinct == k:
                        break
                    distinct += 1
                cnt[c] += 1
                r += 1
            e[j] = r
            c = a[j]
            cnt[c] -= 1
            if cnt[c] == 0:
                distinct -= 1

        # R[j]: partitions of s[j:] when a fresh segment starts at j (no change)
        R = [0] * (n + 1)
        for j in range(n - 1, -1, -1):
            R[j] = 1 + R[e[j]]
        best = R[0]

        # Greedy (unchanged) segment start and segment index for each position
        seg_start = [0] * n
        seg_idx = [0] * n
        j = 0
        t = 0
        while j < n:
            end = e[j]
            for i in range(j, end):
                seg_start[i] = j
                seg_idx[i] = t
            t += 1
            j = end

        # pref[l][x]: occurrences of letter l in s[:x]
        pref = [[0] * (n + 1) for _ in range(26)]
        for l in range(26):
            row = pref[l]
            acc = 0
            for x in range(n):
                if a[x] == l:
                    acc += 1
                row[x + 1] = acc

        INF = n + 1
        nextpos = [INF] * 26  # first occurrence at index > i of each letter

        for i in range(n - 1, -1, -1):
            st = seg_start[i]
            p = seg_idx[i]
            Mset = {l for l in range(26) if pref[l][i] - pref[l][st] > 0}
            ordered = sorted((nextpos[l], l) for l in range(26) if nextpos[l] < INF)
            for c in range(26):
                if c in Mset:
                    # changing i to c adds no new letter to the current segment
                    need = k + 1 - len(Mset)
                    q = n
                    seen = 0
                    for pos, l in ordered:
                        if l in Mset:
                            continue
                        seen += 1
                        if seen == need:
                            q = pos
                            break
                    val = p + 1 + R[q]
                else:
                    T = Mset | {c}
                    if len(T) <= k:
                        need = k + 1 - len(T)
                        q = n
                        seen = 0
                        for pos, l in ordered:
                            if l in T:
                                continue
                            seen += 1
                            if seen == need:
                                q = pos
                                break
                        val = p + 1 + R[q]
                    else:
                        # the segment ends right before i; i starts a new segment with c
                        q = n
                        seen = 0
                        for pos, l in ordered:
                            if l == c:
                                continue
                            seen += 1
                            if seen == k:
                                q = pos
                                break
                        val = p + 2 + R[q]
                if val > best:
                    best = val
            nextpos[a[i]] = i
        return best
