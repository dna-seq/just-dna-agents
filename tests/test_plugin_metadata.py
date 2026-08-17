"""Smoke tests for the distributable Claude Code and Codex plugin surfaces."""

import json
from pathlib import Path

from conftest import REPO_ROOT


def _read_json(path: Path) -> dict[str, object]:
    return json.loads(path.read_text())


def test_claude_plugin_declares_all_runtime_components() -> None:
    manifest = _read_json(REPO_ROOT / ".claude-plugin" / "plugin.json")

    assert manifest["name"] == "just-dna-agents"
    assert manifest["skills"] == "./skills/"
    assert manifest["agents"] == [
        "./.claude/agents/module-creator.md",
        "./.claude/agents/paper-scout.md",
        "./.claude/agents/pgs-module-creator.md",
        "./.claude/agents/pgx-module-creator.md",
        "./.claude/agents/researcher.md",
        "./.claude/agents/reviewer.md",
    ]
    assert manifest["commands"] == "./commands/"
    assert manifest["mcpServers"] == "./.claude-plugin/mcp.json"


def test_plugin_mcp_config_uses_published_runtime() -> None:
    config = _read_json(REPO_ROOT / ".claude-plugin" / "mcp.json")
    servers = config["mcpServers"]

    assert isinstance(servers, dict)
    annotation_server = servers["just-dna-agents-mcp"]
    assert annotation_server["command"] == "uvx"
    assert annotation_server["args"] == [
        "just-dna-agents-mcp@0.4.0",
        "serve",
        "--transport",
        "stdio",
    ]
    assert servers["biocontext-kb"]["url"] == "https://biocontext-kb.fastmcp.app/mcp"


def test_plugin_command_and_skill_files_are_present() -> None:
    commands = {
        path.stem
        for path in (REPO_ROOT / "commands").glob("*.md")
    }

    assert {
        "paper-scout",
        "create-module",
        "create-pgs-module",
        "create-pgx-module",
    } <= commands
    assert (REPO_ROOT / "skills" / "module-authoring" / "SKILL.md").is_file()
    assert (REPO_ROOT / "skills" / "create-module" / "SKILL.md").is_file()
    assert (REPO_ROOT / "skills" / "create-module" / "agents" / "openai.yaml").is_file()


def test_codex_plugin_declares_skills_and_published_runtime() -> None:
    manifest = _read_json(REPO_ROOT / ".codex-plugin" / "plugin.json")
    claude_manifest = _read_json(REPO_ROOT / ".claude-plugin" / "plugin.json")

    assert manifest["name"] == "just-dna-agents"
    assert manifest["version"] == claude_manifest["version"]
    assert manifest["skills"] == "./skills/"

    servers = manifest["mcpServers"]
    assert isinstance(servers, dict)
    annotation_server = servers["just-dna-agents-mcp"]
    assert annotation_server["type"] == "stdio"
    assert annotation_server["args"][0] == f"just-dna-agents-mcp@{manifest['version']}"
    assert servers["biocontext-kb"] == {
        "type": "streamable-http",
        "url": "https://biocontext-kb.fastmcp.app/mcp",
    }
