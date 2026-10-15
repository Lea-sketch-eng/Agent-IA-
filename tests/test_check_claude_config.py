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


def test_agent_with_invalid_model_fails(tmp_path):
    agent = write(tmp_path / "a.md", "---\nname: a\ndescription: d\nmodel: opus-5.5\n---\n")
    with pytest.raises(ValueError, match="model"):
        check_agent(agent)


def test_agent_with_model_alias_or_id_and_effort_passes(tmp_path):
    for model in ("opus", "inherit", "claude-opus-5-5"):
        agent = write(
            tmp_path / "a.md", f"---\nname: a\ndescription: d\nmodel: {model}\neffort: xhigh\n---\n"
        )
        check_agent(agent)


def test_agent_with_invalid_effort_fails(tmp_path):
    agent = write(tmp_path / "a.md", "---\nname: a\ndescription: d\neffort: extreme\n---\n")
    with pytest.raises(ValueError, match="effort"):
        check_agent(agent)


def test_orchestrer_skill_is_user_invocable_only():
    from check_claude_config import ROOT, load_frontmatter

    skill = ROOT / "Agents" / "architect-orchestrator" / "skills" / "orchestrer" / "SKILL.md"
    assert load_frontmatter(skill).get("disable-model-invocation") is True


def test_agent_with_invalid_yaml_fails(tmp_path):
    content = "---\nname: a\ndescription: Lancer : uniquement sur demande\n---\n"
    agent = write(tmp_path / "a.md", content)
    with pytest.raises(ValueError, match="YAML invalide"):
        check_agent(agent)
