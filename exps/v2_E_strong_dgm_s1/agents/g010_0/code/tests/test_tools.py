import os
from tools import bash, edit

def test_bash_runs_and_keeps_cwd(tmp_path):
    out = bash.tool_function(f"cd {tmp_path} && echo hello")
    assert "hello" in out
    out = bash.tool_function("pwd")
    assert str(tmp_path) in out

def test_bash_stdin_closed_and_timeout(tmp_path):
    out = bash.tool_function("python3 -c 'import sys; print(len(sys.stdin.read()))'")
    assert "0" in out
    out = bash.tool_function("sleep 5", timeout=1)
    assert "timed out" in out

def test_editor_create_view_replace_insert(tmp_path):
    f = str(tmp_path / "a.py")
    assert "written" in edit.tool_function("create", f, file_text="x = 1\ny = 2\n")
    assert "x = 1" in edit.tool_function("view", f)
    assert "Edited" in edit.tool_function("str_replace", f, old_str="y = 2", new_str="y = 3")
    assert "y = 3" in open(f).read()
    assert "Inserted" in edit.tool_function("insert", f, new_str="z = 0", insert_line=0)
    assert open(f).read().startswith("z = 0")
    assert "Error" in edit.tool_function("str_replace", f, old_str="missing", new_str="q")
