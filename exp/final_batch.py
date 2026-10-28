"""PREREG_v2 H7 (and common re-measurement): every loop arm's reported best agent, chosen exactly as in
analysis/summary.py (ladder_report.loop_best: highest full selection score among archive members, the initial agent
included), plus same-batch references, evaluated together on F x 2 (exp/eval_interleaved.py -> results/F_final.jsonl).

Run once all listed loop arms have ended. Writes results/F_final_manifest.json (arm -> chosen best) before launching.
usage: final_batch.py [--dry] [--workers N]
"""
import argparse, json, os, sys, time
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis')); sys.path.insert(0, os.path.join(SHI, 'exp'))
from collect import collect
import ladder_report as LR

ARMS = ['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3', 'v2_A_nohint_s1', 'v2_A_nohint_s2',
        'v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6', 'v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3',
        'v3_H_hgm_s1', 'v3_H_hgm_s2', 'v3_H_hgm_s3']
REFS = [('fin_seed_dgm', os.path.join(SHI, 'harness/seed_dgm')),
        ('fin_seed_dgm_cap16k', os.path.join(SHI, 'harness/seed_dgm_cap16k')),
        ('fin_grid_L', os.path.join(SHI, 'harness/grid/L'))]

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('--dry', action='store_true'); ap.add_argument('--workers', type=int, default=64)
    a = ap.parse_args()
    man = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'arms': {}}; agents = list(REFS)
    for e in ARMS:
        cfg, st, recs = collect(e); b = LR.loop_best(recs)
        ent = {'generation': st.get('generation'), 'best': b and b['aid'], 'best_S': b and b['sel']}
        if b and b['aid'] != 'initial':
            name = f"fin_{e}__{b['aid']}"; agents.append((name, os.path.join(SHI, 'exps', e, 'agents', b['aid'], 'code')))
            ent['agent_name'] = name
        else:
            ent['agent_name'] = 'fin_seed_dgm'   # no archive member beat the seed: the loop reports the seed itself
        man['arms'][e] = ent
    print(json.dumps(man, indent=1))
    if a.dry: return
    json.dump(man, open(os.path.join(SHI, 'results', 'F_final_manifest.json'), 'w'), indent=1)
    import eval_interleaved
    eval_interleaved.main('F_final', 'fresh', 2, 'claude-haiku-5-5', a.workers, agents)

if __name__ == '__main__':
    main()
