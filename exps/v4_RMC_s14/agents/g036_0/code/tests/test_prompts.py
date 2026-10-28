import os
import subprocess
import coding_agent
from coding_agent import AgenticSystem


def _make_repo(tmp_path):
    repo = tmp_path / "repo"
    repo.mkdir()
    subprocess.run(["git", "init", "-q", str(repo)], check=True)
    subprocess.run(["git", "-C", str(repo), "-c", "user.email=a@b", "-c", "user.name=t",
                    "commit", "-q", "--allow-empty", "-m", "init"], check=True)
    commit = subprocess.run(["git", "-C", str(repo), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=True).stdout.strip()
    return str(repo), commit


def test_prompts_require_restating_io_and_constraints(tmp_path, monkeypatch):
    repo, commit = _make_repo(tmp_path)
    calls = []

    def fake_chat(instruction, model=None, msg_history=None, logging=None):
        calls.append(instruction)
        return list(msg_history or []) + [{"role": "assistant", "content": "ok"}]

    monkeypatch.setattr(coding_agent, "chat_with_agent", fake_chat)
    agent = AgenticSystem(
        problem_statement="Sum two numbers.",
        git_tempdir=repo,
        base_commit=commit,
        chat_history_file=str(tmp_path / "log" / "chat.md"),
    )
    agent.forward()

    analysis, implementation = calls[0], calls[1]
    assert "Restate the input and output format" in analysis
    assert "list every constraint" in analysis
    assert "re-state the input and output format and the constraints" in implementation
    # Numbering stays consecutive in the analysis list.
    for n in range(1, 7):
        assert f"\n{n}. " in analysis


def test_final_review_phase_rereads_problem_and_checks_edge_cases(tmp_path, monkeypatch):
    repo, commit = _make_repo(tmp_path)
    calls = []

    def fake_chat(instruction, model=None, msg_history=None, logging=None):
        calls.append(instruction)
        return list(msg_history or []) + [{"role": "assistant", "content": "ok"}]

    monkeypatch.setattr(coding_agent, "chat_with_agent", fake_chat)
    agent = AgenticSystem(
        problem_statement="Sum two numbers.",
        git_tempdir=repo,
        base_commit=commit,
        chat_history_file=str(tmp_path / "log" / "chat.md"),
    )
    agent.forward()

    # analysis, implementation, review
    assert len(calls) == 3
    review = calls[2]
    assert "FINAL REVIEW phase" in review
    assert "Re-read the <problem_description>" in review
    assert "Sum two numbers." in review
    assert "Enumerate the edge cases" in review
    assert "Re-run all tests" in review
    for n in range(1, 8):
        assert f"\n{n}. " in review
