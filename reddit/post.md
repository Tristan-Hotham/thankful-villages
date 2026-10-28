## Title

[OC] Were Thankful Villages lucky, or just small? Parishes with under 500 people are 9 times likelier than parishes of 1,000 or more to be one of the villages where every serviceman came home from the First World War (Wikipedia list, 2011 Census)

## Body (optional)

A Thankful Village is a parish whose servicemen all came home from the First World War. Of the 55 on the list, 42 are still their own parish, so I set their 2011 populations against all 11,358 parishes in England and Wales. 83% of them have under 500 people, against 46% of all parishes, and the rate falls from about 7 per 1,000 parishes under 500 people to 0.7 per 1,000 for parishes of 1,000 or more. For the five villages that record how many served (11 to 25), the chance that all came home was 4% to 25% if each man faced a 12% risk of dying. On that model, chance alone would give 544 to 1,373 Thankful Villages, far more than the 55 known, probably because many church parishes shared one memorial and because a village has to prove it before it joins the list.

Caveat: 2011 populations stand in for 1911 sizes, so treat the expected totals as orders of magnitude.

Interactive version: https://tristan-hotham.github.io/thankful-villages/

## Source comment

Source: the 55 villages (52 in England, 3 in Wales), their "doubly thankful" flag, coordinates and served counts from the Wikipedia article "Thankful Villages" and the individual village articles, accessed 26 October 2026 (CC BY-SA 4.0). Each village is matched to the civil parish of its nearest postcodes using postcodes.io (ONS Postcode Directory, Open Government Licence v3); 13 villages that are now part of a differently named, larger parish are left out of the size comparison. Population: Office for National Statistics, Census 2011 KS101EW usual residents by parish, via Nomis (Open Government Licence v3); parishes not published separately are treated as under 100. Model: P(all came home) = 0.88^(s·N), with N the parish population and s the share who served (6% to 13%). Outline of England and Wales from Office for National Statistics boundaries (Open Government Licence v3). Base map on the interactive page © Esri.

Tools: Python (pandas, NumPy, GeoPandas, pyproj, matplotlib).

Interactive: https://tristan-hotham.github.io/thankful-villages/
Blog post: https://blog.tristanhotham.com/2026/10/26/thankful-villages-luck-or-size/
Data and code: https://doi.org/10.5281/zenodo.23676168
