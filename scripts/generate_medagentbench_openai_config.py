#!/usr/bin/env python3
"""Generate local MedAgentBench OpenAI-compatible configs from env variables."""

from __future__ import annotations

import argparse
import os
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
MEDAGENTBENCH = ROOT / "MedAgentBench"
AGENT_CONFIG_DIR = MEDAGENTBENCH / "configs" / "agents"
ASSIGNMENT_CONFIG_DIR = MEDAGENTBENCH / "configs" / "assignments"


def load_dotenv(path: Path) -> None:
    if not path.exists():
        return

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        line = raw_line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue

        key, value = line.split("=", 1)
        key = key.strip()
        value = value.strip().strip('"').strip("'")
        os.environ.setdefault(key, value)


def get_env(*names: str, default: str = "") -> str:
    for name in names:
        value = os.environ.get(name, "").strip()
        if value:
            return value
    return default


def chat_completions_url(api_base: str) -> str:
    api_base = api_base.rstrip("/")
    if api_base.endswith("/chat/completions"):
        return api_base
    return f"{api_base}/chat/completions"


def write_file(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print(f"Wrote {path.relative_to(ROOT)}")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Generate local MedAgentBench configs for OpenAI-compatible APIs."
    )
    parser.add_argument(
        "--env-file",
        default=ROOT / ".env",
        type=Path,
        help="Path to .env file. Defaults to project .env.",
    )
    parser.add_argument(
        "--model",
        default=None,
        help="Override LLM_MODEL or OPENAI_MODEL for this generated config.",
    )
    args = parser.parse_args()

    load_dotenv(args.env_file)

    api_key = get_env("LLM_API_KEY", "DEEPSEEK_API_KEY", "OPENAI_API_KEY")
    if not api_key:
        raise SystemExit(
            "Missing API key. Add LLM_API_KEY, DEEPSEEK_API_KEY, or "
            "OPENAI_API_KEY to .env."
        )
    api_base = get_env("LLM_API_BASE", "OPENAI_API_BASE", default="https://api.openai.com/v1")
    model = args.model or get_env("LLM_MODEL", "OPENAI_MODEL", default="gpt-4o-mini")
    agent_name = get_env("LLM_AGENT_NAME", default=model)
    max_tokens = get_env("LLM_MAX_TOKENS", "OPENAI_MAX_TOKENS", default="2048")
    temperature = get_env("LLM_TEMPERATURE", "OPENAI_TEMPERATURE", default="0")
    url = chat_completions_url(api_base)

    openai_chat = f"""module: src.client.agents.HTTPAgent
parameters:
  url: {url}
  headers:
    Content-Type: application/json
    Authorization: Bearer {api_key}
  body:
    model: "{model}"
    temperature: {temperature}
    max_tokens: {max_tokens}
  prompter:
    name: role_content_dict
    args:
      agent_role: assistant
  return_format: "{{response[choices][0][message][content]}}"
"""

    api_agents = f"""{agent_name}:
    import: "./openai-chat.local.yaml"
    parameters:
        name: "{model}"
        body:
            model: "{model}"
"""

    assignment = f"""import: definition.yaml

definition:
  agent:
    import:
      - ../agents/api_agents.local.yaml
      - ../agents/fs_agent.yaml

concurrency:
  task:
    medagentbench-std: 1
  agent:
    {agent_name}: 1

assignments:
  - agent:
      - {agent_name}
    task:
      - medagentbench-std

output: "outputs/MedAgentBenchv1"
"""

    write_file(AGENT_CONFIG_DIR / "openai-chat.local.yaml", openai_chat)
    write_file(AGENT_CONFIG_DIR / "api_agents.local.yaml", api_agents)
    write_file(ASSIGNMENT_CONFIG_DIR / "baseline.local.yaml", assignment)

    print("\nNext:")
    print("  cd MedAgentBench")
    print(
        "  uv run python -m src.client.agent_test "
        f"--config configs/agents/api_agents.local.yaml --agent {agent_name}"
    )
    print(
        "  uv run python -m src.assigner "
        "--config configs/assignments/baseline.local.yaml"
    )


if __name__ == "__main__":
    main()
