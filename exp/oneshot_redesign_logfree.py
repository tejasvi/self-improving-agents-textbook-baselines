"""PREREG_v3 E3: one-shot redesign WITHOUT failure logs. Same model call as exp/oneshot_redesign_v2.py (agent summary,
the DGM seed's code, the same task paragraph), minus the section with the logs of five failed runs. No evaluation
feedback. Output: harness/redesign/<tag>_r<i>/ (seed copy + returned files), raw responses, prompt and manifest.
usage: oneshot_redesign_logfree.py MODEL TAG N"""
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import oneshot_redesign_v2 as O
import dgm_lcb, dgm_prompts as P

def prompt():
    return (P.coding_agent_summary_lcb +
            "\n# The agent's code\n\n" + O.code_dump(O.SEED) +
            "\n\n# Your task\n\nRevise this coding agent so that it solves as many hard problems of this kind as possible. "
            "You get no further feedback, so make the changes you are confident will help, and keep the agent working: "
            "coding_agent.py must keep its command-line interface, every tool must keep the tool_info()/tool_function() "
            "interface, and model names and API access (client creation, environment variables) must stay as they are. "
            "Return every file you change in full, each wrapped exactly as <file path=\"relative/path.py\">...</file>; "
            "files you do not return stay unchanged.")

def main(model, tag, n):
    user = prompt()
    out = os.path.join(O.SHI, 'harness', 'redesign'); os.makedirs(out, exist_ok=True)
    open(os.path.join(out, f'{tag}_prompt.txt'), 'w').write(user)
    man = {'model': model, 'logs': None, 'prompt_chars': len(user), 'samples': {}}
    for i in range(n):
        name = f'{tag}_r{i}'; dest = os.path.join(out, name)
        if os.path.exists(dest): continue
        raw = dgm_lcb.llm_text(model, 'You are an expert engineer of LLM-based coding agents.', user,
                               run=f'v3_E3|{tag}|{i}', budget=4.0, max_tokens=20000)
        open(os.path.join(out, f'{name}.raw.txt'), 'w').write(raw)
        written, bad = O.materialize(raw, dest)
        man['samples'][name] = {'written': written, 'compile_errors': bad, 'raw_chars': len(raw)}
        print(name, man['samples'][name], flush=True)
    json.dump(man, open(os.path.join(out, f'{tag}_manifest.json'), 'w'), indent=1)

if __name__ == '__main__':
    main(sys.argv[1], sys.argv[2], int(sys.argv[3]))
