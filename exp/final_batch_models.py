"""Final fresh evaluation for loops run with other task models (K45: claude-haiku-4-5; O: gpt-oss-120b via the second
proxy). Same best-agent rule as exp/final_batch.py (ladder_report.loop_best); references evaluated in the same batch.

usage: final_batch_models.py k45|oss [--dry] [--workers N]
  k45: arms v3_K45_dgm_s1, v3_K45_dgm_s2, refs seed_dgm + seed_strong; model claude-haiku-4-5, budget $1, F x 1
       -> results/F_final_k45.jsonl
  oss: arms v3_O_dgm_s1..s3, refs seed_dgm + seed_strong; model openai/gpt-oss-120b-maas, budget $0.25, F x 1, run with
       SHI_PROXY_SOCK=~/shi_eval/ledger2/proxy.sock -> results/F_final_oss.jsonl
Writes results/F_final_<k>_manifest.json before launching.
"""
import argparse, json, os, sys, time
SHI = os.path.expanduser('~/shi_eval')
sys.path.insert(0, os.path.join(SHI, 'analysis')); sys.path.insert(0, os.path.join(SHI, 'exp'))
from collect import collect
import ladder_report as LR
CFG = {'k45': dict(arms=['v3_K45_dgm_s1', 'v3_K45_dgm_s2'], model='claude-haiku-4-5', budget='1.0'),
       'oss': dict(arms=['v3_O_dgm_s1', 'v3_O_dgm_s2', 'v3_O_dgm_s3'], model='openai/gpt-oss-120b-maas', budget='0.25')}

def main():
    ap = argparse.ArgumentParser(); ap.add_argument('which', choices=list(CFG)); ap.add_argument('--dry', action='store_true')
    ap.add_argument('--workers', type=int, default=32); a = ap.parse_args(); c = CFG[a.which]
    if a.which == 'oss' and 'ledger2' not in os.environ.get('SHI_PROXY_SOCK', ''):
        sys.exit('oss batch must run with SHI_PROXY_SOCK pointing to ~/shi_eval/ledger2/proxy.sock')
    pre = f'f{a.which}_'
    agents = [(pre + 'seed_dgm', os.path.join(SHI, 'harness/seed_dgm')), (pre + 'seed_strong', os.path.join(SHI, 'harness/seed_strong'))]
    man = {'ts': time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()), 'model': c['model'], 'budget': c['budget'], 'arms': {}}
    for e in c['arms']:
        cfg, st, recs = collect(e); b = LR.loop_best(recs)
        ent = {'generation': st.get('generation'), 'best': b and b['aid'], 'best_S': b and b['sel']}
        if b and b['aid'] != 'initial':
            name = f"{pre}{e}__{b['aid']}"; agents.append((name, os.path.join(SHI, 'exps', e, 'agents', b['aid'], 'code')))
            ent['agent_name'] = name
        else:
            ent['agent_name'] = pre + 'seed_dgm'
        man['arms'][e] = ent
    print(json.dumps(man, indent=1))
    if a.dry: return
    json.dump(man, open(os.path.join(SHI, 'results', f'F_final_{a.which}_manifest.json'), 'w'), indent=1)
    os.environ['EVAL_BUDGET'] = c['budget']
    import eval_interleaved
    eval_interleaved.main(f'F_final_{a.which}', 'fresh', 1, c['model'], a.workers, agents)

if __name__ == '__main__':
    main()
