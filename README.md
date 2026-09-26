# Python-based-Enterprise-Zero-Trust-AI-Security-Gateway-API
Architected a Zero-Trust AI Security Gateway in Python and FastAPI to protect enterprise LLM applications against indirect prompt injections and data exfiltration.

## Overview
As enterprises rapidly adopt Large Language Models (LLMs) and Retrieval-Augmented Generation (RAG) pipelines, traditional security perimeters are no longer sufficient. Attackers are shifting from direct jailbreaks to Indirect Prompt Injections, hiding malicious instructions inside the external documents and websites that AI agents are instructed to read.

This project is a Stateful, Zero-Trust AI Security Gateway built with FastAPI and Python. It acts as a multi-layered firewall between the user, the core application LLM, and the internal network. Instead of relying solely on brittle keyword filters, this gateway implements a defense-in-depth pipeline utilizing local semantic vector-search (sentence-transformers), dual-LLM privilege separation, and active Canary Token egress monitoring.

Threats Mitigated (Aligned with OWASP GenAI LLM Top 10 2026):   
LLM01: Prompt Injection: Blocked via a latency-optimized, multi-tier input gate combining heuristic Regex filtering and cosine-similarity vector checks against known adversarial embeddings.
LLM02: Sensitive Information Disclosure (Data Exfiltration): Prevented via Canary Token injection. Synthetic tracking tokens are embedded into untrusted context windows; if the egress scanner detects the LLM attempting to output these tokens, the transaction is immediately blocked and flagged as an exfiltration attempt.
LLM03: Excessive Agency: Mitigated via a Dual-Agent Sandbox. A highly restricted "Router Agent" makes authorization decisions, while an isolated "Executor Agent" interacts with untrusted RAG data, ensuring a compromised agent cannot access internal APIs.

## Running the Streamlit Dashboard
Ensure your FastAPI app is running in one terminal:

uvicorn main:app --reload

In a second terminal, launch Streamlit:

streamlit run dashboard.py
