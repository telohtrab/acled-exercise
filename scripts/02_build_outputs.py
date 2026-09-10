"""
Build the tables used for the map, the chart and the infographic.

Inputs:
  data/source/us_data_center_protests.csv   (ACLED subset, 1 row = 1 event)
  data/source/state_incentive_tier.csv      (external data: state-level data
                                              center tax-incentive aggressiveness,
                                              transcribed from buildermuse.com 2026
                                              "Data Center Tax Incentives by State";
                                              states not listed there = "not documented")

Outputs:
  output/state_summary.csv   one row per state: protest count, incentive tier
  output/monthly_trend.csv   one row per month: protest count (US total)
"""
import pandas as pd

events = pd.read_csv("data/source/us_data_center_protests.csv")
tiers = pd.read_csv("data/source/state_incentive_tier.csv")

# --- state summary (for the map) ---
state_counts = (
    events.groupby("admin1")
    .size()
    .reset_index(name="protest_count")
    .rename(columns={"admin1": "state"})
)

state_summary = state_counts.merge(tiers, on="state", how="left")
state_summary["incentive_tier"] = state_summary["incentive_tier"].fillna("not_documented")
state_summary = state_summary.sort_values("protest_count", ascending=False)
state_summary.to_csv("output/state_summary.csv", index=False)

# --- monthly trend (for the chart) ---
events["event_date"] = pd.to_datetime(events["event_date"])
monthly = (
    events.set_index("event_date")
    .resample("MS")
    .size()
    .reset_index(name="protest_count")
    .rename(columns={"event_date": "month"})
)
monthly.to_csv("output/monthly_trend.csv", index=False)

print("state_summary.csv:", len(state_summary), "states")
print(state_summary.head(10).to_string(index=False))
print()
print("monthly_trend.csv:", len(monthly), "months")
