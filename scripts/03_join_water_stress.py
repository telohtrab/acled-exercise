"""
Join protest events (and existing data centers) to WRI Aqueduct 4.0 baseline
water stress watersheds (point-in-polygon), via a local GeoJSON extract of the
Aqueduct FeatureServer (Baseline Annual layer) over the CONUS envelope.

Source: WRI Aqueduct 4.0, hosted on Esri Living Atlas
  https://www.arcgis.com/home/item.html?id=c784f4ebddaf43c8b816612fb62e7e5b
  FeatureServer: https://services.arcgis.com/P3ePLMYs2RVChkJx/arcgis/rest/services/aqueduct_water_risk/FeatureServer/1
  License: CC BY 4.0, World Resources Institute (WRI), data vintage April 2023.
  Aggregation unit: HydroBASINS level 6 sub-basins.

bws_cat (Baseline Water Stress, Category) scale: 0=Low, 1=Low-medium,
2=Medium-high, 3=High, 4=Extremely high (WRI standard categories).
"""
import json
import pandas as pd
from shapely.geometry import shape, Point
from shapely.strtree import STRtree

with open("data/source/aqueduct_water_stress_us.geojson", encoding="utf-8") as f:
    gj = json.load(f)

polys = []
props = []
for feat in gj["features"]:
    geom = shape(feat["geometry"])
    polys.append(geom)
    props.append(feat["properties"])

tree = STRtree(polys)


def lookup(lat, lon):
    pt = Point(lon, lat)
    idx = tree.query(pt, predicate="intersects")
    if len(idx) == 0:
        return None
    # take the first intersecting polygon (basins do not overlap)
    return props[idx[0]]


def join_df(df, lat_col, lon_col):
    bws_cat, bws_label, bws_raw, basin_name = [], [], [], []
    for lat, lon in zip(df[lat_col], df[lon_col]):
        res = lookup(lat, lon)
        if res is None:
            bws_cat.append(None); bws_label.append(None); bws_raw.append(None); basin_name.append(None)
        else:
            bws_cat.append(res.get("bws_cat"))
            bws_label.append(res.get("bws_label"))
            bws_raw.append(res.get("bws_raw"))
            basin_name.append(res.get("name_1"))
    df = df.copy()
    df["bws_cat"] = bws_cat
    df["bws_label"] = bws_label
    df["bws_raw"] = bws_raw
    df["basin_admin1"] = basin_name
    return df


protests = pd.read_csv("data/source/us_data_center_protests.csv")
protests_ws = join_df(protests, "latitude", "longitude")
protests_ws.to_csv("output/protests_with_water_stress.csv", index=False)

dcs = pd.read_csv("data/raw/im3_open_source_data_center_atlas/im3_open_source_data_center_atlas.csv")
dcs_ws = join_df(dcs, "lat", "lon")
dcs_ws.to_csv("output/existing_dcs_with_water_stress.csv", index=False)

print("=== Protestations par categorie de stress hydrique (lieu de la protestation) ===")
print(protests_ws["bws_label"].value_counts(dropna=False))
print()
print("=== Data centers EXISTANTS (tous, protestes ou non) par categorie de stress hydrique ===")
print(dcs_ws["bws_label"].value_counts(dropna=False))
