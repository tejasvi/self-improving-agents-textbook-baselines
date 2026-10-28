"""PREREG_v2 B1: build the 16 textbook-move variants of the DGM seed (file swaps from the hand-written seed).

E = tools/edit.py, B = tools/bash.py, L = llm_withtools.py, P = coding_agent.py. Output: harness/grid/<subset>/ ('none' = seed).
"""
import itertools, os, shutil
H = os.path.expanduser('~/shi_eval/harness')
MOVES = {'E': 'tools/edit.py', 'B': 'tools/bash.py', 'L': 'llm_withtools.py', 'P': 'coding_agent.py'}
IGN = shutil.ignore_patterns('.git', '__pycache__', '*.pyc', '.pytest_cache')

def build():
    out = os.path.join(H, 'grid'); os.makedirs(out, exist_ok=False)
    names = []
    for r in range(5):
        for sub in itertools.combinations('EBLP', r):
            name = ''.join(sub) or 'none'
            d = os.path.join(out, name)
            shutil.copytree(os.path.join(H, 'seed_dgm'), d, ignore=IGN)
            for m in sub:
                shutil.copy2(os.path.join(H, 'seed_strong', MOVES[m]), os.path.join(d, MOVES[m]))
            names.append(name)
    return names

if __name__ == '__main__':
    print(' '.join(build()))
