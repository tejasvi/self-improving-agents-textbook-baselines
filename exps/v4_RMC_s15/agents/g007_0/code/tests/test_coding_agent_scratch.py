import os
from unittest import mock

import coding_agent


def _fake_chat_factory(prompts, scratch_seen):
    def fake_chat(msg, model=None, msg_history=None, logging=print):
        prompts.append(msg)
        history = list(msg_history or [])
        history.append({"role": "user", "content": msg})
        reply = "EXAMPLES_PASSED: yes" if "Final review step" in msg else "ok"
        history.append({"role": "assistant", "content": reply})
        return history
    return fake_chat


def _make_system(tmp_path):
    log = tmp_path / "log" / "chat.md"
    return coding_agent.AgenticSystem(
        problem_statement="Print the sum of two numbers.",
        git_tempdir=str(tmp_path / "repo"),
        base_commit="abc",
        chat_history_file=str(log),
    )


def test_scratch_dir_is_outside_repo_and_in_prompts(tmp_path):
    system = _make_system(tmp_path)
    prompts = []
    seen_dirs = []

    def fake_mkdtemp(prefix=""):
        d = str(tmp_path / f"{prefix}fixed")
        os.makedirs(d)
        seen_dirs.append(d)
        return d

    with mock.patch.object(coding_agent, "chat_with_agent", side_effect=_fake_chat_factory(prompts, None)), \
         mock.patch.object(coding_agent.tempfile, "mkdtemp", side_effect=fake_mkdtemp):
        _, passed = system.run_attempt()

    assert passed is True
    assert len(seen_dirs) == 1
    scratch = seen_dirs[0]
    # Scratch dir must not be inside the repository
    assert not scratch.startswith(system.git_tempdir)
    # Implementation, verification and review prompts all reference the scratch dir
    impl, verify, review = prompts[1], prompts[2], prompts[3]
    assert scratch in impl and "unit tests" in impl
    assert scratch in verify
    assert scratch in review
    # Scratch dir is removed after the attempt
    assert not os.path.exists(scratch)


def test_each_attempt_gets_fresh_scratch_dir(tmp_path):
    system = _make_system(tmp_path)
    prompts = []
    created = []

    def fake_mkdtemp(prefix=""):
        d = str(tmp_path / f"{prefix}{len(created)}")
        os.makedirs(d)
        created.append(d)
        return d

    with mock.patch.object(coding_agent, "chat_with_agent", side_effect=_fake_chat_factory(prompts, None)), \
         mock.patch.object(coding_agent.tempfile, "mkdtemp", side_effect=fake_mkdtemp), \
         mock.patch.object(coding_agent, "reset_to_commit"), \
         mock.patch.object(coding_agent, "apply_patch"), \
         mock.patch.object(coding_agent, "diff_versus_commit", return_value=""):
        system.forward(max_attempts=2)

    # Passing on the first attempt means exactly one scratch dir was used
    assert len(created) == 1
    assert all(not os.path.exists(d) for d in created)


def test_scratch_dir_cleaned_up_on_exception(tmp_path):
    system = _make_system(tmp_path)
    created = []

    def fake_mkdtemp(prefix=""):
        d = str(tmp_path / f"{prefix}err")
        os.makedirs(d)
        created.append(d)
        return d

    def boom(*a, **k):
        raise RuntimeError("llm failure")

    with mock.patch.object(coding_agent, "chat_with_agent", side_effect=boom), \
         mock.patch.object(coding_agent.tempfile, "mkdtemp", side_effect=fake_mkdtemp):
        try:
            system.run_attempt()
        except RuntimeError:
            pass
    assert created and not os.path.exists(created[0])
