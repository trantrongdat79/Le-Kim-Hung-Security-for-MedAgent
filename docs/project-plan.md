# PROJECT PLAN

## 1. PROJECT CONTEXT

Context: Medical
Evaluation based on: MedAgentBench

Multi-agentic system: runnable and provide suggestion about medical

Atleast 3 Agents:
1. Input validation / clarify
2. Validation output
3. Decision

Must support memory and retreival

## 2. TECH STACK & REQUIREMENTS

Language: Python 3.9
Benchmark: MedAgentBench
Medical environment: FHIR server through Docker
LLM provider: OpenAI API 
Config format: YAML
Output format: JSON
Operating tools: terminal, Docker, Python virtual environment or Conda

## 3. DIRECTORY STRUCTURE

Le-Kim-Hung-Security-for-MedAgent/
├── README.md
├── docs/
│   ├── project-plan.md
│   └── medagentbench-understanding.md        # created after Sprint 1
├── MedAgentBench/
│   ├── README.md
│   ├── configs/
│   ├── data/
│   ├── src/
│   └── outputs/                              # generated benchmark results
├── scripts/
│   └── run_medagentbench_baseline.sh          # optional, maybe later
├── .env.example                               # optional, for API key template
└── .gitignore

## 4. EXECUTION PLAN (SPRINTS)

### Sprint 1: Reproduce MedAgentBench Baseline

Objective: Run the original MedAgentBench benchmark without modifying its core logic, using our own API key and one baseline model.

Expected work:
- Read MedAgentBench README and configs.
- Set up Python environment.
- Install dependencies.
- Start Docker FHIR server.
- Configure one API-backed LLM agent.
- Run agent connectivity test.
- Start task controller and task workers.
- Run a small benchmark subset.
- Collect output files.
- Write documentation about how MedAgentBench works.

Expected output:
- A working local MedAgentBench setup.
- At least one successful benchmark run.
- Baseline result files in MedAgentBench/outputs/.
- A document: docs/medagentbench-understanding.md

The understanding document should answer:
- What is MedAgentBench?
- What role does it play in our project?
- How does the benchmark interact with an agent?
- What are GET / POST / FINISH actions?
- Where are benchmark tasks stored?
- Where are FHIR function definitions stored?
- Where are results saved?
- What problems did we encounter while running it?
- Where can we plug in our future multi-agent system?

### Other sprints (placeholders)
- Sprint 2: Design and implement a custom 3-agent wrapper.
- Sprint 3: Add memory and retrieval.
- Sprint 4: Evaluate the multi-agent system on MedAgentBench and compare with baseline.
- Sprint 5: Clean documentation, report, and demo.