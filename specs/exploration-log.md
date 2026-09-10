# ACLED Exercise — Exploration Log and Hypotheses

Technical exercise for the ACLED Visualization and Digital Communication Specialist application, 2026-09-10, 4-hour time limit.

## Brief (summary)

Choose one of two provided datasets (US protests, 2024-present — or Sahel, Mali/Burkina Faso/Niger, 2024-present).
Deliverables: at least one map, one infographic, one additional chart, and an explanation of the identified pattern.
Enrich with an external dataset (mining, infrastructure, economic, demographic...).
Tools: free choice of preprocessing (Python, QGIS), map/chart in Tableau or Flourish, infographic in an AI design tool.
Graded on: quality of the pattern, relevance of the external data, technical skill, and how attractive/insightful the visualizations are for an external audience.

## Initial exploration — both datasets

**US events** (`ACLED_US_events_...csv`), 42,188 rows, 2024-01-01 to 2026-09-03.
- 39,941 Protests (94.7%), 1,721 Strategic developments, 367 Riots, the rest marginal.
- The `tags` column mostly carries `crowd size=...` plus a few keywords (Repression, counter-demonstration) — no topical theme in `tags`, so themes have to be found in `notes` (free text), as the brief itself suggests.
- Keyword scan on `notes` (count of events mentioning the term):
  - immigration/ICE: 15,055 · Trump/admin: 12,993 · healthcare: 6,121 · Israel/Palestine: 5,263 · labor/union: 5,390 · LGBTQ: 2,666 · housing: 1,087 · abortion: 815 · climate: 553 · election: 323 · **data center: 330**
- New York, California, and Massachusetts lead on raw protest volume, but that mostly reflects population size and media coverage rather than an interesting pattern in itself.

**Sahel events**, 13,160 rows (Mali 5,892 / Burkina Faso 4,899 / Niger 2,369).
- Dominated by political violence: Battles (3,988), Strategic developments (3,253), Violence against civilians (2,756), Explosions/Remote violence (2,523). Protests marginal (557).
- Cumulative fatalities: Burkina Faso 15,726, Mali 12,214, Niger 5,348 — Burkina Faso has a higher fatalities-per-event ratio than Mali.
- One actor dominates by far: JNIM (5,513 events), followed by Malian armed forces (2,154) and ISSP (1,453).
- Possible angle: JNIM's territorial expansion / town sieges, or a link between artisanal gold-mining zones and JNIM activity (financing) — but the external data (mining, infrastructure) is too scattered to source cleanly within the time limit. Dropped.

## Dataset decision

**US events, "protests against data centers" angle** (extracted from `notes` via keyword match on `data center`/`data centre`).

Why:
- A workable subset size (330 events) with a **very clear temporal pattern**: 3 events in 2024 → 61 in 2025 → 266 in the first 8 months of 2026. Near-exponential growth, a strong and verifiable story.
- Broad, diffuse geographic spread (Indiana, Texas, Virginia, Michigan, Missouri at the top, not concentrated in 1-2 states), consistent with a national wave of local backlash rather than an isolated phenomenon.
- A very topical subject (the AI data center boom, water/electricity/land-use tension), matching exactly the example given in the brief — likely a real pattern the exercise designers intended to be found in this dataset.
- Dropped alternative: Sahel/JNIM (external mining/infrastructure data too slow to source cleanly within the time limit).

## Motives expressed by protesters

Re-read the `notes` of all 330 events to identify the motives actually expressed (keyword search on free text; a single event can cite several motives):

| Motive cited in `notes` | Events / 330 |
|---|---|
| Environment/pollution (general) | 184 |
| Water (consumption, contamination, aquifer depletion) | 118 |
| Democratic process / lack of public consultation | 50 |
| Noise | 42 |
| Electricity (rates, strained grid) | 38 |
| AI mentioned explicitly | 38 |
| Farmland/zoning | 17 |

**Finding**: the dominant motives are concrete and local (water, electricity, opaque approval process), not ideological or anti-AI. Motives are often combined within a single protest (e.g. Saint Charles, Missouri, August 2025: water, grid strain, and lack of consultation all cited together). The Ogallala Aquifer is named repeatedly (e.g. Amarillo, Texas).

→ A replacement/complementary angle was considered and later confirmed: cross-referencing protest locations with water-stress data (water is the most recurrent concrete motive after general environmental concerns), a good fit for Benjamin's GIS background. See dedicated section below.

## Nature of the unrest (peaceful vs. violent)

Across the 330 events in the data center subset, `sub_event_type`:
- Peaceful protest: 324 (98.2%)
- Protest with intervention: 5 (1.5%)
- Attack: 1 (0.3%)

No "Mob violence" or "Riot" at all (these categories do exist in the full US dataset — 167 mob violence events out of 42,188 — but none appear in the data center subset). An almost entirely peaceful movement: residents, environmental groups (Sierra Club recurs often), attendance at city council meetings and public hearings.

Notable exception: 6 April 2026, Indianapolis (Indiana) — a shooting targeting the home of a local City-County Councilor who had supported a data center project, with a note left protesting the construction. No injuries, coded "Attack." An isolated but discordant signal worth flagging in the accompanying text, without over-weighting it (1 case out of 330).

## Violence by protest theme (full US dataset)

Question: are some protest themes more prone to violence than others? Method: same keyword approach on `notes`; `is_violent` = sub_event_type in {Violent demonstration, Mob violence, Looting/property destruction, Attack, Armed clash}.

Baseline across the full US dataset (n=42,188): **1.65% violent**.

| Theme | % violent | n |
|---|---|---|
| Israel/Palestine | 3.40% | 5,263 |
| Immigration/ICE | 2.69% | 15,055 |
| Police (topic) | 2.33% | 129 |
| LGBTQ | 1.76% | 2,666 |
| Housing | 1.56% | 1,087 |
| Election | 1.55% | 323 |
| Abortion | 0.61% | 815 |
| Labor/union | 0.56% | 5,390 |
| Trump/admin | 0.47% | 12,993 |
| **Data centers** | **0.30%** | **330** |
| Healthcare | 0.08% | 6,121 |
| Climate | 0.00% | 553 |
| Guns | 0.00% | 132 |

**Finding**: Israel/Palestine and immigration/ICE sit well above the baseline (×2 and ×1.6). Data centers sit well below it (×0.18 the baseline) — confirming and reinforcing the earlier finding (98.2% peaceful in the dedicated subset): this is a movement of residents and associations, not a conflictual one, unlike other topics in the same dataset. A usable point for the accompanying text to characterize the nature of the movement.

## Violence by geographic region (full US dataset)

At the broad census-region level (Northeast/Midwest/South/West): a small spread — Northeast 1.84%, West 1.82%, Midwest 1.48%, South 1.28% (national baseline 1.65%). Not very discriminating at this level of aggregation.

At the state level (n≥200 events): a clearer spread. Leading: Oregon 3.18% (n=817), Minnesota 3.07% (n=1,107), New York 2.88% (n=5,315), Illinois 2.47% (n=1,823), DC 2.39% (n=964). Lowest: West Virginia 0.00% (n=222), Maine 0.17% (n=577), Iowa 0.23% (n=437).

Consistent with the well-known reputation of Portland/Minneapolis/NYC/Chicago as flashpoints for protest unrest (post-2020 George Floyd legacy in particular). Not directly tied to the data center subject (peaceful everywhere, including in these states) — kept as possible context, not as a main angle.

## Primary external dataset: IM3 Open Source Data Center Atlas (PNNL/DOE)

- Source: Mongird, Thurber, Vernon, Burleyson, Akdemir, Rice — Pacific Northwest National Laboratory, funded by the DOE Office of Science (IM3 program). Locations derived from OpenStreetMap.
- DOI: https://doi.org/10.57931/2550666 — page: https://data.msdlive.org/records/65g71-a4731
- License: Open Data Commons Open Database License (ODbL), citation required.
- Local file: `data/raw/im3_open_source_data_center_atlas/im3_open_source_data_center_atlas.csv`
- 1,242 rows (1,040 buildings, 109 campuses, 93 points), columns: id, state, state_abb, state_id, county, county_id, operator, ref, name, sqft, lon, lat, type

Plausibility check: Virginia leads (292 facilities), matching its well-known reputation as "Data Center Alley" (Northern Virginia) — a credible source on that basis.

## Result: protests-to-existing-data-centers ratio by state (first pass)

Cross-reference `output/state_summary_v2.csv` (protest_count ÷ existing_dc_count by state):

| State | Protests | Existing DCs | Ratio |
|---|---|---|---|
| Indiana | 30 | 4 | 7.50 |
| West Virginia | 7 | 1 | 7.00 |
| Kentucky | 9 | 3 | 3.00 |
| Pennsylvania | 17 | 7 | 2.43 |
| Michigan | 21 | 9 | 2.33 |
| Wisconsin | 16 | 8 | 2.00 |
| Missouri | 19 | 11 | 1.73 |
| Texas | 28 | 92 | 0.30 |
| California | 11 | 94 | 0.12 |
| Ohio | 7 | 56 | 0.12 |
| Virginia | 23 | 292 | 0.08 |

**Data-quality flag (resolved later, see next section)**: manually checking the 4 "Indiana" rows in IM3 showed only 2 were actual data centers (IU Data Center, Digital Crossroad); the other 2 were university buildings mis-tagged in OpenStreetMap ("Learning GIS!", an agricultural-engineering building at Purdue). External research (Data Center Frontier, 2026) found Indiana actually has **46 recorded data center projects, $28B+ in announced investment, 5 under construction** — none of these recent, major projects appear in IM3, because IM3 is derived from OpenStreetMap (crowd-sourced), which lags behind markets in the middle of a construction boom. **IM3 therefore structurally, and disproportionately, undercounts the newest markets, precisely the ones this analysis cares about most.** → IM3 dropped as the counting source, replaced by FracTracker (next section). IM3 is still used for the water-stress cross-reference, where point locations are sufficient and exhaustive state-level counts aren't critical.

## Replacement source: FracTracker U.S. Data Centers Tracker

Found while looking for a more reliable alternative to IM3, prompted by Benjamin after the Indiana check. FracTracker Alliance is an established environmental nonprofit (participatory mapping, validated, used for example by the Piedmont Environmental Council and Science for Georgia as data partners).

- Public dashboard: https://fractracker.org/data-centers-tracker/
- Underlying FeatureServer (found via the ArcGIS item behind the Web Experience, layer "Data Center Summary"): `https://services.arcgis.com/jDGuO8tYggdCCnUJ/arcgis/rest/services/data_centers_v4_agol_all/FeatureServer/0`
- Methodology: press, trade reports, public zoning/permitting records, FOIA requests, submissions from local advocacy groups, partner datasets. Claimed daily updates. Free non-commercial use.
- 1,670 US facilities recorded, with a detailed `status` field (Operating: 531, Proposed: 740, Approved/Permitted/Under construction: 174, Cancelled: 78, Suspended: 69, Expanding: 68, Pre-proposal: 10) — far more granular than IM3 (existing vs. project vs. cancelled).
- **A `community_pushback` field (Yes/Unknown) is directly in the data** — FracTracker itself tags each facility for documented local opposition. This field is independent of our ACLED extraction and can be used as a cross-check.
- Indiana check: **43 recorded facilities (vs. 46 from Data Center Frontier, consistent), only 7 of them "Operating."** Much closer to reality than IM3 (which counted only 4, 2 of them wrong).
- Local file: `data/raw/fractracker_data_centers_us.geojson`

### Protests-to-"Operating"-data-centers ratio (recalculated, more reliable)

| State | Protests | "Operating" DCs (FracTracker) | Ratio |
|---|---|---|---|
| Indiana | 30 | 7 | 4.29 |
| Michigan | 21 | 1 | 21.00 |
| Wisconsin | 16 | 2 | 8.00 |
| Minnesota | 8 | 1 | 8.00 |
| Kentucky | 9 | 2 | 4.50 |
| Missouri | 19 | 5 | 3.80 |
| Illinois | 12 | 5 | 2.40 |
| Tennessee | 9 | 4 | 2.25 |
| Texas | 28 | 62 | 0.45 |
| Pennsylvania | 17 | 40 | 0.42 |
| Georgia | 15 | 85 | 0.18 |
| Virginia | 23 | 180 | 0.13 |

Michigan and Wisconsin actually turn out to be the most extreme cases (ratio 21 and 8), more so than Indiana — a nuance worth keeping: Indiana remains the best media-documented example (see press-corroboration section), but the numbers no longer single it out as THE most extreme case, in the interest of accuracy.

### Independent cross-check: `community_pushback` (FracTracker) vs. our ACLED counts

With no link to our ACLED extraction, FracTracker tags each data center "pushback=Yes" or "Unknown." Share of "Yes" by state:

| State | % of facilities with documented opposition (FracTracker) |
|---|---|
| Wisconsin | 60% (12/20) |
| Michigan | 48% (13/27) |
| Missouri | 38% (13/34) |
| Indiana | 37% (16/43) |
| California | 32% (12/37) |
| Texas | 15% (32/214) |
| Georgia | 12% (22/180) |
| Virginia | 2.4% (11/463) |

**Two independent sources (our ACLED extraction and FracTracker's own `community_pushback` tag) converge**: Virginia, the most mature and densest market (463 recorded facilities), has by far the lowest contestation rate; the newer, fast-growing markets (Wisconsin, Michigan, Missouri, Indiana) have the highest. This is genuine triangulation, not an isolated number, a solid point for the final deliverable.

Practical consequence: replace the IM3 figures (`output/state_summary_v2.csv`, superseded) with `output/state_summary_v3_fractracker.csv` going forward. Headline, unchanged: **"contestation tracks the shock of change, not market saturation."**

## Second data-quality flag — FracTracker also has a coverage bias

Verification (prompted by Benjamin): Florida and Utah show up with 0 "Operating" data centers in FracTracker, which looked like it indicated untouched markets. External research: **false**. Florida has had major operational data centers since 2017 (Equinix Miami/NAP of the Americas, one of the most important connectivity hubs in the US); Utah since 2021 (Meta Eagle Mountain, 7 buildings, $1.5B invested). These well-known, well-documented facilities are simply absent from FracTracker.

**Conclusion: FracTracker, like IM3, has uneven state coverage, denser where its partner organizations are active (Virginia via the Piedmont Environmental Council, Georgia via Science for Georgia), thinner elsewhere.** Neither external source found so far is a reliable, exhaustive count of data centers by state.

**Final, methodologically defensible decision at this stage**: drop any precise count ("number of existing data centers per state") as a ratio denominator. Use instead the **FracTracker `community_pushback` rate (%)**, which is less sensitive to coverage gaps than an absolute count (it's a proportion within what's tracked, not a total), **with a reliability threshold of n≥10 recorded facilities per state** — below that threshold the data is too noisy to interpret (e.g. Hawaii, n=1, would show 0% or 100% with no real meaning), and the state is shown as "insufficient data" rather than silently hidden.

Result: 33 of 48 states with a reliable value, 15 below the threshold. The main story holds: Indiana 37.2%, Wisconsin 60%, Michigan 48.1%, Missouri 38.2% vs. Virginia 2.4%, Texas 15%, Georgia 12.2% — all comfortably above the reliability threshold. Final file at this stage: `output/flourish_map_data_final.csv` (columns: state, protest_count, n_facilities, pushback_pct, reliable, map_value).

**Limitation to state explicitly on the map/in the methodology text**: the `community_pushback` rate depends on FracTracker's coverage, denser in some states (notably those with identified local advocacy partners) — to be treated as an indicator, not a certified exhaustive measure. An acknowledged, documented limitation rather than a hidden one, consistent with the standard of rigor expected by ACLED.

## Third, final source: dcmap.us (US Data Center Map)

Found on Benjamin's suggestion (`https://dcmap.us/agent-api/v2/index.json`), a dedicated public JSON "agent API," state-level aggregates.

- Publisher: US Data Center Map (dcmap.us). Public methodology: https://dcmap.us/methodology/, monthly aggregation of public sources, standardized lifecycle categories (operational, construction, planned, paused, inactive).
- Endpoint used: `https://dcmap.us/agent-api/v2/states.json`, official state-level aggregates only (no individual rows/coordinates exposed by this API, deliberately, per their documented "access_boundary").
- **Citation required, no republishing as a database** (explicit usage policy), respected: we cite dcmap.us with a source link and republish only derived aggregates (ratios, percentages), not raw data.
- Local file: `data/raw/dcmap_us_states.json`. Data as of 2026-08-31.
- **Decisive check**: Florida = 123 operational, Utah = 50 operational, fully fixing the coverage gap found in FracTracker (which showed them at 0). This source is markedly more complete than both IM3 and FracTracker.
- Bonus: includes a `water_stress_level` field per state, roughly consistent with our own WRI Aqueduct analysis (no simple relationship; a mix of Low-Medium to High levels among the top-contestation states, confirming the absence of a linear link already found).

### Final ratio adopted (ACLED protests ÷ dcmap.us "operational" data centers)

| State | Operational | Protests | Ratio |
|---|---|---|---|
| Indiana | 59 | 30 | 0.508 |
| Arkansas | 17 | 8 | 0.471 |
| West Virginia | 17 | 7 | 0.412 |
| Wisconsin | 45 | 16 | 0.356 |
| Missouri | 56 | 19 | 0.339 |
| Michigan | 70 | 21 | 0.300 |
| Kentucky | 32 | 9 | 0.281 |
| Georgia | 114 | 15 | 0.132 |
| Minnesota | 49 | 8 | 0.163 |
| Tennessee | 73 | 9 | 0.123 |
| Virginia | 282 | 23 | 0.082 |
| Texas | 349 | 28 | 0.080 |
| New Jersey | 94 | 6 | 0.064 |
| Florida | 123 | 7 | 0.057 |
| Illinois | 138 | 12 | 0.087 |
| Ohio | 163 | 7 | 0.043 |
| California | 305 | 11 | 0.036 |

**This is the final version, used for the map.** The gap is more modest than the figures computed on IM3 or FracTracker (Indiana ≈6x Virginia, ≈14x California, not 90x as in the first, erroneous calculation), but this time built on a complete source with no coverage gaps and no artificial zeros. It is the most honest and defensible figure of the three versions produced during the exercise — the narrower gap compared with earlier versions doesn't invalidate the angle, it just makes it more rigorous.

Output file: `output/state_summary_v4_dcmap.csv`. This file (not `state_summary_v2.csv` or `state_summary_v3_fractracker.csv`, both superseded) is the one used as the basis for the Flourish map.

Tested variant: ratio on `planned` data centers instead of `operational` → `output/state_summary_v5_planned_ratio.csv` / `output/flourish_states_planned_ratio.geojson`. Slightly different ranking (Wisconsin leads at 2.29, then Michigan 1.40, Arkansas 1.33, Indiana 1.11) but the same qualitative reading.

**Final decision**: the map based on `operational` was kept for the deliverable, a more direct and intuitive story (an already-established industry vs. observed contestation) than the `planned` version, which requires explaining the notion of a project pipeline before it can be understood. The `planned` variant is kept as documented exploration, not used in the final deliverable.

**Robustness check**: ratio recalculated on `operational + planned` (total_dc) → `output/state_summary_v8_total_ratio.csv`, `ratio_total` property added to `flourish_states_with_data.geojson` for comparison. Same states lead (Indiana, Arkansas, Wisconsin, West Virginia, Michigan, Missouri, Kentucky) as with `operational` alone, the result doesn't hinge on the exact choice of denominator, which strengthens the credibility of the finding. `ratio` (operational alone) remains the metric used for the map; `ratio_total` is available in the tooltip for comparison.

## Weighting by crowd size (prompted by Benjamin)

Question raised: a ratio based on raw event counts treats a 15-person gathering the same as a 500-person one, a potential bias (e.g. Wisconsin had a high ratio without knowing whether it was driven by small or large gatherings).

Method: extract the `crowd size=` tag (from the `tags` column), weight using ACLED's own published bins (see [ACLED's crowd-size methodology](https://acleddata.com/methodology/how-crowd-size-protests-and-riots-coded-acled-data)): Very small <20, Small 20-99, Medium 100-999, Large 1,000-9,999, Massive ≥10,000. Weights used (bin midpoint or a conservative lower bound): very small=10, small=50, medium=500, large=5,000, massive=10,000.

**Important methodological limitation, stated in ACLED's own documentation**: *"Where the source and note contain no crowd size information, the event is labeled 'crowd size=small' by default."* So some of the 275/330 events tagged "small" may be of genuinely unknown size rather than verified as small. Weight applied to missing tags: 50 (as for "small"), consistent with ACLED's own default behavior.

**Result**: `output/state_summary_v6_weighted.csv`. The ranking shifts for low-n states (a single protest tagged "large" in a state with only 7 events inflates its score sharply, e.g. West Virginia jumps artificially to the top), so this **cannot be used as the map's primary metric without the same sample-size safeguard applied elsewhere.** For the states that carry the main story (sufficient n), the weighting confirms, and even sharpens, the gap: Wisconsin 56.9, Missouri 40.4, Michigan 32.0, Indiana 24.7 vs. Virginia 7.3, California 4.8.

**Decision**: keep the raw ratio (`state_summary_v4_dcmap.csv`) as the map's metric (stable, already set up in Flourish). Use the weighted ratio as a robustness argument in the accompanying text ("the result holds even when weighting by gathering size"), not as the basis for the map itself.

## Water-stress cross-reference (WRI Aqueduct 4.0)

Complementary external dataset: WRI Aqueduct 4.0, "Baseline Water Stress" (bws_cat), hosted on Esri Living Atlas.
- ArcGIS item: https://www.arcgis.com/home/item.html?id=c784f4ebddaf43c8b816612fb62e7e5b
- FeatureServer: `https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/aqueduct_water_risk/FeatureServer/1` ("Baseline Annual" layer)
- License CC BY 4.0, World Resources Institute. Data vintage April 2023. Aggregation unit: HydroBASINS level-6 sub-basins.
- Retrieved via paginated REST queries (the server silently caps at 750 features per request even when more are requested, paginated via `resultOffset` in steps of 750, up to 3,433 US basins total). Local file: `data/source/aqueduct_water_stress_us.geojson`.
- Spatial join (point-in-polygon, shapely/STRtree): `scripts/03_join_water_stress.py` → `output/protests_with_water_stress.csv` and `output/existing_dcs_with_water_stress.csv`.

**Result (honest, not the simple correlation one might expect)**:

| bws category | % of protests | % of existing data centers | Ratio |
|---|---|---|---|
| Low (<10%) | 29.7% | 37.1% | 0.80 |
| Low-Medium (10-20%) | 12.4% | 12.6% | 0.98 |
| Medium-High (20-40%) | 29.1% | 12.9% | **2.26** |
| High (40-80%) | 19.1% | 23.2% | 0.82 |
| Extremely High (>80%) | 9.7% | 14.1% | 0.69 |

No linear "more stress equals more contestation" relationship (the most extreme category is under-represented among protests relative to the existing data-center stock). The clear over-representation sits in the intermediate "Medium-High" category (×2.26). Hypothesis (to be framed as a hypothesis in the deliverable, not as established fact): contestation is sharpest where water stress is already real but not yet extreme or fully anticipated, consistent with the main "novelty/shock of change" angle rather than saturation or maximum objective risk.

## Press corroboration (web research) — our patterns already documented elsewhere

- **18 July 2026: a coordinated national day of action** organized by the HumansFirst movement (co-founded by a former Tea Party leader, so a cross-partisan movement), 142 protests across 42 states in a single day. This explains a good share of the July 2026 peak seen in our data (81/330 in that month alone): **this is not purely organic escalation, part of it is a one-off coordinated event**, an important point to avoid over-reading the curve. Sources: Spokesman, US News, Colorado Springs Gazette, SRN News (18-22 July 2026).
- **National poll (cited by wthr.com, 2026)**: ~70% of Americans now oppose the construction of AI data centers near them, a rare topic of cross-partisan consensus.
- **Data Center Watch (report, cited by costar.com and others, 2026)**: $64B in projects blocked or delayed by local opposition; 75 major projects ($130B) delayed or cancelled in Q1 2026 alone.
- **A concrete case confirming the water motive**: Newton County, Georgia, where a Meta data center dried up private wells and drove up municipal water prices, with a possible county water deficit by 2030 (Fortune, Time, 2026).
- **On Indiana specifically** (Latitude Media, Indiana Capital Chronicle, 2026): cross-partisan contestation, driven by electricity rates (NIPSCO accused of shifting industrial costs onto residential customers) and water, consistent with the dominant motives independently identified in `notes`.

Overall finding: the two dominant motives independently identified in ACLED's `notes` (water, electricity) are exactly the ones specialist press is documenting in real time on this phenomenon, a good validity signal for the analysis.

## Proximity to towns — on the data centers themselves (not the protests)

Method: distance from each of the 1,242 data centers (IM3 atlas) to the nearest incorporated town (source: a database of 29,881 US incorporated places, `data/source/us_incorporated_places.csv`, lat/lon only, no population, a limitation worth noting). A data center is flagged "with a nearby protest" if an ACLED protest event is within 10km.

| Group | N | Median distance to nearest town |
|---|---|---|
| DCs with a nearby protest (≤10km) | 226 | 2.87 km |
| DCs without a nearby protest | 1,016 | 3.74 km |

A real but modest effect (~1km gap in the median), geospatially corroborating what the text had already shown (only 7% of `notes` explicitly cite residential proximity): proximity to towns plays a secondary role, not the main driver of the phenomenon. Output: `output/dcs_with_town_distance.csv`.

## Proximity to towns at the regional (state) level

Reframed question: in states where data centers are, on average, closer to towns, is there more protest activity? Calculation: median distance from data centers (IM3 atlas) to the nearest town, by state (states with ≥5 data centers), set against protest counts and the protest-to-DC rate for that state.

| State | Median distance to a town | Protests | Protest/DC rate |
|---|---|---|---|
| New Jersey | 1.51 km (closest) | 6 | 0.128 |
| Virginia | 2.46 km | 23 | 0.079 |
| Missouri | 8.37 km | 19 | 1.727 |
| Nevada | 12.95 km (farthest) | 4 | 0.114 |

**Correlation, median distance vs. protest count: -0.12. Median distance vs. protest/DC rate: -0.11.** Essentially zero, no usable relationship. New Jersey (data centers closest to towns on average) has a low protest rate; Missouri (data centers relatively far from towns) has one of the highest rates. **A clean negative result: proximity to towns does not explain the regional distribution of contestation.** Dropped as an angle; what explains it better remains the market's novelty in a given state (protest/existing-DC ratio, Indiana vs. Virginia) and, to a lesser extent, water stress (the Medium-High category).

## Alternative angle considered, then dropped: Operation Metro Surge (immigration/ICE)

While looking for angles closer to ACLED's actual core business (conflict analysis, political violence), a very strong pattern turned up in the full US dataset: a January 2026 spike (1,889 immigration/ICE-related events in a single month, versus a usual 200-650/month).

An explanation was found both in ACLED's own `notes` and confirmed by the press: **Operation Metro Surge**, a large-scale DHS/ICE operation in Minneapolis-Saint Paul (Minnesota) in late 2025-2026, roughly 2,000-3,000 agents deployed, around 3,000 claimed arrests. On 7 January 2026, an ICE agent fatally shot a protester (Renee Good) and a Venezuelan man, triggering a wave of school walkouts and citizen protests, followed by a gradual withdrawal of federal agents (a troop movement documented as "Strategic developments" in ACLED, 4 and 20 February 2026), and then a national "No Kings 3" mobilization (100,000-200,000 people in Saint Paul, 28 March 2026).

**Why it was dropped despite the strength of the pattern**: the topic was already extensively covered by the general press (a dedicated Wikipedia page, live CNN coverage), a visualization on it would illustrate a story everyone already knows rather than demonstrating the ability to extract a non-obvious pattern. The data center angle, by contrast, doesn't appear in any structured field and hadn't been covered with this level of detail (motives, state ratio, water stress) in the press consulted, a better fit for what the exercise appears designed to evaluate: the ability to extract and narrate a non-obvious signal.

## Scope decisions (final)

- **Map**: 3D choropleth (Flourish "Region map") by state, ratio of protests to operational data centers (dcmap.us, `output/state_summary_v4_dcmap.csv`), the final, fully covered source with no state-by-state gaps. Height and color encode the same variable (visual reinforcement, not two different variables stacked). No individual point map (330 points across the US would be dense and hard to read for an external audience).
- **Additional chart**: a national monthly "circle timeline" (bubble scatter, one point per month, size = estimated turnout from ACLED's crowd-size tags), rather than a per-state breakdown. A per-state heatmap (42 rows) and a 42-line chart were both tried and dropped: too dense to read at a glance, and they duplicated the state-level comparison already carried by the map. The national timeline instead adds a genuinely different dimension (when, and at what scale), with the 18 July 2026 coordinated day of action noted as context so the peak isn't misread as pure organic growth.
- **Infographic / accompanying text**: the "contestation tracks the shock of change, not market saturation" angle (Indiana vs. Virginia), with the dominant motives (water, electricity) and an honest statement of the method's limits (the successive external-source corrections, the non-linear water-stress relationship, the ICE angle considered and set aside).
- No time allocated to an individual geolocated point map or an in-depth county-by-county analysis, out of scope for the 4-hour budget.
