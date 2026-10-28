"""PREREG_v3 E2 final evaluation (run on the second machine as user lcb after the eight v3 loops end): one common batch,
all 232 fresh problems x 2 runs, interleaved: the reported best agents of the five clean random-diagnosis loops
(v4_RMC_s11-15), the three v2 random-diagnosis loops (v3_RM_s1-3), the three same-time DGM loops (v4_A_dgm_s7-9) and the
six earlier DGM loops (v2_A_dgm_s1-3, v3_A_dgm_s4-6); the DGM seed; L (harness/grid/L). Earlier loops' best agents are
taken from results/F_final_manifest.json; new loops' from dgm_lcb.Run(exp).best(). Writes results/F_final_r3_manifest.json
and runs exp/eval_interleaved.py with tag F_final_r3.
usage: r3_final_batch.py WORKERS [--dry-run]"""
import json, os, subprocess, sys, time
SHI = os.path.expanduser('~/shi_eval'); sys.path.insert(0, os.path.join(SHI, 'exp'))
import dgm_lcb
NEW = [f'v4_RMC_s{s}' for s in range(11, 16)] + [f'v4_A_dgm_s{s}' for s in (7, 8, 9)]
OLD = ['v3_RM_s1', 'v3_RM_s2', 'v3_RM_s3', 'v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3', 'v3_A_dgm_s4', 'v3_A_dgm_s5', 'v3_A_dgm_s6']
def main(workers, dry):
    man = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'arms': {}}
    old = json.load(open(os.path.join(SHI, 'results', 'F_final_manifest.json')))['arms']
    for e in NEW:
        R = dgm_lcb.Run(e); st = R.state(); assert st['generation'] >= 40, (e, st['generation'])
        b = R.best(); man['arms'][e] = {'generation': st['generation'], 'best': b, 'best_S': R.perf(b)['accuracy_score']}
    for e in OLD:
        man['arms'][e] = {'generation': old[e]['generation'], 'best': old[e]['best'], 'best_S': old[e]['best_S']}
    agents = [('r3_seed_dgm', os.path.join(SHI, 'harness', 'seed_dgm')), ('r3_grid_L', os.path.join(SHI, 'harness', 'grid', 'L'))]
    for e, v in man['arms'].items():
        p = os.path.join(SHI, 'exps', e, 'agents', v['best'], 'code'); assert os.path.isdir(p), p
        v['agent_name'] = f"r3_{e}__{v['best']}"; agents.append((v['agent_name'], p))
    json.dump(man, open(os.path.join(SHI, 'results', 'F_final_r3_manifest.json'), 'w'), indent=1)
    print(json.dumps({e: (v['best'], v['best_S']) for e, v in man['arms'].items()}, indent=0))
    if dry: return
    cmd = [sys.executable, '-I', os.path.join(SHI, 'exp', 'eval_interleaved.py'), 'F_final_r3', 'fresh', '2', 'claude-haiku-5-5',
           str(workers)] + [f'{n}={p}' for n, p in agents]
    subprocess.run(cmd, check=True)
if __name__ == '__main__':
    main(int(sys.argv[1]), '--dry-run' in sys.argv)
