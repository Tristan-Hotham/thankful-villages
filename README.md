# Thankful Villages: luck or size?

**Read the post and explore the map:** https://tristan-hotham.github.io/thankful-villages/

**Archived data and code:** [doi:10.5281/zenodo.23676168](https://doi.org/10.5281/zenodo.23676168)

A Thankful Village is a parish whose servicemen all came home from the First World War. This project asks whether those villages were lucky or simply small.

## Findings

- Size matters a lot. Parishes with fewer than 500 people (2011 Census) are about nine times likelier to be on the list than parishes of 1,000 or more.

| 2011 parish population | Parishes | Thankful Villages | Per 1,000 parishes |
|---|---:|---:|---:|
| under 100 (not published separately) | 1,140 | 8 | 7.0 |
| 100–199 | 1,149 | 9 | 7.8 |
| 200–499 | 2,918 | 18 | 6.2 |
| 500–999 | 2,019 | 4 | 2.0 |
| 1,000+ | 4,132 | 3 | 0.7 |

- For the five villages that record how many served, everyone coming home was a 4% to 25% chance, if each man faced an independent 12% risk of death.
- Chance alone predicts far more Thankful Villages than are known: between 544 and 1,373 across England and Wales, for 6 to 13 men serving per 100 residents. The likely reasons are shared memorials across multi-township church parishes, and that thankfulness has to be proved before a village joins the list.

## Method

1. **List:** the 55 villages (52 in England, 3 in Wales) and their "doubly thankful" flag come from the Wikipedia article "Thankful Villages" (accessed 26 October 2026). Coordinates come from each village's article.
2. **Parish:** each village is matched to the civil parish of its nearest postcodes (postcodes.io). Thirteen villages are now part of a differently named, larger parish, and they are left out of the size comparison.
3. **Population:** 2011 Census KS101EW usual residents by parish, from Nomis. Parishes the Census did not publish separately are treated as "under 100".
4. **Model:** P(thankful) = 0.88<sup>s·N</sup>, where N is the parish population and s the share who served.
5. **Served counts:** from the village articles. Upper Slaughter 25 (24 men and one woman), Colwinston 23, Nether Kellet 21, Harley 20, Stretton en le Field 11.

Modern populations are a proxy for 1911 sizes. Treat the expected totals as orders of magnitude.

## Files

| Path | What it is |
|---|---|
| `analysis.py` | The whole analysis. It writes `results/` and `data/thankful.json`. |
| `data/raw/thankful_villages.json` | Villages parsed from Wikipedia, with coordinates and the nearest postcodes' parishes. |
| `data/raw/parishes2011_ks101.csv` | 2011 Census usual residents by parish, England and Wales (Nomis). |
| `results/thankful_villages.csv` | One row per village with parish, population and match status. |
| `results/size_bands.csv` | Counts by population band, with model expectations. |

## Sources and licences

- Wikipedia, "Thankful Villages" and individual village articles, CC BY-SA 4.0.
- Office for National Statistics, Census 2011 (KS101EW) via Nomis, Open Government Licence v3.
- postcodes.io, using the ONS Postcode Directory, OGL v3.
- Base map © Esri.

Code is MIT licensed.

AI use: written with drafting, data and coding help from Claude (Anthropic).

Tristan Hotham, independent researcher, 2026.
