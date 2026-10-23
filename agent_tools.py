"""agent_tools.py — the tools an agent may call to study the wildfire simulator.

Each tool takes simple arguments and returns a short dict of numbers. They are deliberately narrow:
a tool that can only run the simulator and summarise it gives the model nothing to misuse.
The crew constraint (at most two crossings) lives INSIDE run_plan, not in a word list: that is the strong form
of a guard rail.
"""
import numpy as np
from fire_sim import *

MAX_CLOSED = 2          # the crew can clear at most two crossings before the fire arrives

def summarise(arrival):
    lost = structures_lost(arrival)
    k, n = int((lost > 0).sum()), len(lost)
    lo, hi = wilson(k, n)
    return {"runs": n, "mean_structures_lost": round(float(lost.mean()), 1), "of_structures": 36,
            "share_of_runs_reaching_town": round(k / n, 2), "share_95pct_interval": [round(float(lo), 2), round(float(hi), 2)],
            "mean_area_burned_ha": int(area_burned(arrival).mean()),
            "median_step_fire_reaches_middle_crossing": float(np.median(crossing_arrival(arrival, "middle")))}

def describe_landscape():
    """What the map looks like and what today's forecast is. Call this first."""
    return {"grid": f"{H} rows x {W} cols, one cell = 1 ha", "river": "runs north-south near column 36, with crossings north/middle/south",
            "town": "36 structures east of the river, rows 31-36, cols 54-59", "fire_start": f"row {START[0]}, col {START[1]} (west of the river)",
            "today": {"wind_speed_m_s": SPEED, "wind_toward": TOWARD, "dryness": DRYNESS, "horizon_steps": HORIZON},
            "wind_directions": list(COMPASS), "dryness_range_seen": "0.6 (damp) to 1.3 (extreme)"}

def run_weather(toward=None, speed=None, dryness=None, n=100, seed=0):
    """Run n fires under given weather (defaults = today) with no firebreaks. Returns summary statistics."""
    if toward is not None and toward not in COMPASS:
        return {"error": f"toward must be one of {list(COMPASS)}"}
    return summarise(simulate(n=n, toward=toward, speed=speed, dryness=dryness, seed=seed))

def run_plan(closed=(), toward=None, speed=None, dryness=None, n=100, seed=0):
    """Run n fires with the named crossings closed by the crew (a tuple/list of 'north','middle','south'). At most two."""
    closed = tuple(closed) if not isinstance(closed, str) else (closed,)
    bad = [c for c in closed if c not in CROSSINGS]
    if bad:
        return {"error": f"unknown crossing(s) {bad}; use north, middle, south"}
    if len(closed) > MAX_CLOSED:
        return {"blocked": f"the crew can clear at most {MAX_CLOSED} crossings before the fire arrives; you asked for {len(closed)}"}
    out = summarise(simulate(n=n, toward=toward, speed=speed, dryness=dryness, closed=closed, seed=seed))
    out["closed"] = list(closed)
    return out

TOOLS_DOC = "\n".join(f"- {f.__name__}{str(__import__('inspect').signature(f))}: {f.__doc__}"
                      for f in (describe_landscape, run_weather, run_plan))
