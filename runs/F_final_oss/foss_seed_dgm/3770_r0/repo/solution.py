class Solution:
    def generateString(self, str1: str, str2: str) -> str:
        n = len(str1)
        m = len(str2)
        L = n + m - 1
        # forced characters from 'T' constraints
        forced = [None] * L
        for i, ch in enumerate(str1):
            if ch == 'T':
                for k in range(m):
                    pos = i + k
                    c = str2[k]
                    if forced[pos] is None:
                        forced[pos] = c
                    elif forced[pos] != c:
                        return ""
        # collect F windows
        windows = []  # each: dict with start, end, satisfied
        start_idx = {}
        end_idx = {}
        for i, ch in enumerate(str1):
            if ch == 'F':
                start = i
                end = i + m - 1
                win_id = len(windows)
                windows.append({"start": start, "end": end, "satisfied": False})
                start_idx.setdefault(start, []).append(win_id)
                end_idx.setdefault(end, []).append(win_id)
        # build answer
        ans = [''] * L
        active = []  # list of window ids currently covering current position
        for pos in range(L):
            # add new windows starting here
            if pos in start_idx:
                active.extend(start_idx[pos])
            forced_char = forced[pos]
            # determine which active windows ending here are still unsatisfied
            required_set = set()
            for win_id in end_idx.get(pos, []):
                if not windows[win_id]["satisfied"]:
                    start = windows[win_id]["start"]
                    needed = str2[pos - start]
                    required_set.add(needed)
            # choose character
            if required_set:
                if forced_char is not None:
                    # forced char must differ from all required chars
                    if forced_char in required_set:
                        return ""
                    chosen = forced_char
                else:
                    # smallest letter not in required_set
                    for c in "abcdefghijklmnopqrstuvwxyz":
                        if c not in required_set:
                            chosen = c
                            break
            else:
                chosen = forced_char if forced_char is not None else 'a'
            ans[pos] = chosen
            # update satisfaction for active windows and prune those ending here
            new_active = []
            for win_id in active:
                if not windows[win_id]["satisfied"]:
                    start = windows[win_id]["start"]
                    needed = str2[pos - start]
                    if chosen != needed:
                        windows[win_id]["satisfied"] = True
                # keep if not ending yet
                if pos < windows[win_id]["end"]:
                    new_active.append(win_id)
            active = new_active
        # after constructing, verify all F windows are satisfied (should be true)
        for w in windows:
            if not w["satisfied"]:
                return ""
        return "".join(ans)
