## Sprint 1: Reproduce MedAgentBench Baseline

### Step 1: Setup python environment

Update pyproject.toml to match the sprint goal
```
requires-python = ">=3.9,<3.10"
```

Pin uv to the correct Python version
```bash
uv python install 3.9
uv python pin 3.9
uv venv --python 3.9
uv pip install -r MedAgentBench/requirements.txt
```

### Setup the local config files

Create the env file contains the configs:
```bash
cp .env.example .env
```

Edit the config, setup your env. For example:
```bash
# OpenAI-compatible API settings.
LLM_API_BASE=https://api.deepseek.com
LLM_API_KEY=sk-your-key-here
LLM_MODEL=deepseek-v4-flash
LLM_MAX_TOKENS=2048
LLM_TEMPERATURE=0
```

Generate MedAgentBench local configs:
```bash
uv run python scripts/generate_medagentbench_openai_config.py
```

It will generate:
```bash
MedAgentBench/configs/agents/openai-chat.local.yaml
MedAgentBench/configs/agents/api_agents.local.yaml
MedAgentBench/configs/assignments/baseline.local.yaml
```

### Test the LLM API:
```bash
uv run python -m src.client.agent_test --config configs/agents/api_agents.local.yaml --agent deepseek-v4-flash
```
This checks whether MedAgentBench can call your model.

### Start FHIR Server
In another terminal:
```bash
docker pull jyxsu6/medagentbench:latest
docker tag jyxsu6/medagentbench:latest medagentbench
docker run -p 8080:8080 medagentbench
```
Then visit: ```http://localhost:8080/```

You may want to disable AirPlay Receiver to free port 5000 for med

### Add refsol.py
MedAgentBench needs this for official scoring:
```MedAgentBench/src/server/tasks/medagentbench/refsol.py```
The README of MedAgentBench links to the download.

### Start Task Workers

The assumption for this step is that ports from 5000 to 5015 are available. For Mac OS system, you may want to follow [here](https://stackoverflow.com/questions/69955686/why-cant-i-run-the-project-on-port-5000) to free port 5000 to use.

From MedAgentBench:
```bash
cd MedAgentBench
uv run python -m src.start_task -a
```
Wait until workers register successfully.

### Run Baseline Assignment
In another terminal, from MedAgentBench:
```bash
cd MedAgentBench
uv run python -m src.assigner --config configs/assignments/baseline.local.yaml
```
This uses concurrency 1 (based on the config file), which is good for Sprint 1 because it keeps cost and debugging pain low.