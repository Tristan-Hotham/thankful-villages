"""r/dataisbeautiful collage for thankful-villages: thankful_villages_luck_or_size.png (2400 x 3000).
Every number is read from results/size_bands.csv, results/thankful_villages.csv, results/curve.json and data/thankful.json,
or computed from them. Run: python3 collage.py  (THANKFUL=/path/to/thankful-villages)
"""
import os, sys, json
HERE = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, HERE)
TV = os.environ.get("THANKFUL", "/home/claude/repo-thankful")
import numpy as np, pandas as pd
from house import *
from matplotlib.lines import Line2D

BANDS = pd.read_csv(os.path.join(TV, "results/size_bands.csv"), index_col=0)
T = pd.read_csv(os.path.join(TV, "results/thankful_villages.csv"))
CURVE = np.array(json.load(open(os.path.join(TV, "results/curve.json")))["curve"])
J = json.load(open(os.path.join(TV, "data/thankful.json")))
C = counties_km(); EW = C[C.nation.isin(["England", "Wales"])]

labs = list(BANDS.index)                       # under 100, 100–199, 200–499, 500–999, 1,000+
PAL = ["#0F5C55", "#2E9A8A", "#7CC3B0", "#E7A54A", "#B5532A"]
OTHER = "#B4AC9E"
bands = [0, 100, 200, 500, 1000, 1e9]
def band(p, nd):
    return labs[0] if nd else labs[np.searchsorted(bands, p, side="right") - 1]
T["band"] = [band(p, nd) if sp else None for p, nd, sp in zip(T.pop2011, T.nodata2011, T.same_parish)]
T["x"], T["y"] = to_km(T.lon.values, T.lat.values)
assert int(T.same_parish.sum()) == int(BANDS.thankful.sum())

small = BANDS.loc[labs[:3]]; big = BANDS.loc[labs[4]]
ratio = (small.thankful.sum() / small.parishes.sum()) / (big.thankful / big.parishes)
share_tv_small = 100 * small.thankful.sum() / BANDS.thankful.sum()
share_par_small = 100 * small.parishes.sum() / BANDS.parishes.sum()
sv = {n: (s, p) for n, s, p in J["served"]}
pmin, pmax = min(p for s, p in sv.values()), max(p for s, p in sv.values())
ex = J["expected"]

fig = new_fig()
words(fig, 0.045, 0.972, [("Were Thankful Villages", FG)])
words(fig, 0.045, 0.924, [("lucky,", PAL[3]), ("or just", FG), ("small?", PAL[0])])
fig.text(0.045, 0.862, f"Thankful Villages are parishes whose servicemen all came home from the First World War. {len(T)} are\n"
         f"known; {int(T.same_parish.sum())} are still their own parish, so their size can be set against all {J['n_parishes']:,} parishes in England and Wales.",
         family=SER, fontsize=14.5, color=FG, va="top", linespacing=1.15)

ax = fig.add_axes([0.0, 0.25, 0.6, 0.575]); ax.set_facecolor(BGC)
EW.plot(ax=ax, color=LAND, edgecolor=BGC, linewidth=0.6, zorder=0)
for b, c in zip(labs, PAL):
    m = T.band == b
    ax.scatter(T.x[m], T.y[m], s=120, color=c, edgecolor="white", lw=1, zorder=3)
m = T.band.isna()
ax.scatter(T.x[m], T.y[m], s=90, color=OTHER, edgecolor="white", lw=1, zorder=2)
d = T.doubly.astype(bool)
ax.scatter(T.x[d], T.y[d], s=330, facecolor="none", edgecolor=FG, lw=1.1, zorder=4)
ax.set_xlim(130, 660); ax.set_ylim(5, 665); ax.set_aspect(1); ax.axis("off")


def note(txt, xy, xyt, ha="left"):
    ax.annotate(txt, xy=xy, xytext=xyt, family=MONO, fontsize=10.2, color=FG, ha=ha, va="center", zorder=8,
                arrowprops=dict(arrowstyle="-", color=FG, lw=.8, shrinkB=6), path_effects=halo(3))


pct = lambda p: int(p * 100 + 0.5)            # round half up, as in the README (24.5% -> 25%)
pos = {"Upper Slaughter": ((470, 30), "left"), "Nether Kellet": ((230, 520), "center"), "Harley": ((215, 390), "center"),
       "Colwinston": ((200, 110), "center"), "Stretton en le Field": ((548, 390), "left")}
for v, (xyt, ha) in pos.items():
    r = T[T.village == v].iloc[0]; s, p = sv[v]
    nm = "Stretton en le\nField" if v.startswith("Stretton") else v
    note(f"{nm}: {s} served,\n{pct(p)}% chance all\ncame home", (r.x, r.y), xyt, ha)

# key
fig.text(0.62, 0.8, "2011 PARISH POPULATION", family=MONO, fontsize=11, color=MUT)
yy = 0.776
for b, c in zip(labs, PAL):
    fig.lines.append(Line2D([0.635], [yy], marker="o", ms=10, color=c, mec="white", transform=fig.transFigure))
    fig.text(0.652, yy, b + (" or not published" if b == labs[0] else ""), family=MONO, fontsize=10.5, color=FG, va="center")
    yy -= 0.021
fig.lines.append(Line2D([0.635], [yy], marker="o", ms=9, color=OTHER, mec="white", transform=fig.transFigure))
fig.text(0.652, yy, "now part of a larger parish", family=MONO, fontsize=10.5, color=FG, va="center"); yy -= 0.028
fig.lines.append(Line2D([0.635], [yy], marker="o", ms=15, mfc="none", mec=FG, mew=1.1, ls="none", transform=fig.transFigure))
fig.text(0.652, yy, f"doubly thankful: all came home\nfrom both world wars ({int(d.sum())})", family=MONO, fontsize=10.5, color=FG,
         va="center", linespacing=1.15)

items = [
    (f"{ratio:.0f}×", PAL[0],
     f"likelier to be a Thankful Village if the parish\nhas under 500 people than if it has 1,000 or more."),
    (f"{share_tv_small:.0f}%", PAL[1],
     f"of the matched villages have under 500 people.\nOnly {share_par_small:.0f}% of all parishes are that small."),
    (f"{pct(pmin)}% to {pct(pmax)}%", PAL[3],
     f"chance that all came home, for the five villages\nthat record how many served, if each man had\na 12% risk of dying."),
    (f"{ex['0.13']:,} to {ex['0.06']:,}", PAL[4],
     f"Thankful Villages would be expected by chance\nalone, against the {len(T)} known. Shared memorials\nand the need for proof may explain the gap."),
]
headlines(fig, [0.62, 0.25, 0.37, 0.362], items, big=34, step=0.25, sub_off=0.1)

# bottom: rate by size band, and the luck curve
label(fig, 0.045, 0.232, "THANKFUL VILLAGES PER 1,000 PARISHES, BY 2011 POPULATION")
a = fig.add_axes([0.07, 0.085, 0.4, 0.12]); a.set_facecolor(BGC)
xs = np.arange(len(labs))
a.bar(xs, BANDS.rate_per_1000, color=PAL, width=.7)
for x0, v, n in zip(xs, BANDS.rate_per_1000, BANDS.thankful):
    a.text(x0, v + .25, f"{v:.1f}", family=MONO, fontsize=10, color=FG, ha="center", va="bottom")
a.set_xticks(xs, labs); a.set_ylim(0, 9.5); a.set_yticks([])
for t in a.get_xticklabels(): t.set_family(MONO); t.set_fontsize(9.6); t.set_color(MUT)
a.tick_params(length=0)
for sp in a.spines.values(): sp.set_visible(False)
a.axhline(0, color=FG, lw=.8)

label(fig, 0.55, 0.232, "CHANCE THAT EVERYONE CAME HOME (12% RISK EACH)")
b = fig.add_axes([0.6, 0.085, 0.36, 0.12]); b.set_facecolor(BGC)
b.plot(CURVE[:, 0], CURVE[:, 1] * 100, color=PAL[4], lw=2)
for v, (s, p) in sv.items():
    b.plot(s, p * 100, "o", ms=7, color=PAL[3], mec="white", zorder=3)
b.set_xlim(0, 60); b.set_ylim(0, 100)
b.set_yticks([0, 50, 100], ["0%", "50%", "100%"]); b.set_xticks([0, 10, 20, 30, 40, 50, 60])
b.set_xlabel("men serving", family=MONO, fontsize=9.6, color=MUT, labelpad=2)
for t in b.get_xticklabels() + b.get_yticklabels(): t.set_family(MONO); t.set_fontsize(9.6); t.set_color(MUT)
b.tick_params(length=0)
for sp in ("top", "right"): b.spines[sp].set_visible(False)
for sp in ("left", "bottom"): b.spines[sp].set_color("#BDB5A6")
b.grid(color="#DDD6C8", lw=.6); b.set_axisbelow(True)
b.text(26, 30, "the five villages\nwith served counts", family=MONO, fontsize=9.6, color=FG, va="center")

footer(fig, "Data: Wikipedia 'Thankful Villages' and village articles (CC BY-SA 4.0), accessed 26 October 2026; ONS Census 2011 KS101EW\n"
       "via Nomis and postcodes.io (ONS Postcode Directory), both OGL v3; counties ONS (OGL v3). 2011 populations stand in for 1911\n"
       "sizes; treat expected totals as orders of magnitude. Analysis and chart: Tristan Hotham, with Python and matplotlib.")
fig.savefig(os.path.join(HERE, "thankful_villages_luck_or_size.png"), dpi=200, facecolor=BGC)
print("written", ratio, share_tv_small, share_par_small, pmin, pmax, int(d.sum()))
