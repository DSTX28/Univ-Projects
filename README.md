# Wildfire AI Agent — Research Workshop Project

A reproducible Python simulation and AI-agent evaluation exercise based on the **CADS / Texas State University “How to Build Agents for Research” workshop** (October 2026). Original workshop materials credit Aniruddha Bora. This repository adapts the workshop-provided code for learning and demonstration; the wildfire model is illustrative, not a real-world operational forecasting system.

## What this project demonstrates

- Probabilistic wildfire simulation on a 48 × 72 landscape with 36 town structures.
- Comparing wind direction, wind speed, dryness, and river-crossing interventions.
- Checking model recommendations with independent numerical tests.
- An agent-loop design with tools, traces, and guardrails (requires a configured LLM).

## Files

- `wildfire_assignment.ipynb`: Colab notebook containing all seven exercises, completed numerical check code, and prepared agent prompts.
- `fire_sim.py`: Workshop wildfire simulator.
- `agent_tools.py`: Narrow tools exposed to the research agent.
- `RESULTS.md`: Independently computed experiment results.
- `requirements.txt`: Python dependencies.

## Run in Google Colab

1. Upload `wildfire_assignment.ipynb` using **Upload notebook**.
2. In the Colab **Files** sidebar, upload `fire_sim.py` and `agent_tools.py` to the working directory.
3. Connect a Python runtime and run the cells in order. Independent checks run without an LLM.
4. To run the **agent** sections, configure a reachable Ollama-compatible API endpoint, then set `RUN_AGENT = True` in the relevant cells. The default `localhost:11434` endpoint will not connect to an Ollama installation on your laptop from hosted Colab.

## Status and limitations

**Verified:** numerical simulation checks for Exercises 0–4 and critical reading of the supplied flawed trace in Exercise 5.

**Not verified:** actual agent answers and traces for Exercises 1–4, and the 10-agent-run reliability experiment in Exercise 6. The notebook deliberately marks these as pending. Do not describe this as a fully completed AI-agent evaluation until those runs are executed and checked.

The example agent uses generated Python and a basic text-based guard, which is **not a security boundary**. Only run trusted code in an isolated environment.

## Attribution

Workshop source code and exercise: *How to Build Agents for Research*, CADS, Texas State University, Aniruddha Bora, October 2026.

## Technical project report and résumé summary

See [Wildfire AI Agent Technical Report (PDF)](Wildfire_AI_Agent_Technical_Report.pdf) for objectives, methodology, benchmark results, limitations, and résumé-ready bullets. The PDF is a report of independently checked simulations, **not** a claim that the live AI agent or repeated reliability trials have been run.

## Running Exercise 6 in Google Colab

1. Upload `wildfire_assignment.ipynb`, `fire_sim.py`, and `agent_tools.py` to the same Colab runtime.
2. Run the **Google Colab model setup** cell; it installs Ollama and downloads `qwen2.5:7b-instruct` into the Colab runtime.
3. Run notebook cells in order through Exercise 3.
4. Run Exercise 6 to collect ten **real** independent model runs and save `exercise6_results.json` and trace files.
5. Replace the Exercise 6 placeholder with the printed observed result. Do not claim agent success until the runs complete.

**Status:** Exercise 6 implementation is ready but its ten agent outcomes have not been executed or measured in this delivered archive.
