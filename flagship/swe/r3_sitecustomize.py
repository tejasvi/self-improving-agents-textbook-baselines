# sitecustomize for the flagship venv on the SWE machine (PREREG_v3 E1, 2026-10-25): the machine has no internet egress, so GET
# requests to raw.githubusercontent.com (swebench's test-spec code reads requirement files there) are answered from
# flagship/swe/raw_github_cache.json, fetched once on a machine with internet (same URLs, same status codes and bodies).
# Every other request goes through unchanged. Unknown raw.githubusercontent.com URLs fail loudly.
import json as _json, os as _os
_P = _os.path.expanduser('~/shi_eval/flagship/swe/raw_github_cache.json')
try:
    import requests as _rq
    _orig_get = _rq.get
    _cache = _json.load(open(_P)) if _os.path.exists(_P) else {}
    class _CachedResponse:
        def __init__(self, url, code, text):
            self.url = url; self.status_code = code; self.text = text; self.ok = code == 200
            self.content = text.encode()
    def _get(url, *args, **kwargs):
        if isinstance(url, str) and url.startswith('https://raw.githubusercontent.com/'):
            if url not in _cache:
                raise RuntimeError(f'raw GitHub URL not in offline cache: {url}')
            code, text = _cache[url]
            return _CachedResponse(url, code, text)
        return _orig_get(url, *args, **kwargs)
    _rq.get = _get
except ImportError:
    pass
