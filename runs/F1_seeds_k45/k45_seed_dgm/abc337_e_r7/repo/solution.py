import math
import sys

def main():
    N = int(input())
    
    # Calculate minimum number of friends needed
    # We need 2^M >= N, so M = ceil(log2(N))
    M = math.ceil(math.log2(N))
    
    print(M)
    sys.stdout.flush()
    
    # For each friend, determine which bottles to give them
    # Friend i (0-indexed) gets all bottles where bit i is 1
    for friend_idx in range(M):
        bottles = []
        for bottle_idx in range(N):
            # bottle_idx in 0-indexed, so bottle number is bottle_idx + 1
            bottle_num = bottle_idx + 1
            # Check if bit friend_idx is set in bottle_idx
            if (bottle_idx >> friend_idx) & 1:
                bottles.append(bottle_num)
        
        # Print the distribution for this friend
        print(len(bottles), *bottles)
        sys.stdout.flush()
    
    # Read the results
    results = input().strip()
    
    # Reconstruct the bottle number from the results
    # If friend i got upset, bit i is set in the spoiled bottle's number
    spoiled_bottle = 0
    for friend_idx in range(M):
        if results[friend_idx] == '1':
            spoiled_bottle |= (1 << friend_idx)
    
    # Convert from 0-indexed to 1-indexed
    spoiled_bottle += 1
    
    print(spoiled_bottle)
    sys.stdout.flush()

if __name__ == "__main__":
    main()
