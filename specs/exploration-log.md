# ACLED Exercise — Exploration Log

Technical exercise for the ACLED Visualization and Digital Communication Specialist application, 2026-09-10, 4-hour time limit.

## Brief (summary)

Choose one of two datasets (US protests, 2024-present — or Sahel, Mali/Burkina Faso/Niger, 2024-present). Deliverables: a map, an infographic, one additional chart, and an explanation of the pattern found, enriched with an external dataset. Graded on the quality of the pattern, the relevance of the external data, technical skill, and how attractive/insightful the visuals are for an external audience.

## Dataset and angle

**US events, "protests against data centers"** (330 events, extracted from free-text `notes` via keyword match on "data center"/"data centre" — the topic isn't in any structured field). Chosen over the Sahel dataset (JNIM/gold-mining angle: interesting but external mining/infrastructure data too scattered to source cleanly in 4h) because of a very clear temporal pattern (3 events in 2024 → 266 in the first 8 months of 2026), a broad geographic spread, and a genuinely non-obvious finding rather than an already widely-covered story.

**Finding**: contestation is far higher, relative to industry size, in states new to data centers (Indiana, Wisconsin, Michigan, Missouri) than in established hubs (Virginia, Texas, California). Indiana draws roughly six times more protests per operational data center than Virginia. Population, water stress, and proximity to cities were tested and don't explain the gap.

## Paths explored and dropped

- **Sahel / JNIM territorial expansion or gold-mining financing**: strong actor-level pattern, but no clean external mining/infra data available in time.
- **State tax-incentive aggressiveness** (first external-data angle): dropped after re-reading protest notes, only 8/330 events cited the topic — not what people are actually protesting.
- **Proximity to cities** (data-center-to-town distance, and state-level correlation with protest rate): tested twice, both times a clean negative result (correlation ≈ 0). Not a driver.
- **Water-stress category (WRI Aqueduct)**: no linear relationship; over-representation sits in the "Medium-High" band only, not the most extreme one. Kept as a secondary, hedged finding, not a main angle.
- **Violence/geography checks** (which protest topics or US regions run more violent): data centers protests are ~0.18× as violent as the dataset baseline (98% peaceful) — used to characterize the movement, not as an external-data angle.
- **Operation Metro Surge / immigration-enforcement protests (Minnesota)**: a very strong, well-documented pattern (named DHS operation, fatalities, national mobilization) found in the same dataset, deliberately set aside — already extensively covered by national press, less useful to demonstrate finding a non-obvious signal.
- **Chart formats tried and rejected**: a 42-state heatmap and a 42-line chart were both too dense to read and duplicated the map's state-by-state comparison; replaced by the national bubble timeline (see below).
- **Crowd-size weighting**: re-ran the state ratio weighted by ACLED's crowd-size tags instead of raw event counts. Confirms and even sharpens the gap on high-n states, but unstable on low-n states (a single "large"-tagged event can dominate) — kept as a robustness argument in text, not as the map's metric.

## Data center count: three sources, in order (kept in detail — none of them is clean)

The map's ratio needs a reliable count of data centers per state. No public source turned out to be fully trustworthy; each was checked against known reality before being replaced.

1. **IM3 Open Source Data Center Atlas** (PNNL/DOE, OpenStreetMap-derived, ODbL). Plausible at first glance (Virginia led, matching its "Data Center Alley" reputation) — but Benjamin manually checked the Indiana rows and found only 4 facilities listed (2 of them mistagged university buildings) against a real count of ~46 (Data Center Frontier). OSM-derived data structurally lags behind fast-growing markets — dropped as the count source, still used later for the water-stress point join.
2. **FracTracker U.S. Data Centers Tracker** (advocacy-oriented nonprofit, news/permits/FOIA-sourced). Fixed the Indiana problem (43 facilities, close to reality) and added a useful independent `community_pushback` field. Benjamin then flagged that Florida and Utah showed 0 "Operating" facilities, which looked suspicious; checking it confirmed both states host major, long-running data centers (Equinix Miami since 2017, Meta Eagle Mountain since 2021) that FracTracker simply doesn't track — coverage is denser where its advocacy partners are active, thinner elsewhere.
3. **dcmap.us (US Data Center Map)**, a monthly-updated aggregator with full state-level coverage and no artificial zeros (Florida 123 operational, Utah 50). Used for the final ratio. Citation required by their usage policy; only derived aggregates are republished, not raw rows (their API doesn't expose those anyway).

Independent cross-check: FracTracker's own `community_pushback` rate (% of tracked facilities with documented opposition) shows the same ranking as the ACLED-based ratio — Virginia lowest (2.4%), Wisconsin/Michigan/Missouri/Indiana highest (37-60%) — two unrelated methods agreeing on the same story.

## The map: protests per operational data center, by state

- Metric: ACLED protest count ÷ dcmap.us operational data center count, by state.
- Robustness checks: same ranking holds when the denominator is `planned` projects instead, or `operational + planned` combined; holds when protests are weighted by estimated crowd size. Population correlation with the ratio: −0.18 (not a confound).
- Built as a 3D region map in Flourish (height and color both encode the ratio); tooltip also carries protest count, operational/planned counts, and water-stress level for context.
- File: `output/flourish_states_with_data.geojson`; source table: `output/state_summary_v4_dcmap.csv` (in `output/archive/` after final cleanup, see its README).

## The chart: national turnout timeline

- A bubble scatter, one point per month (Jan 2024–Aug 2026), sized by estimated turnout (ACLED crowd-size tags: very small=10 … massive=10,000; missing tags default to "small"=50, per ACLED's own methodology).
- Shows the escalation the map doesn't: near-zero through 2024, sharp acceleration from late 2025, a peak in July 2026 partly driven by a coordinated national day of action on 18 July 2026 (142 protests, 42 states — confirmed via press, not just organic growth).
- Chosen over a per-state breakdown specifically to avoid re-showing the map's own comparison on a second chart.
- File: `output/bubble_timeline_national.csv`.

## The infographic: 3D terrain (Blender, bonus)

- A US-shaped mesh (silhouette cut from state boundaries, longitude corrected by cos(37°N) for a non-distorted shape), displaced by a heightmap of estimated turnout density (Gaussian-smoothed point data, tight sigma for distinct small peaks rather than merged hills).
- Cycles render (GPU/OptiX), height-based navy-to-orange material matching ACLED's brand colors, five tallest peaks labeled: Luther OK (~5,500), Taylor TX (~5,100), Memphis TN (~5,110), Lewisburg WV (5,000), Kenilworth NJ (~5,100).
- Composited in Affinity Designer with title, peak labels, and source line.
- Built outside the three required deliverables, as an extra.
- Files: `blender/` (scene, heightmaps, mask), `assets/Estimated Turnout Density Map.png` (final export).

## What people are protesting (used in the accompanying text, not a separate external-data angle)

Motives extracted from `notes`: environment/pollution (184/330), water (118), lack of public consultation (50), noise (42), electricity (38), AI mentioned explicitly (38). Concrete, local grievances, not anti-AI ideology — corroborated by press coverage found independently (NIPSCO electricity-cost complaints in Indiana, Meta's well-depletion case in Newton County, Georgia).
