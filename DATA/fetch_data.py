"""
fetch_data.py - Week 8: get data from an API and save it as DATA/raw.csv.

Run it:  python fetch_data.py
"""

from pathlib import Path
import pandas as pd
import requests


url = "https://earthquake.usgs.gov/fdsnws/event/1/query"

params = {
    "format": "geojson",
    "minmagnitude": 2.5,
    "limit": 500
}

records_key = "features"

rename = {
    "properties_mag": "magnitude",
    "properties_place": "place",
    "properties_time": "time",
    "properties_tsunami": "tsunami",
    "properties_sig": "significance",
    "properties_type": "type"
}

keep = [
    "magnitude",
    "place",
    "time",
    "tsunami",
    "significance",
    "type"
]

must_have = ["place"]

raw_file = Path(__file__).parent / "DATA" / "raw.csv"


def get_data(url, params):
    try:
        response = requests.get(url, params=params, timeout=15)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        print("Could not get the data:", error)
        return None


def make_table(data, records_key):
    records = data[records_key] if records_key else data
    return pd.json_normalize(records, sep="_")


def tidy_data(df):
    df = df.drop(columns=["type"])
    df = df.rename(columns=rename)
    df = df[keep]
    df = df.dropna(subset=must_have)
    return df


def save_data(df, path):
    path.parent.mkdir(exist_ok=True)
    df.to_csv(path, index=False)
    print(f"Saved {len(df)} rows to {path}")


if __name__ == "__main__":
    data = get_data(url, params)

    if data is not None:
        table = make_table(data, records_key)
        table = tidy_data(table)
        print(table.head())
        save_data(table, raw_file)
