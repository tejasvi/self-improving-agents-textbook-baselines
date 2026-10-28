#!/usr/bin/env python3

import sys
import math

def solve():
    # Read N
    N = int(input())
    
    # Calculate minimum number of friends needed
    # We need ceil(log2(N)) friends to distinguish N bottles
    M = (N - 1).bit_length()  # This is equivalent to ceil(log2(N))
    
    # Print M
    print(M, flush=True)
    
    # Create the distribution of juice to friends
    # Friend i (0-indexed) drinks from bottles whose i-th bit is 1
    # We use bottles numbered 1 to N, so we map bottle k to binary representation (k-1)
    
    friend_bottles = [[] for _ in range(M)]
    
    for bottle_num in range(1, N + 1):
        # bottle_num is 1 to N, convert to 0-indexed for binary representation
        binary_rep = bottle_num - 1
        
        # For each friend/bit position
        for friend_idx in range(M):
            # Check if bit at position friend_idx is set
            if (binary_rep >> friend_idx) & 1:
                friend_bottles[friend_idx].append(bottle_num)
    
    # Output the distribution
    for friend_idx in range(M):
        bottles = friend_bottles[friend_idx]
        output = str(len(bottles)) + ' ' + ' '.join(map(str, bottles))
        print(output, flush=True)
    
    # Read the response
    response = input().strip()
    
    # Convert response to binary number to find the spoiled bottle
    # response[i] is '1' if friend i got sick
    spoiled_binary = 0
    for friend_idx in range(M):
        if response[friend_idx] == '1':
            spoiled_binary |= (1 << friend_idx)
    
    # Convert back to bottle number (1-indexed)
    spoiled_bottle = spoiled_binary + 1
    
    # Print the answer
    print(spoiled_bottle, flush=True)

if __name__ == "__main__":
    solve()
