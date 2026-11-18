# I Feel You: How Developers' Emotions Affect the Fairness of Coding Agents

This repository contains the online appendix of the Registered Report *"I Feel You: How Developers' Emotions Affect the Fairness of Coding Agents"*, submitted to the Registered Reports track of **MSR 2027**. The study investigates whether the emotions developers express when asking for debugging assistance affect the fairness of coding agents, whether they lead agents to exhibit **empathetic sycophancy**, and whether a fairness-aware multi-agent pipeline can refine unfair responses.

---
## 📂 Repository Structure

Upon completion of the study, the repository will be organized as follows:
```
.
├── 🗂️ datasets/
├── 💬 prompts/
├── ⚙️ data_preparation/
├── 📝 requests/
├── ✍️ annotations/
├── 📊 results/
├── 📈 analysis/
└── 📄 README.md
```

### 🗂️ datasets/
Will contain the datasets used in the study.
- `codechat/` — the CodeChat conversations.
- `benchmark/` — the faulty files of the selected post-cutoff bugs.

### 💬 prompts/
Will contain the prompts of the LLM-based components.
- Prompt of the Analyzer.
- Prompt of the LLMJudge.
- Prompt of the LLMRefiner.

### ⚙️ data_preparation/
Contains the scripts used to prepare the data.

### 📝 requests/
Will contain the neutral requests and their emotional variants submitted to the LLMUser.

### ✍️ annotations/
Will contain the manual annotations used to validate the Analyzer, the LLMJudge, and the refined responses.

### 📊 results/
Will contain the Analyzer outputs, extracted emotional expressions, LLMUser responses, LLMJudge evaluations, and refined responses.

### 📈 analysis/
Will contain the scripts used to answer the research questions.

---