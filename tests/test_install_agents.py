import subprocess
from pathlib import Path

INSTALL = Path(__file__).resolve().parent.parent / "Agents" / "install.sh"


def run(*args, home=None):
    env = {"PATH": "/usr/bin:/bin", "HOME": str(home or "/nonexistent")}
    return subprocess.run(["bash", str(INSTALL), *args], capture_output=True, text=True, env=env)


def test_install_in_project_copies_agents_and_skill(tmp_path):
    result = run("architect-orchestrator", str(tmp_path))
    assert result.returncode == 0, result.stderr
    agents = {p.name for p in (tmp_path / ".claude" / "agents").glob("*.md")}
    assert {"architect-orchestrator.md", "code-generator.md", "code-verifier.md"} <= agents
    assert (tmp_path / ".claude" / "skills" / "orchestrer" / "SKILL.md").is_file()


def test_install_global_uses_home(tmp_path):
    result = run("architect-orchestrator", "--global", home=tmp_path)
    assert result.returncode == 0, result.stderr
    assert (tmp_path / ".claude" / "agents" / "architect-orchestrator.md").is_file()


def test_unknown_agent_fails(tmp_path):
    result = run("inconnu", str(tmp_path))
    assert result.returncode == 1
    assert "Agent inconnu" in result.stderr
    assert not (tmp_path / ".claude").exists()
