# Cyprus Weather and Electricity Prices Dataset

**An open dataset of weather observations for Limassol, Cyprus, joined with
30-minute Cyprus day-ahead electricity market clearing prices.**

Released as open data to support research and development in energy
systems, building optimization, weather forecasting, and electricity
market analysis in Cyprus and the broader Mediterranean region.

**License:** [CC0 1.0 Universal](LICENSE) — public domain, no attribution required.

---

## What's in this dataset

Three CSV files live under [`data/`](data/):

| File | Rows | Description |
| --- | --- | --- |
| [`weather_raw.csv`](data/weather_raw.csv) | ~9,700 | Weather observations at native cadence (approx. every 5–15 min) |
| [`prices_30min.csv`](data/prices_30min.csv) | ~5,000 | Cyprus day-ahead market clearing prices at 30-minute resolution |
| [`weather_prices_joined.csv`](data/weather_prices_joined.csv) | ~9,700 | Weather observations with the 30-minute market price for their window joined |

**Coverage window:** 1 January 2026 – mid April 2026.

**Location:** Limassol, Cyprus (single station).

---

## Quick start

```python
import pandas as pd

# Just the join — easiest for most use cases
df = pd.read_csv("data/weather_prices_joined.csv", parse_dates=["timestamp"])
print(df.head())
print(df.columns.tolist())
```

You will need `pandas` only. No credentials, no network, no API keys.

### One-line average price per day

```python
df = pd.read_csv("data/weather_prices_joined.csv", parse_dates=["timestamp"])
daily = (df.set_index("timestamp")["price_eur_per_mwh"]
           .resample("D").mean())
print(daily.head())
```

A minimal `load_dataset.py` example is included under [`loader/`](loader/)
if you prefer to copy-paste a script.

---

## Data dictionary

### `weather_raw.csv` and `weather_prices_joined.csv`

| Column | Type | Description |
| --- | --- | --- |
| `timestamp` | datetime (UTC) | Observation time |
| `weather_text` | string | Short human-readable weather phrase (`sunny`, `mostly cloudy`, etc.) |
| `has_precipitation` | bool | True if any precipitation is being observed |
| `precipitation_type` | string | `rain`, `snow`, `ice` or `None` |
| `is_daytime` | bool | True if the observation is during local daylight |
| `temp_c` | float | Ambient dry-bulb air temperature (°C) |
| `realfeel_temp_c` | float | AccuWeather RealFeel® temperature (°C) |
| `apparent_temp_c` | float | Apparent temperature incorporating wind and humidity (°C) |
| `relative_humidity` | int | Relative humidity (%) |
| `dewpoint_c` | float | Dew-point temperature (°C) |
| `wind_direction_degrees` | int | Wind direction in degrees (meteorological convention) |
| `wind_direction_localized` | string | Cardinal direction (`n`, `nne`, `ne`, ...) |
| `wind_speed_kmh` | float | Wind speed (km/h) |
| `wind_gust_kmh` | float | Peak wind gust (km/h) |
| `uv_index` | int | UV index (0 = none, 11+ = extreme) |
| `uv_index_text` | string | Categorical UV level (`low`, `moderate`, ...) |
| `cloud_cover_perc` | int | Cloud cover percentage (0–100) |
| `cloud_ceiling_m` | float | Cloud ceiling altitude in metres |
| `pressure_mb` | float | Atmospheric pressure at sea level (millibar / hPa) |
| `wetbulb_temp_c` | float | Wet-bulb temperature (°C) |

The `weather_prices_joined.csv` file additionally contains:

| Column | Type | Description |
| --- | --- | --- |
| `price_period_start` | datetime (UTC) | Start of the 30-minute market window |
| `price_period_end` | datetime (UTC) | End of the 30-minute market window |
| `price_eur_per_mwh` | float | Day-ahead market clearing price for that window (EUR/MWh) |
| `total_sales_mwh` | float | Total energy sold into the market during that window (MWh), summed across energy categories |
| `total_purchase_mwh` | float | Total energy purchased during that window (MWh), summed across categories |

### `prices_30min.csv`

One row per 30-minute market window. The Cyprus day-ahead market has a
single clearing price per window that applies to all generators and
consumers.

| Column | Type | Description |
| --- | --- | --- |
| `period_start` | datetime (UTC) | Start of the 30-minute window |
| `period_end` | datetime (UTC) | End of the 30-minute window |
| `price_eur_per_mwh` | float | Market clearing price (EUR/MWh) |
| `total_sales_mwh` | float | Total energy sold into the market during that window (MWh) |
| `total_purchase_mwh` | float | Total energy purchased during that window (MWh) |
| `n_categories` | int | Number of energy categories (e.g. conventional, solar) that reported for this window — useful for data-quality checks |

---

## Data sources

* **Weather.** AccuWeather observations for a single Limassol station,
  posted at the provider's native cadence (typically every 5–15 minutes).
  No interpolation or smoothing is applied — raw provider observations
  are exported as-is.
* **Prices.** Cyprus day-ahead market clearing prices. Each 30-minute
  window has a single clearing price that applies uniformly across all
  generation technologies. Sales and purchase volumes are aggregated
  across all reported categories into a single total per window.
* **Join logic.** Each weather observation is matched to the most
  recent price window whose `period_start` ≤ the observation timestamp,
  using `pandas.merge_asof` with a 30-minute tolerance. This labels
  every weather row with the price that was in effect at the moment
  of observation.

---

## How to cite

Attribution is not required. If you would still like to credit the
dataset, a plain-text citation such as *"Cyprus Weather and Electricity
Prices Dataset"* is sufficient.

---

## Licence

Released into the public domain under
[CC0 1.0 Universal](https://creativecommons.org/publicdomain/zero/1.0/).
You are free to copy, modify, distribute, and use the data for any
purpose — commercial or otherwise — without asking permission, without
paying, and without attribution. The dataset is provided *as is* with
no warranty.
