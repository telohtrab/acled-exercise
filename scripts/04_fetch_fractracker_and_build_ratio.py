"""
Fetch the FracTracker Alliance "U.S. Data Centers Tracker" (replaces the IM3
atlas as denominator source — IM3/OSM was found to undercount fast-growing
new markets like Indiana, see specs/exploration-log.md).

Source: FracTracker Alliance, https://fractracker.org/data-centers-tracker/
FeatureServer (found via the ArcGIS Web Experience item's embedded webmap):
  https://services.arcgis.com/jDGuO8tYggdCCnUJ/arcgis/rest/services/data_centers_v4_agol_all/FeatureServer/0
Methodology: news, permits/zoning filings, FOIA requests, advocacy-group and
partner submissions (e.g. Piedmont Environmental Council, Science for Georgia).
Non-commercial reuse permitted.
"""
import requests
import json
import numpy as np
import pandas as pd

URL = "https://services.arcgis.com/jDGuO8tYggdCCnUJ/arcgis/rest/services/data_centers_v4_agol_all/FeatureServer/0/query"

ABBR_TO_NAME = {
    'AL': 'Alabama', 'AK': 'Alaska', 'AZ': 'Arizona', 'AR': 'Arkansas', 'CA': 'California',
    'CO': 'Colorado', 'CT': 'Connecticut', 'DE': 'Delaware', 'FL': 'Florida', 'GA': 'Georgia',
    'HI': 'Hawaii', 'ID': 'Idaho', 'IL': 'Illinois', 'IN': 'Indiana', 'IA': 'Iowa', 'KS': 'Kansas',
    'KY': 'Kentucky', 'LA': 'Louisiana', 'ME': 'Maine', 'MD': 'Maryland', 'MA': 'Massachusetts',
    'MI': 'Michigan', 'MN': 'Minnesota', 'MS': 'Mississippi', 'MO': 'Missouri', 'MT': 'Montana',
    'NE': 'Nebraska', 'NV': 'Nevada', 'NH': 'New Hampshire', 'NJ': 'New Jersey', 'NM': 'New Mexico',
    'NY': 'New York', 'NC': 'North Carolina', 'ND': 'North Dakota', 'OH': 'Ohio', 'OK': 'Oklahoma',
    'OR': 'Oregon', 'PA': 'Pennsylvania', 'RI': 'Rhode Island', 'SC': 'South Carolina',
    'SD': 'South Dakota', 'TN': 'Tennessee', 'TX': 'Texas', 'UT': 'Utah', 'VT': 'Vermont',
    'VA': 'Virginia', 'WA': 'Washington', 'WV': 'West Virginia', 'WI': 'Wisconsin', 'WY': 'Wyoming',
    'DC': 'District of Columbia',
}


def fetch_all():
    # ArcGIS FeatureServer paginates regardless of resultRecordCount, so loop
    # on resultOffset until an empty page confirms we've reached the end.
    all_features, offset = [], 0
    while True:
        params = {
            "where": "1=1", "outFields": "*", "returnGeometry": "true",
            "f": "geojson", "resultOffset": offset, "resultRecordCount": 1000,
        }
        r = requests.get(URL, params=params, timeout=60)
        feats = r.json().get("features", [])
        all_features.extend(feats)
        if len(feats) == 0:
            break
        offset += 1000
    return {"type": "FeatureCollection", "features": all_features}


gj = fetch_all()
with open("data/raw/fractracker_data_centers_us.geojson", "w", encoding="utf-8") as f:
    json.dump(gj, f)

df = pd.DataFrame([feat["properties"] for feat in gj["features"]])
df["state_name"] = df["state"].map(ABBR_TO_NAME)
df["pushback_yes"] = df["community_pushback"].fillna("").str.strip().str.lower() == "yes"

operating = df[df["status"] == "Operating"]
by_state_operating = operating.groupby("state_name").size().rename("operating_dc_count")

protests = pd.read_csv("data/source/us_data_center_protests.csv")
protest_by_state = protests.groupby("admin1").size().rename("protest_count")

merged = pd.concat([protest_by_state, by_state_operating], axis=1).fillna(0)
merged["operating_dc_count"] = merged["operating_dc_count"].astype(int)
merged["protest_count"] = merged["protest_count"].astype(int)
merged["ratio"] = (merged["protest_count"] / merged["operating_dc_count"].replace(0, np.nan)).round(2)
# Note: this ratio was later replaced by the dcmap.us version (fuller state
# coverage, see specs/exploration-log.md); the community_pushback rate below
# remains part of the final cross-validation.
merged = merged.sort_values("protest_count", ascending=False)
merged.to_csv("output/state_summary_v3_fractracker.csv")

pushback_rate = df.groupby("state_name")["pushback_yes"].mean().rename("pushback_rate")
pushback_n = df.groupby("state_name").size().rename("n_facilities")
pd.concat([pushback_n, pushback_rate], axis=1).sort_values("pushback_rate", ascending=False).to_csv(
    "output/state_pushback_rate_fractracker.csv"
)

print("N total FracTracker:", len(df))
print(merged.head(15).to_string())
