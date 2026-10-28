"""Run a command inside an unprivileged bubblewrap sandbox (no network, minimal filesystem).

Only explicitly bound paths are visible. If `sock` is given, the host LLM proxy socket is bound at
/run/llm.sock and an in-sandbox forwarder serves it at http://127.0.0.1:8080.
"""
import os, subprocess, signal, time

SHI = os.path.expanduser('~/shi_eval')
AGENTENV = os.path.join(SHI, 'agentenv')
FWD = os.path.join(SHI, 'infra', 'sbx_fwd.py')
BASE_RO = ['/usr', '/lib', '/lib64', '/bin', '/sbin', '/etc/alternatives', '/etc/ld.so.cache', '/etc/ld.so.conf',
           '/etc/ld.so.conf.d', '/etc/localtime', '/etc/ssl', '/etc/mime.types']

def run(cmd, *, rw=(), ro=(), sock=None, env=None, timeout=600, mem_gb=4, cwd='/work', stdin_data=None,
        stdout_path=None, nice=15):
    """cmd: list. rw/ro: iterables of (host_path, sandbox_path). Returns dict(rc, out, err, timed_out, secs)."""
    a = ['bwrap', '--unshare-all', '--die-with-parent', '--new-session', '--cap-drop', 'ALL',
         '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--tmpfs', '/run', '--dir', '/work']
    for p in BASE_RO:
        if os.path.exists(p): a += ['--ro-bind', p, p]
    a += ['--ro-bind', AGENTENV, AGENTENV]
    for h, s in ro: a += ['--ro-bind', h, s]
    for h, s in rw: a += ['--bind', h, s]
    e = {'PATH': f'{AGENTENV}/bin:/usr/local/bin:/usr/bin:/bin', 'HOME': '/tmp', 'LANG': 'C.UTF-8',
         'PYTHONDONTWRITEBYTECODE': '1', 'OMP_NUM_THREADS': '1', 'OPENBLAS_NUM_THREADS': '1', 'MKL_NUM_THREADS': '1',
         'GIT_CONFIG_NOSYSTEM': '1', 'GIT_AUTHOR_NAME': 'agent', 'GIT_AUTHOR_EMAIL': 'agent@local',
         'GIT_COMMITTER_NAME': 'agent', 'GIT_COMMITTER_EMAIL': 'agent@local'}
    if env: e.update(env)
    a += ['--clearenv']
    for k, v in e.items(): a += ['--setenv', k, str(v)]
    a += ['--chdir', cwd]
    if sock:
        a += ['--ro-bind', FWD, '/opt/sbx_fwd.py', '--bind', sock, '/run/llm.sock']
        inner = ['/bin/sh', '-c', 'python3 /opt/sbx_fwd.py 8080 /run/llm.sock & i=0; while [ $i -lt 50 ]; do '
                 'python3 -c "import socket;s=socket.socket();s.connect((\'127.0.0.1\',8080))" 2>/dev/null && break; '
                 'i=$((i+1)); sleep 0.05; done; "$@"; rc=$?; kill %1 2>/dev/null; exit $rc', 'sh'] + list(cmd)
    else:
        inner = list(cmd)
    full = ['nice', '-n', str(nice), 'prlimit', f'--as={int(mem_gb * 2**30)}', '--'] + a + inner
    t0 = time.time()
    out_f = open(stdout_path, 'wb') if stdout_path else subprocess.PIPE
    p = subprocess.Popen(full, stdin=subprocess.PIPE if stdin_data is not None else subprocess.DEVNULL,
                         stdout=out_f, stderr=subprocess.PIPE, start_new_session=True)
    timed_out = False
    try:
        out, err = p.communicate(input=stdin_data, timeout=timeout)
    except subprocess.TimeoutExpired:
        timed_out = True
        try: os.killpg(p.pid, signal.SIGKILL)   # process group we created (start_new_session)
        except ProcessLookupError: pass
        out, err = p.communicate()
    if stdout_path: out_f.close(); out = b''
    return {'rc': p.returncode, 'out': out, 'err': err, 'timed_out': timed_out, 'secs': time.time() - t0}
