"""PREREG_v3 E2: the DGM loop of exp/dgm_lcb.py in mode 'randommove', drawing requests from the clean list
exp/random_moves_clean.py instead of exp/random_moves.py. exp/dgm_lcb.py is unchanged: its 'randommove' branch imports
the module named random_moves at call time, and this launcher registers the clean list under that name first.
usage: dgm_lcb_rmclean.py EXP   (EXP's config must have mode 'randommove')"""
import argparse, json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import random_moves_clean
sys.modules['random_moves'] = random_moves_clean
import dgm_lcb

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('exp'); a = ap.parse_args()
    cfg = json.load(open(os.path.join(dgm_lcb.SHI, 'exps', a.exp, 'config.json')))
    assert cfg['mode'] == 'randommove', cfg['mode']
    import random_moves
    assert random_moves.MOVES is random_moves_clean.MOVES
    dgm_lcb.Run(a.exp).run()
