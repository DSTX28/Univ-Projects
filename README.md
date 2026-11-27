# University engineering projects

**Daniel Shaheen** · Electrical Engineering, Micro & Nano Devices and Systems · Texas State University
(previously Oklahoma State University) · [Portfolio](https://dstx28.github.io/)

Course and workshop projects, one folder each, with report, source files and figures.

| Project | What it shows | Tools |
|---|---|---|
| [**4–20 mA current-loop converter**](4-20mA-current-loop-converter/) | Designed, built and bench-tested an op-amp interface for industrial sensor loops; decomposed the measured error into gain (−6 %), offset and nonlinearity (0.7 % FS) and showed calibration cuts error from 7 % to 1.2 % FS | LM358, simulation, breadboard, DMM, Python |
| [**Band-pass filter design**](bandpass-filter-design/) | Characterised an unknown part from measured frequency-response data, fitted a 4-pole transfer function (2.4 dB RMS error) and designed a standard-value active replacement | MATLAB, LTspice |
| [**Wildfire intervention study**](wildfire-simulation-study/) | Controlled Monte Carlo experiment (fixed seeds, 100 runs × 7 options) finding a 94 % loss reduction; then tested an LLM agent on the same questions: right only 3/10 times, with root causes traced; fixed and sandboxed the workshop notebook | Python, NumPy, Ollama, LLM agents |
| [**Digital fuel pump**](digital-fuel-pump-systemverilog/) | Modular RTL datapath with arithmetic, registered display logic and seven-segment decoding, verified by testbench | SystemVerilog |

### Related projects
- [**fabsim**](https://github.com/DSTX28/fabsim): silicon process simulator (oxidation, diffusion, implantation,
  sheet resistance, oxide colour) validated against published data, with an [interactive furnace demo](https://dstx28.github.io/fabsim/)
- [**secom-yield-analysis**](https://github.com/DSTX28/secom-yield-analysis): SPC and yield-excursion analysis
  of real semiconductor production data
