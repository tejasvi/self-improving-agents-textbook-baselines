"""Translate Anthropic Messages API requests to Gemini / OpenAI-compatible (Vertex MaaS) backends and back.

Used by the proxy so that unmodified harnesses (which speak the Anthropic API) can run on other model
families for the transfer experiments. One tool call per response is kept (as with the Claude shim).
"""
import json, uuid, threading, time
import requests
import google.auth, google.auth.transport.requests
from google import genai
from google.genai import types

PROJECT = '__CLOUD_PROJECT__'
_lock = threading.Lock()
_sig_cache = {}          # tool_use id -> gemini thought signature (bytes)
_gclient = None
_cred = {'c': None, 'exp': 0}

PRICES = {  # USD per MTok (input, output) for accounting
    'gemini-2.5-flash': (0.30, 2.50), 'gemini-2.5-flash-lite': (0.10, 0.40), 'gemini-3-flash-preview': (0.50, 3.00),
    'openai/gpt-oss-120b-maas': (0.15, 0.60),
}

def gclient():
    global _gclient
    with _lock:
        if _gclient is None:
            _gclient = genai.Client(vertexai=True, project=PROJECT, location='global')
        return _gclient

def access_token():
    with _lock:
        if _cred['c'] is None or time.time() > _cred['exp']:
            c, _ = google.auth.default(scopes=['https://www.googleapis.com/auth/cloud-platform'])
            c.refresh(google.auth.transport.requests.Request())
            _cred['c'] = c; _cred['exp'] = time.time() + 1800
        return _cred['c'].token

def _blocks(content):
    if isinstance(content, str): return [{'type': 'text', 'text': content}]
    return content or []

def _tool_result_text(b):
    c = b.get('content')
    if isinstance(c, list): c = '\n'.join(x.get('text', '') for x in c if isinstance(x, dict))
    return '' if c is None else str(c)

def _clean_schema(s):
    if isinstance(s, dict):
        return {k: _clean_schema(v) for k, v in s.items() if k not in ('additionalProperties', '$schema', 'strict')}
    if isinstance(s, list): return [_clean_schema(x) for x in s]
    return s

def _system_text(system):
    if isinstance(system, list): return '\n'.join(x.get('text', '') for x in system if isinstance(x, dict))
    return system or None

# ---------------- Gemini ----------------
def gemini_call(model, req):
    names = {}
    contents = []
    for m in req.get('messages', []):
        parts = []
        for b in _blocks(m.get('content')):
            t = b.get('type')
            if t == 'text' and b.get('text'):
                parts.append(types.Part(text=b['text']))
            elif t == 'tool_use':
                names[b['id']] = b['name']
                kw = {'function_call': types.FunctionCall(name=b['name'], args=b.get('input') or {})}
                sig = _sig_cache.get(b['id'])
                if sig: kw['thought_signature'] = sig
                parts.append(types.Part(**kw))
            elif t == 'tool_result':
                parts.append(types.Part(function_response=types.FunctionResponse(
                    name=names.get(b.get('tool_use_id'), 'tool'), response={'result': _tool_result_text(b)})))
        if not parts: parts = [types.Part(text='(empty)')]
        contents.append(types.Content(role='model' if m['role'] == 'assistant' else 'user', parts=parts))
    cfg = dict(max_output_tokens=int(req.get('max_tokens', 4096)))
    st = _system_text(req.get('system'))
    if st: cfg['system_instruction'] = st
    if req.get('tools'):
        cfg['tools'] = [types.Tool(function_declarations=[types.FunctionDeclaration(
            name=t['name'], description=t.get('description', ''), parameters=_clean_schema(t.get('input_schema')))
            for t in req['tools']])]
        cfg['automatic_function_calling'] = types.AutomaticFunctionCallingConfig(disable=True)
    r = gclient().models.generate_content(model=model, contents=contents, config=types.GenerateContentConfig(**cfg))
    cand = (r.candidates or [None])[0]
    out, stop = [], 'end_turn'
    if cand is not None and cand.content and cand.content.parts:
        for p in cand.content.parts:
            if getattr(p, 'thought', False): continue
            if p.function_call and not any(b['type'] == 'tool_use' for b in out):
                tid = 'toolu_gem_' + uuid.uuid4().hex[:20]
                if getattr(p, 'thought_signature', None): _sig_cache[tid] = p.thought_signature
                out.append({'type': 'tool_use', 'id': tid, 'name': p.function_call.name, 'input': dict(p.function_call.args or {})})
            elif p.text and not p.function_call:
                out.append({'type': 'text', 'text': p.text})
    if any(b['type'] == 'tool_use' for b in out): stop = 'tool_use'
    elif cand is not None and str(getattr(cand, 'finish_reason', '')).endswith('MAX_TOKENS'): stop = 'max_tokens'
    if not out: out = [{'type': 'text', 'text': ''}]
    u = r.usage_metadata
    usage = {'input_tokens': (u.prompt_token_count or 0) if u else 0,
             'output_tokens': ((u.candidates_token_count or 0) + (u.thoughts_token_count or 0)) if u else 0}
    return {'id': 'msg_gem_' + uuid.uuid4().hex[:16], 'type': 'message', 'role': 'assistant', 'model': model,
            'content': out, 'stop_reason': stop, 'stop_sequence': None, 'usage': usage}

# ---------------- OpenAI-compatible (Vertex MaaS) ----------------
def openai_call(model, req):
    msgs = []
    st = _system_text(req.get('system'))
    if st: msgs.append({'role': 'system', 'content': st})
    for m in req.get('messages', []):
        bl = _blocks(m.get('content'))
        if m['role'] == 'assistant':
            text = '\n'.join(b.get('text', '') for b in bl if b.get('type') == 'text') or None
            calls = [{'id': b['id'], 'type': 'function', 'function': {'name': b['name'], 'arguments': json.dumps(b.get('input') or {})}}
                     for b in bl if b.get('type') == 'tool_use']
            msg = {'role': 'assistant', 'content': text}
            if calls: msg['tool_calls'] = calls
            msgs.append(msg)
        else:
            texts = [b.get('text', '') for b in bl if b.get('type') == 'text']
            for b in bl:
                if b.get('type') == 'tool_result':
                    msgs.append({'role': 'tool', 'tool_call_id': b.get('tool_use_id'), 'content': _tool_result_text(b)})
            if texts: msgs.append({'role': 'user', 'content': '\n'.join(texts)})
    body = {'model': model, 'messages': msgs, 'max_tokens': int(req.get('max_tokens', 4096))}
    if req.get('tools'):
        body['tools'] = [{'type': 'function', 'function': {'name': t['name'], 'description': t.get('description', ''),
                                                           'parameters': _clean_schema(t.get('input_schema'))}} for t in req['tools']]
        body['tool_choice'] = 'auto'; body['parallel_tool_calls'] = False
    url = f'https://aiplatform.googleapis.com/v1/projects/{PROJECT}/locations/global/endpoints/openapi/chat/completions'
    resp = requests.post(url, json=body, headers={'Authorization': f'Bearer {access_token()}'}, timeout=600)
    if resp.status_code != 200:
        raise RuntimeError(f'HTTP {resp.status_code}: {resp.text[:400]}')
    d = resp.json()
    if isinstance(d, list): d = d[0]
    ch = d['choices'][0]; msg = ch['message']; out = []
    content = msg.get('content') or ''
    if not msg.get('tool_calls') and '<|call|>' in content:
        # provider-side parse failure: the model's native (harmony) tool call leaked into the text; recover it
        import re
        m = re.search(r'to=functions\.([A-Za-z0-9_]+).*?<\|message\|>(.*?)<\|call\|>', content, re.DOTALL)
        if m:
            msg['tool_calls'] = [{'id': 'call_' + uuid.uuid4().hex[:16], 'type': 'function',
                                  'function': {'name': m.group(1), 'arguments': m.group(2)}}]
            content = content[:content.find('<|start|>')] if '<|start|>' in content else ''
    if content.strip(): out.append({'type': 'text', 'text': content})
    for tc in (msg.get('tool_calls') or [])[:1]:
        try: args = json.loads(tc['function'].get('arguments') or '{}')
        except Exception: args = {'_raw': tc['function'].get('arguments')}
        out.append({'type': 'tool_use', 'id': tc.get('id') or 'call_' + uuid.uuid4().hex[:16], 'name': tc['function']['name'], 'input': args})
    stop = 'tool_use' if any(b['type'] == 'tool_use' for b in out) else ('max_tokens' if ch.get('finish_reason') == 'length' else 'end_turn')
    if not out: out = [{'type': 'text', 'text': ''}]
    u = d.get('usage') or {}
    return {'id': d.get('id', 'msg_oai'), 'type': 'message', 'role': 'assistant', 'model': model, 'content': out,
            'stop_reason': stop, 'stop_sequence': None,
            'usage': {'input_tokens': u.get('prompt_tokens', 0), 'output_tokens': u.get('completion_tokens', 0)}}

def call(model, req):
    if model.startswith('gemini'): return gemini_call(model, req)
    return openai_call(model, req)

def cost(model, usage):
    p = PRICES.get(model, (1.0, 5.0))
    return (usage.get('input_tokens', 0) * p[0] + usage.get('output_tokens', 0) * p[1]) / 1e6
