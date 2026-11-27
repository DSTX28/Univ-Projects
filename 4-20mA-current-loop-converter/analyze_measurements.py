"""Characterise the built 4-20 mA -> 0-5 V converter from the bench measurements in report.pdf (Table, Sec. 6).

Separates the error into gain, offset and nonlinearity with a least-squares line fit, then shows what a
two-point (4 mA / 20 mA) calibration would leave.   python analyze_measurements.py
"""
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

I_mA = np.array([4, 8, 12, 16, 20], dtype=float)
V_meas = np.array([-0.0644, 1.1695, 2.3047, 3.4972, 4.6486])
V_ideal = (I_mA - 4) * 0.3125                       # 312.5 ohm design, 0 V at 4 mA

slope, intercept = np.polyfit(I_mA, V_meas, 1)       # V per mA
fit = slope * I_mA + intercept
nonlin = V_meas - fit
# two-point calibration using the 4 and 20 mA readings
g = (V_meas[-1] - V_meas[0]) / 16.0
V_cal = (V_meas - V_meas[0]) / g * 0.3125
print(f"effective transimpedance: {1000 * slope:.1f} ohm (design 312.5 ohm, gain error {100 * (slope / 0.3125 - 1):+.1f} %)")
print(f"output at 4 mA: {V_meas[0] * 1000:+.1f} mV (offset)")
print(f"worst nonlinearity vs best-fit line: {1000 * np.abs(nonlin).max():.0f} mV = {100 * np.abs(nonlin).max() / 5:.2f} % of full scale")
print(f"worst error after 2-point calibration: {1000 * np.abs(V_cal - V_ideal).max():.0f} mV "
      f"= {100 * np.abs(V_cal - V_ideal).max() / 5:.2f} % of full scale (before: {100 * np.abs(V_meas - V_ideal).max() / 5:.1f} %)")

fig, (a, b) = plt.subplots(1, 2, figsize=(10, 3.8))
a.plot(I_mA, V_ideal, "k--", label="design (312.5 Ω)")
a.plot(I_mA, V_meas, "o", color="C3", label="measured on bench")
a.plot(I_mA, fit, "-", color="C3", alpha=.5, label=f"fit: {1000 * slope:.1f} Ω")
a.set_xlabel("loop current (mA)"); a.set_ylabel("output (V)"); a.legend(); a.grid(alpha=.3)
a.set_title("Transfer function", loc="left")
b.bar(I_mA - 0.8, 1000 * (V_meas - V_ideal), 1.5, label="raw error", color="C3")
b.bar(I_mA + 0.8, 1000 * (V_cal - V_ideal), 1.5, label="after 2-point calibration", color="C0")
b.axhline(0, color="k", lw=.8); b.set_xlabel("loop current (mA)"); b.set_ylabel("error (mV)")
b.set_title("Error budget: mostly gain, removable by calibration", loc="left"); b.legend(); b.grid(alpha=.3)
fig.tight_layout(); fig.savefig("images/error-analysis.png", dpi=150)
