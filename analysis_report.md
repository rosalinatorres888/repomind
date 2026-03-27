# RepoMind Analysis: rosalinatorres888/repomind

## 1. Repository Overview

| Field | Value |
|-------|-------|
| **Repository** | rosalinatorres888/repomind |
| **Language**   | Python |
| **Stars**      | 0 |
| **Forks**      | 0 |
| **Open Issues**| 0 |
| **Description**| AI Codebase Intelligence System — analyze any GitHub repo for architecture, dependencies, complexity, security risks, and refactor suggestions |

## 2. Architecture Diagram

```mermaid
graph TD
    main_core["main / core"]
    tests["tests"]
    utils["utils"]
```

**Detected Layers:**

- **utils**: file_parser.py, __init__.py, github_client.py
- **tests**: test_dependency_analyzer.py, test_file_parser.py, test_complexity_analyzer.py, test_security_scanner.py, test_report_generator.py...
- **other**: architecture_mapper.py, complexity_analyzer.py, repo_loader.py, dependency_analyzer.py, __init__.py...

**Entry Points:** main.py

**AI Architecture Summary:**

ANTHROPIC_API_KEY not set — skipping AI insights.

## 3. Dependency Analysis

- **Total modules:** 22
- **Dependency edges:** 0
- **Circular dependency cycles:** 0

### Most Imported Modules

| Module | In-Degree |
|--------|-----------|
| `README.md` | 0 |
| `architecture_mapper.py` | 0 |
| `complexity_analyzer.py` | 0 |
| `repo_loader.py` | 0 |
| `dependency_analyzer.py` | 0 |
| `__init__.py` | 0 |
| `security_scanner.py` | 0 |
| `report_generator.py` | 0 |
| `main.py` | 0 |
| `ai_insights.py` | 0 |

### Dependency Adjacency List


## 4. Complexity Metrics

- **Files analyzed:** 21
- **High-complexity functions flagged:** 3

### Maintainability Index (per file)

| File | MI Score |
|------|----------|
| `complexity_analyzer.py` | 43.88 |
| `report_generator.py` | 43.89 |
| `test_report_generator.py` | 48.96 |
| `test_file_parser.py` | 49.3 |
| `test_security_scanner.py` | 49.46 |
| `test_complexity_analyzer.py` | 49.81 |
| `test_architecture_mapper.py` | 50.26 |
| `test_ai_insights.py` | 52.55 |
| `main.py` | 52.69 |
| `test_repo_loader.py` | 52.69 |
| `architecture_mapper.py` | 53.38 |
| `security_scanner.py` | 54.48 |
| `test_dependency_analyzer.py` | 60.19 |
| `test_main.py` | 60.79 |
| `test_github_client.py` | 60.88 |
| `github_client.py` | 64.11 |
| `repo_loader.py` | 64.93 |
| `dependency_analyzer.py` | 72.97 |
| `ai_insights.py` | 76.37 |
| `__init__.py` | 100.0 |
| `file_parser.py` | 100.0 |

### Flagged Functions

| File | Function | CC | Length | Nested Loops | Params | Reason |
|------|----------|----|--------|--------------|--------|--------|
| `report_generator.py` | `generate_report` | 31 | 188 | 1 | 2 | cyclomatic_complexity |
| `architecture_mapper.py` | `map_architecture` | 16 | 32 | 2 | 1 | cyclomatic_complexity |
| `file_parser.py` | `parse_file` | 11 | 41 | 1 | 1 | cyclomatic_complexity |

## 5. Security Risks

### Risky Imports

`subprocess`, `pickle`

### 🔴 Hardcoded Secrets

| File | Line | Severity | Description |
|------|------|----------|-------------|
| `test_security_scanner.py` | 8 | 🔴 HIGH | Hardcoded password |
| `test_security_scanner.py` | 9 | 🔴 HIGH | Hardcoded API key/secret |

### Additional Findings

| File | Line | Severity | Description |
|------|------|----------|-------------|
| `test_security_scanner.py` | 11 | 🟡 MEDIUM | Insecure HTTP call: "http://api.example.com/data" |
| `test_security_scanner.py` | 12 | 🟢 LOW | open() in write mode — verify file permissions |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/repomind/complexity_analyzer.py` | 81 | 🟢 LOW | Try, Except, Continue detected. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/repomind/security_scanner.py` | 4 | 🟢 LOW | Consider possible security implications associated with the subprocess module. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/repomind/security_scanner.py` | 80 | 🟢 LOW | Starting a process with a partial executable path |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/repomind/security_scanner.py` | 80 | 🟢 LOW | subprocess call - check for execution of untrusted input. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/repomind/security_scanner.py` | 108 | 🟢 LOW | Try, Except, Continue detected. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 41 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 42 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 43 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 44 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 55 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 62 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_ai_insights.py` | 63 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 9 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 16 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 23 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 29 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 37 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_architecture_mapper.py` | 38 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 22 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 29 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 36 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 44 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 46 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_complexity_analyzer.py` | 53 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_dependency_analyzer.py` | 12 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_dependency_analyzer.py` | 17 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_dependency_analyzer.py` | 26 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |
| `/var/folders/7d/38n8qyc974dfs9nc462v_ln40000gn/T/repomind_34_4uesf/tests/test_dependency_analyzer.py` | 31 | 🟢 LOW | Use of assert detected. The enclosed code will be removed when compiling to optimised byte code. |

## 6. Refactoring Suggestions

_Set `ANTHROPIC_API_KEY` to enable AI-powered refactor suggestions._

---
_Generated by [RepoMind](https://github.com/rosalinatorres888/repomind)_