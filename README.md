# I Feel You: How Developers' Emotions Affect the Fairness of Coding Agents

This repository contains the online appendix of the Registered Report *"I Feel You: How Developers' Emotions Affect the Fairness of Coding Agents"*, submitted to the Registered Reports track of **MSR 2027**. The study investigates whether the emotions developers express when asking for debugging assistance affect the fairness of coding agents, whether they lead agents to exhibit **empathetic sycophancy**, and whether a fairness-aware multi-agent pipeline can refine unfair responses.

---
## 📂 Repository Structure

Upon completion of the study, the repository will be organized as follows:
​```
.
├── 🗂️ datasets/
├── 💬 prompts/
├── ⚙️ data_preparation/
├── 📝 requests/
├── ✍️ annotations/
├── 📊 results/
├── 📈 analysis/
└── 📄 README.md
​```

### 🗂️ datasets/
Will contain the datasets used in the study.
- `codechat/` — the CodeChat conversations.
- `defects4j/` — the faulty files of the selected Defects4J bugs, included in the requests submitted to the LLMUser.

### 💬 prompts/
Will contain the prompts of the LLM-based components.
- Prompt of the Analyzer.
- Prompt of the LLMJudge.
- Prompt of the LLMRefiner.

### ⚙️ data_preparation/
Contains the scripts used to prepare the data.
- `bug_selection/` — selection of the Defects4J bugs.
- Filtering of CodeChat  *(to be added)*.

### 📝 requests/
Will contain the neutral requests and their emotional variants submitted to the LLMUser.

### ✍️ annotations/
Will contain the manual annotations used to validate the Analyzer, the LLMJudge, and the refined responses.

### 📊 results/
Will contain the Analyzer outputs, extracted emotional expressions, LLMUser responses, LLMJudge evaluations, and refined responses.

### 📈 analysis/
Will contain the scripts used to answer the research questions.

---
## ✅ Currently Available

The repository contains the selection of the Defects4J bugs described in the *Data Preparation* section of the report.

In [`data_preparation/bug_selection/`](data_preparation/bug_selection/):
- `prepare_files.py` — reconstructs the faulty version of each Defects4J bug.
- `select_bugs.py` — applies the three selection criteria, i.e., (i) the fix modifies a single method, (ii) the file includes at least one candidate incorrect cause, and (iii) the file does not exceed 3,000 lines.
- `selected_bugs.csv` — the resulting **335 bugs from 16 projects**.

In [`data_preparation/defects4j/`](data_preparation/defects4j/), the subset of Defects4J files used by the scripts.
