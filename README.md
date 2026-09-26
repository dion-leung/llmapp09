[README.md](https://github.com/user-attachments/files/32679525/README.md)
# LLM Application CI/CD and Evaluation Evidence

Repository: `dion-leung/llmapp09`

This repository demonstrates a containerised LLM application with automated CI/CD, security scanning, prompt evaluation, and LLM-as-a-judge testing using GitHub Actions.

## Pipeline status

[![LLM Multiroute CI](https://github.com/dion-leung/llmapp09/actions/workflows/llm-multiroute-ci.yml/badge.svg)](https://github.com/dion-leung/llmapp09/actions/workflows/llm-multiroute-ci.yml)
[![LLM Frontend Python CI](https://github.com/dion-leung/llmapp09/actions/workflows/llm-frontend-python-ci.yml/badge.svg)](https://github.com/dion-leung/llmapp09/actions/workflows/llm-frontend-python-ci.yml)
[![PromptFoo Tests](https://github.com/dion-leung/llmapp09/actions/workflows/promptfoo-tests-ci.yml/badge.svg)](https://github.com/dion-leung/llmapp09/actions/workflows/promptfoo-tests-ci.yml)
[![DeepEval Tests](https://github.com/dion-leung/llmapp09/actions/workflows/deepeval-tests-ci.yml/badge.svg)](https://github.com/dion-leung/llmapp09/actions/workflows/deepeval-tests-ci.yml)

## Verified evidence

The following successful GitHub Actions runs were verified on 26 September 2026.

| Pipeline | Result | Run ID | Commit | Evidence |
|---|---|---:|---|---|
| LLM Multiroute CI | ✅ Success | `36222506631` | `30a11251af056dde749f7a42f0f58ca70838e92d` | [View successful run](https://github.com/dion-leung/llmapp09/actions/runs/36222506631) |
| LLM Frontend Python CI | ✅ Success | `36222504789` | `30a11251af056dde749f7a42f0f58ca70838e92d` | [View successful run](https://github.com/dion-leung/llmapp09/actions/runs/36222504789) |
| PromptFoo Tests | ✅ Success | `36222683710` | `30a11251af056dde749f7a42f0f58ca70838e92d` | [View successful run](https://github.com/dion-leung/llmapp09/actions/runs/36222683710) |
| DeepEval Tests | ✅ Success | `36226212728` | `1c2248b9a65d588506ae0182d0f1214be5e49af3` | [View successful run](https://github.com/dion-leung/llmapp09/actions/runs/36226212728) |

At the time of verification, all four required pipelines had completed successfully.

## Solution structure

```text
llmapp09/
├── .github/
│   └── workflows/
│       ├── llm-multiroute-ci.yml
│       ├── llm-frontend-python-ci.yml
│       ├── promptfoo-tests-ci.yml
│       └── deepeval-tests-ci.yml
├── llm-multiroute/
├── llm-frontend-python/
├── llm-python/
├── promptfoo-tests/
├── deepeval-tests/
├── docker-compose.yml
└── .trivyignore
```

## 1. LLM Multiroute CI

Workflow: `.github/workflows/llm-multiroute-ci.yml`

Pipeline sequence:

```text
Ruff lint
   ↓
Pytest unit tests
   ↓
Docker image build
   ↓
Trivy vulnerability scan
   ↓
Docker Hub push
```

The workflow uses Python 3.12. The Docker image is scanned with Trivy before it is pushed. The scan is configured to fail the build on `HIGH` or `CRITICAL` vulnerabilities that are not explicitly documented in `.trivyignore`.

Docker image:

```text
dionleung/llm-multiroute
```

Evidence: [successful LLM Multiroute CI run](https://github.com/dion-leung/llmapp09/actions/runs/36222506631).

## 2. LLM Frontend Python CI

Workflow: `.github/workflows/llm-frontend-python-ci.yml`

Pipeline sequence:

```text
Ruff lint
   ↓
Docker image build
   ↓
Trivy vulnerability scan
   ↓
Docker Hub push
```

The frontend image follows the same security gate as the multiroute backend, with the Docker Hub push occurring only after the vulnerability scan succeeds.

Docker image:

```text
dionleung/llm-frontend-python
```

Evidence: [successful LLM Frontend Python CI run](https://github.com/dion-leung/llmapp09/actions/runs/36222504789).

## 3. PromptFoo evaluation

Workflow: `.github/workflows/promptfoo-tests-ci.yml`

The PromptFoo pipeline:

1. Starts the `llm-multiroute` backend using Docker Compose.
2. Waits until the backend is available at `http://localhost:8080/api/ai/routes`.
3. Executes PromptFoo evaluations for classification, sentiment, summarisation, and intent detection.
4. Tears down the backend after evaluation.

Evidence: [successful PromptFoo run](https://github.com/dion-leung/llmapp09/actions/runs/36222683710).

## 4. DeepEval evaluation

Workflow: `.github/workflows/deepeval-tests-ci.yml`

DeepEval performs LLM-based evaluation across the same four application capabilities:

```text
Classification
Sentiment
Summarisation
Intent detection
```

The current CI implementation uses a local Ollama judge on the GitHub Actions runner:

```text
qwen2.5:7b
```

The workflow installs Ollama, starts the local Ollama service, pulls the judge model, configures DeepEval to use it, starts the application backend, and executes all four DeepEval suites.

The successful run completed:

```text
DeepEval classify tests   ✅
DeepEval sentiment tests  ✅
DeepEval summarize tests  ✅
DeepEval intent tests     ✅
```

This configuration avoids dependency on paid OpenAI API inference for the DeepEval judge.

Evidence: [successful DeepEval run](https://github.com/dion-leung/llmapp09/actions/runs/36226212728).

## Security controls

The two application image pipelines contain a Trivy security gate.

Configuration:

```text
Severity checked: HIGH, CRITICAL
Failure behaviour: exit-code 1
Ignore file: .trivyignore
```

The Docker Hub login and image push occur only after the scan succeeds.

Secrets are stored using GitHub Actions repository secrets rather than being committed to source control. The workflows currently reference:

```text
DOCKERHUB_TOKEN
OLLAMA_API_KEY
OLLAMA_BASE_URL
```

Secret values are intentionally excluded from this repository and this README.

## Running the application

From the repository root:

```bash
docker compose up -d
```

To stop the services:

```bash
docker compose down
```

## Running the evaluation workflows manually

```bash
gh workflow run llm-multiroute-ci.yml --ref main
gh workflow run llm-frontend-python-ci.yml --ref main
gh workflow run promptfoo-tests-ci.yml --ref main
gh workflow run deepeval-tests-ci.yml --ref main
```

Check workflow status:

```bash
gh run list --limit 20
```

## Completion evidence

The repository demonstrates the following completed controls:

- automated source linting
- automated Python unit testing
- Docker image creation
- container vulnerability scanning using Trivy
- Docker Hub publishing after successful security checks
- PromptFoo evaluation of four LLM capabilities
- DeepEval LLM-as-a-judge evaluation of four LLM capabilities
- GitHub Actions orchestration
- repository-secret based credential management
- successful execution of all four required pipelines

### Final verified pipeline state

```text
LLM Multiroute CI        ✅ SUCCESS
LLM Frontend Python CI   ✅ SUCCESS
PromptFoo Tests          ✅ SUCCESS
DeepEval Tests           ✅ SUCCESS
```

Verification date: **26 September 2026**
