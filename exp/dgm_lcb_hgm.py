"""PREREG_v2 G-search: DGM loop with HGM-style parent selection (everything else as exp/dgm_lcb.py).

HGM (Huxley-Goedel Machine) ranks a node by the productivity of its clade (the node and all its descendants) and picks
the node to expand by Thompson sampling. Here: for each archive member n, S_n / F_n = passed / failed selection-set task
runs summed over n and every evaluated descendant (archive member or not); theta_n ~ Beta(1 + S_n, 1 + F_n); the parent
is the argmax of theta. One draw per self-improvement attempt. Failing-task choice, diagnosis, self-modification,
staged evaluation, archive update and final-agent choice are unchanged.
"""
import argparse, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dgm_lcb

class HGMRun(dgm_lcb.Run):
    def clade_counts(self, archive):
        agents = [a for a in os.listdir(os.path.join(self.dir, 'agents'))]
        parent = {}
        for a in agents:
            m = self.meta(a)
            if m is not None: parent[a] = m.get('parent')
        own = {}
        for a in parent:
            try: p = self.perf(a)
            except Exception: continue
            own[a] = (len(p['total_resolved_ids']), len(p['total_unresolved_ids']) + len(p['total_emptypatch_ids']))
        S = {a: 0 for a in archive}; F = {a: 0 for a in archive}
        for a, (s, f) in own.items():
            x = a; seen = set()
            while x is not None and x not in seen:   # credit a's results to every ancestor in the archive
                seen.add(x)
                if x in S: S[x] += s; F[x] += f
                x = parent.get(x) if x != 'initial' else None
        return S, F

    def choose_selfimproves(self, archive, k):
        S, F = self.clade_counts(archive)
        out = []
        for _ in range(k):
            th = {a: self.rng.betavariate(1 + S[a], 1 + F[a]) for a in archive}
            par = max(archive, key=lambda a: th[a])
            p = self.perf(par)
            ids = p['total_emptypatch_ids'] + p['total_unresolved_ids']
            if not ids: ids = p['total_resolved_ids'] + ids
            out.append((par, self.rng.choice(ids)))
        return out

if __name__ == '__main__':
    ap = argparse.ArgumentParser(); ap.add_argument('exp'); a = ap.parse_args()
    HGMRun(a.exp).run()
