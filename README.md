# The Data Center Backlash

Technical exercise for the ACLED Visualization and Digital Communication Specialist application (4-hour time limit, 2026-09-10). Not an official ACLED publication.

**Live page:** https://telohtrab.github.io/acled-exercise/

## Objective

Given a choice of two ACLED datasets (US protests or Sahel conflict events), identify a real pattern, enrich it with an external dataset, and produce a map, an additional chart, and an infographic explaining the finding for an external audience.

## Finding

Protests against US data center construction have surged since late 2025. The states seeing the most contestation relative to their footprint aren't the industry's biggest hubs (Virginia, Texas), they're the newest ones (Indiana, Wisconsin, Michigan). Indiana draws roughly six times more protests per existing data center than Virginia. Population, water stress, and proximity to cities were tested and don't explain the gap.

## Data sources

- **ACLED** — US event data, January 2024–August 2026. The data center subset (330 events) was extracted by keyword match on free-text event notes, since topic isn't a structured field.
- **dcmap.us** (US Data Center Map) — state-level counts of operational/planned data centers, used as the external dataset for the map's ratio. Two earlier sources (IM3/PNNL, FracTracker) were tried first and dropped for coverage gaps; see the exploration log for why.
- **WRI Aqueduct 4.0** — water-stress cross-reference (secondary finding).

## Tools

Python (pandas, shapely, scipy) for extraction and analysis · Flourish for the map and chart · Blender (Cycles) for the bonus 3D terrain infographic · plain HTML/CSS for the page, styled with ACLED's own brand colors and typeface.

## Process

The full, honest trail — including two wrong turns on the external data source, hypotheses tested and ruled out (population, water stress, city proximity), and one strong pattern (immigration-enforcement protests) found and deliberately set aside — is documented in [`specs/exploration-log.md`](specs/exploration-log.md).

## Repository structure

```
data/raw/        original + fetched source data
data/source/     cleaned/derived inputs (protest subset, boundaries, population)
data/archive/    superseded sources, kept for traceability
output/          final tables and GeoJSON used in Flourish
output/archive/  intermediate/dropped versions, kept for traceability
scripts/         extraction and join scripts, commented
blender/         heightmaps, US mask, the Blender scene (terrain, materials, camera), and the Affinity Designer source used to compose the bonus 3D infographic (labels, title, source line)
specs/           exploration log and ACLED codebook notes
assets/          logo and the bonus infographic export
index.html       the page itself
```
