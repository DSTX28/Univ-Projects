# Wildfire intervention study: controlled Monte Carlo experiments and AI-agent evaluation

**Texas State University · CADS "How to Build Agents for Research" workshop · October 2026**
Simulator and agent tools: workshop materials by **Aniruddha Bora**. Experiments, analysis and report: Daniel Shaheen.

**Question:** a fire starts west of a river; a town of 36 structures sits east of it. A crew can close **at
most two** of the three river crossings before the fire arrives. Which two, and how sure are we?

## Experimental design
- Probabilistic cellular-automaton fire model (Alexandridis et al. 2008 style), 48 × 72 one-hectare cells, with
  wind, slope, fuel dryness and ember spotting
- **100 Monte Carlo runs per condition** with a **fixed random seed** across conditions, so every option sees the
  same 100 fires and differences come from the intervention, not the noise
- Factors swept one at a time: wind direction (8), wind speed (2–12 m/s), dryness (0.6–1.3), and all
  7 permitted crossing-closure combinations
- Uncertainty on proportions reported with Wilson 95 % intervals

## Key results ([full table](RESULTS.md))

| Crossings closed | Mean structures lost (of 36) |
|---|---:|
| none (baseline) | 31.6 |
| north | 31.4 |
| south | 29.3 |
| middle | 12.6 |
| north + middle | 12.2 |
| north + south | 29.4 |
| **middle + south** | **1.9** |

- **Best plan: close middle + south**, a 94 % reduction in structures lost. Neither crossing alone comes close
  (south alone barely helps), so the effect depends on closing both together.
- Baseline: the fire reaches town in 96 of 100 runs (95 % CI 0.90–0.98).
- **Dryness dominates:** closing the middle crossing cuts losses to 0 % of baseline at dryness 0.6, but only to
  97 % of baseline at 1.3. The same intervention can be decisive or useless depending on conditions.

## Evaluating an AI agent's reasoning
The workshop's second half used an LLM agent (Qwen 2.5 7B via Ollama) that calls the simulator through narrow
tools, with the two-crossing limit enforced **inside** the tool rather than by prompt instructions. I critiqued a
supplied agent trace that reached a confident recommendation from a flawed experiment: it compared only 4 of 7
options, used 10 runs instead of 100, and changed seeds between options, so its comparison wasn't controlled.

**Status:** the 10-run agent reliability experiment (Exercise 6) is set up in the notebook but hasn't been run
yet, so no agent success rate is reported here.

## Files
| File | Description |
|---|---|
| [`technical-report.pdf`](technical-report.pdf) | 3-page technical report: method, results, limitations |
| [`RESULTS.md`](RESULTS.md) | All numerical results, Exercises 0–5 |
| [`wildfire_assignment.ipynb`](wildfire_assignment.ipynb) | Colab notebook (exercises and agent harness) |
| [`fire_sim.py`](fire_sim.py), [`agent_tools.py`](agent_tools.py) | Workshop simulator and agent tool layer |

<details>
<summary>Running the agent in Google Colab</summary>

1. Upload the notebook, `fire_sim.py` and `agent_tools.py` to Colab (T4 GPU runtime recommended).
2. Install and start Ollama: `!curl -fsSL https://ollama.com/install.sh | sh`, then start `ollama serve` in a background subprocess.
3. `!ollama pull qwen2.5:7b-instruct` (~4.7 GB).
4. Run the agent setup cells in order, then set `RUN_AGENT = True`.

The text-based code guard is an educational safeguard, not a security boundary: run generated code only in an isolated environment.
</details>

*Illustrative model for research education; not for real wildfire response decisions.*
