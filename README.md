# Le-Kim-Hung-Security-for-MedAgent


Context: Medical
Dataset: MedAgent Bench

Multi-agentic system: runnable and provide suggestion about medical

Atleast 3 Agent:
1. Input validation / clarify
2. Validation output
3. Decision

Must support memory and retreival

Evaluate on benchmark data

# Guide

Run simple test chat:
```bash
cd MedAgentBench
uv run python -m src.client.agent_test --config configs/agents/api_agents.local.yaml --agent deepseek-v4-flash
```
