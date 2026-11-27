"""fire_sim.py — the wildfire simulator from the CADS workshop "How to Build Agents for Research", as a module.

A probabilistic cellular automaton (Alexandridis et al., 2008 style) on a 48 x 72 cell landscape (one cell = one
hectare): a river with three crossings (north, middle, south), a town east of the river, a fire starting west of it.
Wind speed and direction, dryness and firebreaks (closed crossings) change how it spreads. Everything is vectorised:
simulate(n=100) runs 100 fires at once in well under a second.

    from fire_sim import *
    arrival = simulate(n=100)                       # today's conditions: wind 6 m/s toward E, dryness 0.9, 55 steps
    structures_lost(arrival).mean()                 # buildings reached, averaged over the 100 fires
    simulate(n=100, closed=("middle",))             # with the middle crossing cleared by the crew
    simulate(n=100, toward="NE", dryness=1.1)       # other weather
    crossing_arrival(arrival, "middle")             # step at which each fire reached the crossing (inf = never)
    wilson(k, n)                                    # 95% interval for a proportion
"""
import math
import numpy as np

P0, C1, C2, A_SLOPE, CELL = 0.58, 0.045, 0.131, 0.078, 100.0     # Alexandridis et al. (2008); cell size in metres
SPOT_RATE, SPOT_REACH = 0.0004, 0.4                              # spotting: illustrative values
UNBURNED, BURNING, BURNED = 0, 1, 2
WATER, ROCK, PASTURE, SHRUB, FOREST, STRUCTURE = 0, 1, 2, 3, 4, 5
VEG = {PASTURE: (-0.4, 0.0), SHRUB: (0.4, -0.3), FOREST: (0.4, 0.0), STRUCTURE: (-0.4, 0.0)}   # (p_veg, p_den)
OFFSETS = [(-1, 0), (1, 0), (0, -1), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1)]

def shift(a, dr, dc, fill=0):
    """Move every value in the grid(s) `a` by (dr, dc) cells; cells that scroll in get `fill`."""
    out = np.full_like(a, fill); h, w = a.shape[-2:]
    out[..., max(dr, 0):h + min(dr, 0), max(dc, 0):w + min(dc, 0)] = a[..., max(-dr, 0):h + min(-dr, 0), max(-dc, 0):w + min(-dc, 0)]
    return out

def spread_base(fuel, elev):
    """Ignition probability from each of the 8 neighbours with no wind: fuel and slope terms. Shape (8, H, W)."""
    veg = np.zeros(fuel.shape, np.float32)
    for kind, (p_veg, p_den) in VEG.items():
        veg[fuel == kind] = (1 + p_veg) * (1 + p_den)
    base = np.zeros((8,) + fuel.shape, np.float32)
    for i, (dr, dc) in enumerate(OFFSETS):
        rise = elev - shift(elev, dr, dc)                                  # this cell minus the burning neighbour
        slope = np.degrees(np.arctan(rise / (CELL * np.hypot(dr, dc))))    # positive when the fire climbs
        base[i] = P0 * veg * np.exp(A_SLOPE * slope)
    return base

def step(fire, base, speed, toward, dryness, rng, blocked=None, spotting=True):
    """One time step for a batch of N fires at once. fire: (N, H, W). speed, toward (radians), dryness: (N,)."""
    burning = fire == BURNING
    can_burn = (fire == UNBURNED) & (base[0] > 0)
    if blocked is not None:
        can_burn &= ~blocked                                               # firebreaks
    escape = np.ones(fire.shape, np.float32)                               # chance that no neighbour ignites the cell
    for i, (dr, dc) in enumerate(OFFSETS):
        p_wind = np.exp(speed * (C1 + C2 * (np.cos(np.arctan2(dr, dc) - toward) - 1)))
        p = np.minimum(base[i] * (p_wind * dryness).astype(np.float32)[:, None, None], 1)
        escape *= 1 - p * shift(burning, dr, dc)
    new = fire.copy()
    new[can_burn & (rng.random(fire.shape, dtype=np.float32) > escape)] = BURNING
    new[burning] = BURNED
    if spotting:                                                           # embers carried downwind
        n, r, c = np.nonzero(burning & (rng.random(fire.shape) < SPOT_RATE * speed[:, None, None]))
        dist, angle = rng.exponential(SPOT_REACH * speed[n]), toward[n] + rng.normal(0, 0.25, len(n))
        rr, cc = np.round(r + dist * np.sin(angle)).astype(int), np.round(c + dist * np.cos(angle)).astype(int)
        ok = (rr >= 0) & (rr < fire.shape[1]) & (cc >= 0) & (cc < fire.shape[2])
        n, rr, cc = n[ok], rr[ok], cc[ok]
        lands = can_burn[n, rr, cc] & (new[n, rr, cc] == UNBURNED)
        new[n[lands], rr[lands], cc[lands]] = BURNING
    return new

def run_fire(fuel, elev, ignite, steps, n=1, speed=6.0, toward=0.0, dryness=1.0, blocked=None, seed=0, spotting=True):
    """Run n fires. Returns `arrival`: for every run and cell, the step at which it ignited (-1 = never)."""
    rng, base = np.random.default_rng(seed), spread_base(fuel, elev)
    speed, toward, dryness = (np.broadcast_to(np.asarray(v, float), (n,)) for v in (speed, toward, dryness))
    fire = np.zeros((n,) + fuel.shape, np.int8); fire[:, ignite[0], ignite[1]] = BURNING
    arrival = np.where(fire == BURNING, 0, -1).astype(np.int16)
    for t in range(1, steps + 1):
        fire = step(fire, base, speed, toward, dryness, rng, blocked, spotting)
        arrival[(fire == BURNING) & (arrival < 0)] = t
    return arrival

# %% ---------------------------------------------
H, W = 48, 72                                                  # 4.8 km by 7.2 km
CROSSINGS = {"north": range(6, 10), "middle": range(22, 26), "south": range(38, 42)}
TOWN, START = (slice(31, 37), slice(54, 60)), (24, 8)
COMPASS = {"E": 0, "SE": 45, "S": 90, "SW": 135, "W": 180, "NW": 225, "N": 270, "NE": 315}   # direction the wind blows toward
SPEED, TOWARD, DRYNESS, HORIZON = 6.0, "E", 0.9, 55            # today's conditions; containment expected at step 55

def blur(a, times):
    for _ in range(times):
        a = (a + np.roll(a, 1, 0) + np.roll(a, -1, 0) + np.roll(a, 1, 1) + np.roll(a, -1, 1)) / 5
    return a

def make_landscape(seed=3):
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:H, 0:W].astype(float)
    river = (36 + np.round(3 * np.sin(np.arange(H) / 7))).astype(int)          # column of the river in each row
    d = xx - river[:, None]
    elev = 180 * (1 - np.exp(-(d / 18) ** 2))                                  # the valley
    for r, c, height, size in [(10, 14, 110, 7), (34, 20, 90, 8), (14, 58, 100, 7), (38, 62, 120, 8), (26, 4, 60, 6)]:
        elev += height * np.exp(-((yy - r) ** 2 + (xx - c) ** 2) / (2 * size ** 2))   # hills
    rough = blur(rng.standard_normal((H, W)), 8)
    elev = np.maximum(elev + 8 * rough / rough.std(), 0)
    patch = blur(rng.standard_normal((H, W)), 5); patch /= patch.std()
    fuel = np.full((H, W), SHRUB)
    fuel[elev + 30 * patch > 150] = FOREST
    fuel[(np.abs(d) < 5) & (patch < 0.3)] = PASTURE
    rocks = blur(rng.standard_normal((H, W)), 2)
    fuel[(rocks > 2.2 * rocks.std()) & (elev > 120)] = ROCK
    for r in range(H):
        fuel[r, river[r]:river[r] + 2] = WATER
    for rows in CROSSINGS.values():
        for r in rows:
            fuel[r, river[r]:river[r] + 2] = PASTURE
    fuel[29:39, 51:63] = np.where(fuel[29:39, 51:63] == WATER, WATER, PASTURE)  # fields around the town
    fuel[TOWN] = STRUCTURE
    return dict(fuel=fuel, elev=elev, river=river)

LAND = make_landscape()

def firebreak(*closed):
    """Cells cleared by the crew: the named crossings."""
    mask = np.zeros((H, W), bool)
    for name in closed:
        for r in CROSSINGS[name]:
            mask[r, LAND["river"][r]:LAND["river"][r] + 2] = True
    return mask

def simulate(n=1, steps=None, speed=None, toward=None, dryness=None, closed=(), seed=0):
    """Run n fires on the landscape under today's conditions unless told otherwise. Returns arrival steps, shape (n, H, W)."""
    toward = np.radians(COMPASS[toward or TOWARD]) if isinstance(toward or TOWARD, str) else toward
    return run_fire(LAND["fuel"], LAND["elev"], START, steps or HORIZON, n, SPEED if speed is None else speed, toward,
                    DRYNESS if dryness is None else dryness, firebreak(*closed)[None] if closed else None, seed)

# what we measure
def structures_lost(arrival): return (arrival[:, TOWN[0], TOWN[1]] >= 0).sum((1, 2))
def area_burned(arrival):     return (arrival >= 0).sum((1, 2))                    # in cells; one cell is one hectare
def crossing_arrival(arrival, name):
    """Step at which each run's fire reached the named crossing (inf = never)."""
    a = np.stack([arrival[:, r, LAND["river"][r]] for r in CROSSINGS[name]], 1).astype(float)
    return np.where(a >= 0, a, np.inf).min(1)

def wilson(k, n, z=1.96):
    """95% confidence interval for a proportion k/n."""
    p, den = k / n, 1 + z * z / n
    centre, half = (p + z * z / (2 * n)) / den, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / den
    return max(0.0, centre - half), min(1.0, centre + half)


def show(arrival, title=""):
    """Draw one fire (or the first of a batch): the landscape with burned cells coloured by the step they ignited."""
    import matplotlib.pyplot as plt
    a = arrival[0] if arrival.ndim == 3 else arrival
    fig, ax = plt.subplots(figsize=(9, 6))
    terrain = {WATER: "#3F8FD9", ROCK: "#B9B4AC", PASTURE: "#E6DFA4", SHRUB: "#BFCB8B", FOREST: "#7FA670", STRUCTURE: "#FFFFFF"}
    img = np.zeros(LAND["fuel"].shape + (3,))
    for k, hx in terrain.items():
        img[LAND["fuel"] == k] = [int(hx[i:i + 2], 16) / 255 for i in (1, 3, 5)]
    ax.imshow(img, interpolation="nearest")
    burned = np.ma.masked_where(a < 0, a)
    im = ax.imshow(burned, cmap="YlOrRd_r", alpha=0.85, interpolation="nearest")
    ax.plot(START[1], START[0], "k*", ms=14, label="ignition")
    ax.add_patch(plt.Rectangle((TOWN[1].start - 0.5, TOWN[0].start - 0.5), 6, 6, fill=False, lw=2, ec="black", label="town"))
    for name, rows in CROSSINGS.items():
        ax.text(LAND["river"][rows[0]] + 3, rows[0] + 2, name, fontsize=9, va="center")
    fig.colorbar(im, ax=ax, label="step at which the cell ignited")
    ax.set_title(title or "one fire: lighter = reached later"); ax.set_xticks([]); ax.set_yticks([]); ax.legend(loc="lower left", fontsize=8)
    plt.show()
