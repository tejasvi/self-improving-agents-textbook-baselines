"""Write llm_proxy_cache.py = infra/llm_proxy.py + automatic prompt caching (and nothing else), and save the diff.
If a Claude request carries no cache_control, add {"type": "ephemeral"} to (a) the last system block (string -> one text
block), (b) the last tool definition, (c) the last content block of the last message (string -> text block): <= 3
breakpoints. Cache writes/reads are charged by the existing cost_usd() with the PRICES fields."""
import difflib, sys
src, dst, diff = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()
helpers = '''# ---- automatic prompt caching (llm_proxy_cache.py; the only change from llm_proxy.py) ----
EPHEMERAL = {'type': 'ephemeral'}
CACHEABLE = ('text', 'tool_result', 'tool_use', 'image', 'document')

def _blocks_have_cc(blocks):
    for b in blocks if isinstance(blocks, list) else []:
        if not isinstance(b, dict): continue
        if 'cache_control' in b: return True
        if b.get('type') == 'tool_result' and isinstance(b.get('content'), list) and \\
                any(isinstance(x, dict) and 'cache_control' in x for x in b['content']): return True
    return False

def has_cache_control(p):
    """True if the request already sets cache_control anywhere the API accepts it (structural check only)."""
    if 'cache_control' in p or _blocks_have_cc(p.get('system')): return True
    if any(isinstance(t, dict) and 'cache_control' in t for t in p.get('tools') or []): return True
    return any(isinstance(m, dict) and _blocks_have_cc(m.get('content')) for m in p.get('messages') or [])

def _cacheable(b):
    return isinstance(b, dict) and b.get('type') in CACHEABLE and not (b.get('type') == 'text' and not b.get('text'))

def add_cache_breakpoints(p):
    """(a) last system block, (b) last tool definition, (c) last content block of the last message."""
    s = p.get('system')
    if isinstance(s, str) and s.strip():
        p['system'] = [{'type': 'text', 'text': s, 'cache_control': dict(EPHEMERAL)}]
    elif isinstance(s, list) and s and _cacheable(s[-1]):
        p['system'] = s[:-1] + [dict(s[-1], cache_control=dict(EPHEMERAL))]
    t = p.get('tools')
    if isinstance(t, list) and t and isinstance(t[-1], dict):
        p['tools'] = t[:-1] + [dict(t[-1], cache_control=dict(EPHEMERAL))]
    ms = p.get('messages')
    if isinstance(ms, list) and ms and isinstance(ms[-1], dict):
        c = ms[-1].get('content')
        if isinstance(c, str) and c.strip():
            p['messages'] = ms[:-1] + [dict(ms[-1], content=[{'type': 'text', 'text': c, 'cache_control': dict(EPHEMERAL)}])]
        elif isinstance(c, list) and c and _cacheable(c[-1]):
            p['messages'] = ms[:-1] + [dict(ms[-1], content=c[:-1] + [dict(c[-1], cache_control=dict(EPHEMERAL))])]

class State:'''
subs = [
    ("    'claude-sonnet-4-6': (3.00, 15.00, 3.75, 0.30),\n}",
     "    'claude-sonnet-4-6': (3.00, 15.00, 3.75, 0.30),\n"
     "    'claude-sonnet-4-5': (3.00, 15.00, 3.75, 0.30),  # flagship machine copy only (decision 2026-10-24)\n"
     "    'claude-sonnet-4-5@20250929': (3.00, 15.00, 3.75, 0.30),\n}"),
    ('class State:', helpers),
    ("            params['tool_choice'] = tc\n        t0 = time.time(); err = None; resp = None\n",
     "            params['tool_choice'] = tc\n"
     "        if not (model.startswith('gemini') or model.startswith('openai/')) and not has_cache_control(params):\n"
     "            add_cache_breakpoints(params)\n"
     "        t0 = time.time(); err = None; resp = None\n"),
]
t = s
for old, new in subs:
    assert t.count(old) == 1, (old[:60], t.count(old))
    t = t.replace(old, new)
open(dst, 'w').write(t)
open(diff, 'w').writelines(difflib.unified_diff(s.splitlines(True), t.splitlines(True), 'infra/llm_proxy.py', 'llm_proxy_cache.py'))
print('ok', len(s), '->', len(t))
