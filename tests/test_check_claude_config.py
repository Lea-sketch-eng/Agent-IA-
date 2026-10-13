import pytest
from check_claude_config import check_agent, check_skill


def write(path, content):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    return path


def test_valid_agent_passes(tmp_path):
    agent = write(tmp_path / "a.md", "---\nname: a\ndescription: d\ntools: Read, Bash\n---\n")
    check_agent(agent)


def test_agent_without_frontmatter_fails(tmp_path):
    agent = write(tmp_path / "a.md", "Pas de frontmatter\n")
    with pytest.raises(ValueError, match="frontmatter"):
        check_agent(agent)


def test_agent_with_unknown_tool_fails(tmp_path):
    agent = write(tmp_path / "a.md", "---\nname: a\ndescription: d\ntools: Read, Foo\n---\n")
    with pytest.raises(ValueError, match="Foo"):
        check_agent(agent)


def test_agent_without_description_fails(tmp_path):
    agent = write(tmp_path / "a.md", "---\nname: a\n---\n")
    with pytest.raises(ValueError, match="description"):
        check_agent(agent)


def test_skill_name_must_match_folder(tmp_path):
    skill = write(tmp_path / "debug-test" / "SKILL.md", "---\nname: autre\ndescription: d\n---\n")
    with pytest.raises(ValueError, match="différent du dossier"):
        check_skill(skill)
