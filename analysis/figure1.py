"""Figure 1: (a) best-so-far selection score by generation, DGM loops vs placebo loops, with the order-statistics
prediction; (b) fresh pass rate vs cost per task for resampled seeds and evolved agents. Writes paper/fig1.pdf."""
import json, os, sys
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
sys.path.insert(0, os.path.dirname(__file__))
from curves import curve, seed_stats, emax
SHI = os.path.expanduser('~/shi_eval')
BLUE, ORANGE, AQUA = '#2a78d6', '#eb6834', '#1baf7a'
INK, INK2, GRID = '#0b0b0b', '#52514e', '#e4e3df'
plt.rcParams.update({'font.size': 8.5, 'axes.edgecolor': INK2, 'axes.labelcolor': INK, 'xtick.color': INK2,
                     'ytick.color': INK2, 'axes.spines.top': False, 'axes.spines.right': False,
                     'pdf.fonttype': 42, 'font.family': 'DejaVu Sans'})

def stepped(exp, maxgen=40):
    c = curve(exp); best = {}; nfull = {}
    for g, b, a, n in c: best[g] = b; nfull[g] = n
    gens = sorted(best); xs, ys, ns = [], [], []
    cur = best[gens[0]]; curn = nfull[gens[0]]
    for g in range(0, min(maxgen, max(gens)) + 1):
        if g in best: cur = best[g]; curn = nfull[g]
        xs.append(g); ys.append(100 * cur); ns.append(curn)
    return np.array(xs), np.array(ys), np.array(ns)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.0, 2.8), gridspec_kw={'width_ratios': [1.05, 1]})
# seed reference: the same evaluations as the text (seed runs and placebo copies, results/summary.json)
_sr = json.load(open(os.path.join(SHI, 'results', 'summary.json')))['seedDgm_S_runs']
mu, sd = 100 * _sr['mean'], 100 * _sr['sd']
ax1.axhspan(mu - sd, mu + sd, color=GRID, lw=0, zorder=0)
ax1.axhline(mu, color=INK2, lw=0.8, zorder=1)
preds = []
for i, e in enumerate(['v2_B_placebo_s1', 'v2_B_placebo_s2', 'v2_B_placebo_s3']):
    x, y, n = stepped(e)
    ax1.step(x, y, where='post', color=ORANGE, lw=1.4, alpha=0.9, label='placebo loops' if i == 0 else None, zorder=3)
    preds.append(np.array([mu + sd * emax(int(k), sims=60000) for k in n]))
L = min(len(p) for p in preds)
ax1.plot(np.arange(L), np.mean([p[:L] for p in preds], 0), color=INK2, lw=1.0, ls='--', zorder=2,
         label='expected max of placebo scores')
for i, e in enumerate(['v2_A_dgm_s1', 'v2_A_dgm_s2', 'v2_A_dgm_s3']):
    x, y, n = stepped(e)
    ax1.step(x, y, where='post', color=BLUE, lw=1.6, label='DGM loops' if i == 0 else None, zorder=4)
ax1.text(39.5, mu - sd + 0.4, 'seed, mean $\\pm$ sd', ha='right', va='bottom', color=INK2, fontsize=7.5)
ax1.set_xlim(0, 40); ax1.set_xlabel('generation'); ax1.set_ylabel('best selection score (%)')
ax1.yaxis.grid(True, color=GRID, lw=0.6); ax1.set_axisbelow(True)
ax1.legend(frameon=False, loc='upper left', fontsize=7.5, handlelength=1.6)
ax1.set_title('(a) reported progress', loc='left', fontsize=9, color=INK)

sk = json.load(open(os.path.join(SHI, 'results', 'seed_at_k.json')))
summ = json.load(open(os.path.join(SHI, 'results', 'summary.json')))
for k, col, lab in (('seed_dgm', BLUE, 'DGM seed, best of $k$'), ('seed_strong', ORANGE, 'engineered seed, best of $k$')):
    ks = sorted((q for q in sk[k] if q.isdigit()), key=int)
    xs = [1000 * sk[k][q]['usd_per_task'] for q in ks]; ys = [100 * sk[k][q]['acc'] for q in ks]
    ax2.plot(xs, ys, color=col, lw=1.4, marker='o', ms=4.5, mec='white', mew=0.8, label=lab, zorder=3)
    ax2.annotate('$k$=1', (xs[0], ys[0]), xytext=(6, -3), textcoords='offset points', fontsize=7, color=INK2, va='top')
lab = {'LoopA': 'loop 1', 'LoopB': 'loop 2', 'LoopC': 'loop 3', 'NohintA': 'no-hint 1', 'NohintB': 'no-hint 2',
       'StrongA': 'engineered-seed loop 1', 'StrongB': 'engineered-seed loop 2'}
off = {'LoopA': (4, -10), 'LoopB': (5, 3), 'LoopC': (-6, -11), 'NohintA': (-6, 4), 'NohintB': (6, -2),
       'StrongA': (6, -10), 'StrongB': (6, 2)}
first = True
for key, rec in summ['loops'].items():
    if 'F1' not in rec or rec.get('usd') is None: continue
    x, y = 1000 * rec['usd'], 100 * rec['F1']
    ax2.plot([x], [y], marker='D', ms=5, color=AQUA, mec='white', mew=0.8, ls='none', zorder=4,
             label='evolved agents (loop bests)' if first else None)
    first = False
    if key in ('LoopA', 'LoopB'):   # the top cluster (loop 3, no-hint and engineered-seed loops) gets one group label
        dx, dy = off.get(key, (5, 0))
        ax2.annotate(lab.get(key, key), (x, y), xytext=(dx, dy), textcoords='offset points', fontsize=7, color=INK,
                     ha='left' if dx >= 0 else 'right')
top = [(1000 * r['usd'], 100 * r['F1']) for k, r in summ['loops'].items()
       if k not in ('LoopA', 'LoopB') and 'F1' in r and r.get('usd') is not None]
if top:
    tx, ty = min(x for x, _ in top), min(y for _, y in top)
    ax2.annotate('loop 3, no-hint and\nengineered-seed loops', (tx, ty), xytext=(tx - 0.5, ty - 7), fontsize=7, color=INK,
                 ha='left', arrowprops=dict(arrowstyle='-', color=INK2, lw=0.6))
ax2.set_xlabel('cost per thousand tasks (USD)'); ax2.set_ylabel('fresh pass rate (%)')
ax2.yaxis.grid(True, color=GRID, lw=0.6); ax2.set_axisbelow(True)
ax2.legend(frameon=False, loc='lower right', fontsize=7.2, handlelength=1.6)
ax2.set_title('(b) fresh problems vs cost', loc='left', fontsize=9, color=INK)
fig.tight_layout(w_pad=2.0)
out = os.path.join(SHI, 'paper', 'fig1.pdf'); fig.savefig(out); fig.savefig(out.replace('.pdf', '.png'), dpi=200)
print('wrote', out)
