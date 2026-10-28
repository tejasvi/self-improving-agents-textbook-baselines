#!/usr/bin/env python3

def is_subsequence(s, t):
    """Check if t is a subsequence of s"""
    t_idx = 0
    for char in s:
        if t_idx < len(t) and char == t[t_idx]:
            t_idx += 1
    return t_idx == len(t)

def get_max_match(s, t):
    """Get the maximum prefix of t that can be matched as subsequence in s"""
    t_idx = 0
    for char in s:
        if t_idx < len(t) and char == t[t_idx]:
            t_idx += 1
    return t_idx

def solve():
    # Read input
    line = input().split()
    N = int(line[0])
    T = line[1]
    
    strings = []
    for _ in range(N):
        strings.append(input().strip())
    
    # For efficiency, we precompute for each string:
    # 1. The maximum prefix of T that can be matched
    # 2. For each prefix length, which strings can complete it
    
    # max_match[i] = maximum length of prefix of T that can be matched in S_i
    max_match = []
    for i in range(N):
        max_match.append(get_max_match(strings[i], T))
    
    # For each possible prefix length (0 to len(T)), track which strings can complete
    # For prefix of length k, we need strings that can match T[k:] as subsequence
    
    # suffixes[k] = for prefix of length k, which strings can match the remaining T[k:]
    suffixes = [[] for _ in range(len(T) + 1)]
    for i in range(N):
        # For string S_i, it can match T[k:] if we check
        for k in range(len(T) + 1):
            if is_subsequence(strings[i], T[k:]):
                suffixes[k].append(i)
    
    count = 0
    for i in range(N):
        # For string S_i, it matches max_match[i] characters of T
        # We need to count strings j such that S_j can match T[max_match[i]:]
        remaining_need = max_match[i]
        # Count how many strings can match the suffix T[remaining_need:]
        count += len(suffixes[remaining_need])
    
    print(count)

solve()
