
# Daniel Shaheen

**Electrical Engineering Student | Texas State University**

## University Engineering Projects

This repository showcases engineering projects involving digital logic design, analog circuits, MATLAB, LTspice, Python, numerical simulations, and AI-agent research.

---

### 1. Digital Fuel Pump System – SystemVerilog

**Oklahoma State University (OSU) | ECEN 2233 – Fundamentals of Digital Logic Design**

#### Project Overview

Designed and simulated a digital fuel pump system using SystemVerilog. The system calculates fuel requirements based on distance and fuel efficiency, determines the total fuel cost, and displays the calculated result through four seven-segment displays.

#### Technical Skills

- SystemVerilog programming
- Digital logic design
- Binary arithmetic and cost calculations
- Seven-segment display control
- Modular hardware design
- Testbench development and waveform simulation

#### Project Documentation

The complete final lab report, including SystemVerilog code screenshots and simulation results, is available in this repository.

---

### 2. 4–20 mA Current Loop Voltage Conversion System – Circuits I

**Oklahoma State University (OSU) | ECEN 2714/2011 – Fundamentals of Electric Circuits Laboratory | Fall 2025**

#### Project Overview

Designed, simulated, built, and tested a current-to-voltage conversion circuit using an LM358 operational amplifier. The system converts an industrial 4–20 mA current signal into a nominal 0–5 V output using a feedback resistor and DC offset network.

#### Technical Skills

- Analog circuit design
- Operational amplifiers (LM358)
- Transimpedance amplifier design
- Circuit simulation
- Breadboard prototyping
- Digital multimeter measurements
- Circuit testing and troubleshooting
- Experimental data analysis

#### Project Documentation

The complete semester design project report, including circuit schematics, design calculations, simulation results, laboratory measurements, graphs, and breadboard photographs, is available in this repository.

---

### 3. Band-Pass Filter Frequency Response Analysis – MATLAB & LTspice

**Individual Engineering Project | Spring 2026**

#### Project Overview

Independently analyzed frequency response data and designed an active band-pass filter using MATLAB and LTspice. Estimated a transfer function, calculated frequency response characteristics, designed and simulated a filter circuit, and compared measured, theoretical, and simulated results.

#### Technical Skills

- MATLAB programming and data analysis
- LTspice circuit design and simulation
- Analog filter design
- Transfer function estimation
- Bode plot analysis
- Operational amplifier circuit design
- Gain, bandwidth, and cutoff frequency calculations
- Circuit simulation and troubleshooting
- IEEE-style technical report writing

#### Project Results

- Measured peak gain: 20.543 dB
- Designed passband gain: approximately 20 dB
- RMS magnitude error: 2.371 dB
- Compared measured, estimated, and simulated frequency responses

#### Project Documentation

The complete IEEE-style project report, including MATLAB code, LTspice circuit schematics, calculations, frequency response graphs, and simulation results, is available in this repository.

---

### 4. Wildfire AI Agent — Research Workshop Project

**Texas State University | CADS — How to Build Agents for Research Workshop | Fall 2026**

**Project Type:** AI-Agent Research, Python Simulation, and Experimental Evaluation

**Original Workshop Materials:** Aniruddha Bora

#### Project Overview

Developed an educational adaptation of a Python wildfire simulation and AI-agent evaluation project based on the CADS / Texas State University "How to Build Agents for Research" workshop in October 2026.

The project explores how AI agents can use Python tools to investigate wildfire behavior, evaluate interventions, and generate evidence-based recommendations.

The project combines:

- Probabilistic wildfire simulations
- Python-based numerical analysis
- AI-agent reasoning with tool calls
- Local large language models using Ollama
- Experimental comparisons using controlled random seeds
- Agent guardrails and execution traces
- Reliability testing across independent agent runs

**Disclaimer:** The wildfire simulator is illustrative and is not intended for real-world emergency forecasting or operational wildfire management.

#### Technical Skills Demonstrated

- Python programming
- Simulation and statistical analysis
- AI-agent development
- Large language model integration
- Google Colab
- Ollama and Qwen2.5
- API communication
- Automated experimentation
- JSON logging and trace analysis
- Research documentation

#### Simulation Environment

The wildfire simulation models a 48 × 72 landscape containing 36 town structures.

Experiments investigate how wildfire outcomes change with:

- Wind direction
- Wind speed
- Environmental dryness
- River-crossing closures
- Intervention combinations

Simulation results are compared using consistent random seeds and repeated trials.

#### Project Files

| File | Description |
|---|---|
| `wildfire_assignment.ipynb` | Main Google Colab notebook containing seven exercises |
| `fire_sim.py` | Wildfire simulation engine |
| `agent_tools.py` | Tools available to the AI agent |
| `RESULTS.md` | Independently computed numerical results |
| `requirements.txt` | Python dependencies |
| `Wildfire_AI_Agent_Technical_Report.pdf` | Technical report and experimental methodology |

Agent trace files and Exercise 6 results are generated when their corresponding experiments complete successfully.

#### AI Agent Architecture

The agent uses a tool-based reasoning loop:

1. Receive a research question.
2. Generate Python code to investigate the simulator.
3. Check the proposed code against defined restrictions.
4. Execute permitted simulation operations.
5. Return numerical results to the AI model.
6. Continue reasoning using the observed results.
7. Produce a final answer supported by simulation evidence.
8. Save the conversation and tool outputs as a JSON trace.

The implementation uses the `qwen2.5:7b-instruct` language model through Ollama.

The basic text-based code guard is an educational safeguard, not a complete security boundary. Generated code should only be executed in an isolated, trusted environment.

#### Running the Project in Google Colab

##### Step 1 — Upload Project Files

Open Google Colab and upload:

- `wildfire_assignment.ipynb`
- `fire_sim.py`
- `agent_tools.py`

Ensure the Python files are accessible from the notebook's working directory.

##### Step 2 — Configure Runtime

Select:

Runtime → Change runtime type

Recommended configuration:

- Runtime type: Python 3
- Hardware accelerator: T4 GPU, if available
- Runtime version: Latest recommended

A CPU runtime can also be used, although model inference may be slower.

##### Step 3 — Install Ollama

Run the following commands in a Colab code cell:

    !apt-get update -qq
    !apt-get install -y zstd
    !curl -fsSL https://ollama.com/install.sh -o /tmp/install_ollama.sh
    !bash /tmp/install_ollama.sh

##### Step 4 — Start Ollama Server

Run:

    import subprocess
    import time

    server = subprocess.Popen(
        ["ollama", "serve"],
        stdout=open("/tmp/ollama.log", "w"),
        stderr=subprocess.STDOUT
    )

    time.sleep(5)
    print("Ollama server startup attempted")

##### Step 5 — Verify Server Connection

Run:

    import urllib.request

    try:
        response = urllib.request.urlopen(
            "http://127.0.0.1:11434/api/tags",
            timeout=5
        )
        print("SUCCESS! Ollama server connected!")
        print(response.read().decode())
    except Exception as e:
        print("Connection failed:", e)

A successful connection confirms the Ollama API is reachable.

An empty model list means the server is running but no model has been downloaded.

##### Step 6 — Download the AI Model

Run:

    !ollama pull qwen2.5:7b-instruct

The model download is approximately 4.7 GB.

Verify installation:

    !ollama list

The output should include:

`qwen2.5:7b-instruct`

##### Step 7 — Initialize the AI Agent

Run the notebook's original agent setup cells in order.

These define the language-model interface, simulator tool execution, code guardrails, agent reasoning loop, and `ask()` function.

Verify the model responds to a test prompt before starting the agent exercises.

Where required, change:

`RUN_AGENT = False`

to:

`RUN_AGENT = True`

Only enable agent execution after confirming the model connection and required functions are working.

#### Exercises

##### Exercise 0 — Baseline Wildfire Simulation

Run 100 wildfire simulations to estimate average structural losses and the probability of the fire reaching town.

##### Exercise 1 — AI-Agent Investigation

Use the research agent to investigate wildfire behavior through permitted simulation tools.

##### Exercise 2 — Environmental Conditions

Compare how environmental conditions influence simulated wildfire outcomes.

##### Exercise 3 — River-Crossing Interventions

Evaluate seven permitted crossing-closure combinations using 100 simulations per option with the same random seed.

The crew can close at most two crossings.

**Independently computed results:**

| Crossing Closure | Mean Structures Lost |
|---|---:|
| None | 31.6 |
| North | 31.4 |
| Middle | 12.6 |
| South | 29.3 |
| North + Middle | 12.2 |
| North + South | 29.4 |
| Middle + South | 1.9 |

**Best independently verified intervention: Middle + South**

This combination reduces mean structural losses from 31.6 to 1.9 in the reported simulation comparison.

A request to close all three crossings is rejected by the simulator's tool-level restriction.

These values are independent simulation results, not yet verified AI-agent recommendations.

##### Exercise 4 — Simulation Evaluation

Use numerical checks to evaluate the relevant wildfire simulation outcomes and compare findings.

##### Exercise 5 — Critical Review of Agent Reasoning

Examine a supplied flawed agent trace and identify weaknesses in its reasoning, evidence, or conclusions.

##### Exercise 6 — Agent Reliability Experiment

Conduct ten independent AI-agent conversations using the wildfire intervention question.

Evaluate whether each completed agent response correctly identifies the middle and south crossings.

Record:

- Number of completed agent runs
- Number of successful recommendations
- Success rate
- 95% Wilson confidence interval
- Individual agent responses
- JSON execution traces

Expected output files include:

- `exercise6_results.json`
- `trace_ex6_0.json` through `trace_ex6_9.json`

These files should only be reported as completed after successful execution.

#### Experimental Reproducibility

The project emphasizes reproducible research by:

- Comparing intervention options using consistent seeds
- Using repeated simulation trials
- Recording numerical outputs
- Separating independently verified results from AI-generated conclusions
- Saving agent execution traces
- Evaluating agent reliability across multiple conversations

#### Current Project Status

**Completed or verified:**

- Wildfire simulator numerical checks for Exercises 0–4
- Independent comparison of crossing interventions
- Critical review of the supplied flawed trace in Exercise 5
- Installation of Ollama in Google Colab
- Successful connection to the Ollama server
- Successful download of `qwen2.5:7b-instruct`

**Pending verification:**

- Successful model-response test through the notebook's `llm()` function
- Actual AI-agent answers and traces for Exercises 1–4
- Ten independent agent runs for Exercise 6
- Measured Exercise 6 success rate and confidence interval

The latest model-response test encountered a Python `NameError`, so successful agent execution has not yet been established.

These limitations will be updated when the corresponding tests are completed.

#### Technical Report

See the [Wildfire AI Agent Technical Report](https://github.com/DSTX28/Univ-Projects/blob/main/Wildfire_AI_Agent_Technical_Report.pdf) for the project methodology, numerical results, limitations, and technical summary.

The report documents independently checked simulations and does not establish completion of the live AI-agent reliability experiment.

#### Attribution

Based on the **How to Build Agents for Research** workshop presented through CADS at Texas State University, October 2026.

Original workshop materials credit Aniruddha Bora.

This repository is an educational adaptation of the workshop materials. Original workshop contributions are acknowledged, and independently performed experiments are distinguished from the provided material.

#### Disclaimer

This project is intended for research education and software experimentation.

Simulation outputs should not be used to make real-world wildfire response, evacuation, or emergency management decisions.

