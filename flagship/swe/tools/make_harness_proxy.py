"""Write swe/dgm_harness_proxy.py = DGM's swe_bench/harness.py with the two changes the flagship needs
(per-run proxy key per instance, ANTHROPIC_BASE_URL passed into the task container) and save the diff."""
import difflib, sys, os
src, dst, diff = sys.argv[1], sys.argv[2], sys.argv[3]
s = open(src).read()
subs = [
    ("def process_entry(entry, out_dname, model_name_or_path, model_patch_paths):\n",
     "# flagship: the driver replaces this with a per-instance proxy token minter (default = DGM's behaviour)\n"
     "api_key_for = lambda instance_id: os.getenv('ANTHROPIC_API_KEY')\n\n"
     "def process_entry(entry, out_dname, model_name_or_path, model_patch_paths):\n"),
    ("            \"ANTHROPIC_API_KEY\": os.getenv('ANTHROPIC_API_KEY'),\n",
     "            \"ANTHROPIC_API_KEY\": api_key_for(instance_id),  # flagship: per-run proxy token\n"
     "            \"ANTHROPIC_BASE_URL\": os.getenv('ANTHROPIC_BASE_URL'),  # flagship: proxy on the docker bridge\n"),
]
t = s
for old, new in subs:
    assert t.count(old) == 1, (old, t.count(old))
    t = t.replace(old, new)
open(dst, 'w').write(t)
open(diff, 'w').writelines(difflib.unified_diff(s.splitlines(True), t.splitlines(True), 'dgm_repo/swe_bench/harness.py', 'swe/dgm_harness_proxy.py'))
print('ok', len(s), '->', len(t))
