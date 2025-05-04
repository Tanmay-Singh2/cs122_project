from flask import Flask, render_template, request
import requests
import folium
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd

app = Flask(__name__)

import os

def fetch_flights():
    # Fetch flight data
    resp = requests.get("https://opensky-network.org/api/states/all", timeout=10)
    raw = resp.json().get("states", [])
    cols = [
        "icao24","callsign","origin_country","time_pos","last_contact","lon",
        "lat","baro_altitude","on_ground","velocity","heading","vertical_rate",
        "sensors","geo_altitude","squawk","spi","position_source"
    ]
    df = pd.DataFrame(raw, columns=cols)
    df["callsign"] = df.callsign.str.strip().fillna("N/A")
    df = df.dropna(subset=["lat", "lon"])
    df["alt_ft"] = (df.baro_altitude.fillna(0) * 3.28084).round().astype(int)
    df["heading"] = df.heading.fillna(0)

    timestamp = datetime.now(ZoneInfo("UTC")).strftime("%Y%m%d_%H%M%S")
    os.makedirs("data/csv", exist_ok=True)
    filepath = f"data/csv/flights_{timestamp}.csv"
    df.to_csv(filepath, index=False)

    return df


def get_color(alt_ft):
    if   alt_ft < 1000:  return "#ff4500"
    elif alt_ft < 5000:  return "#ffa500"
    elif alt_ft < 10000: return "#9acd32"
    elif alt_ft < 20000: return "#00ced1"
    elif alt_ft < 30000: return "#1e90ff"
    elif alt_ft < 40000: return "#8a2be2"
    else:                 return "#ff00ff"

@app.route("/")
def index():
    view  = request.args.get("view",  "us")       
    limit = request.args.get("limit", "200")      

    df = fetch_flights()

    if view == "us":
        # include continental US + Alaska & Hawaii
        df = df[
            (df.lat  >= 18)  & (df.lat  <= 72) &
            (df.lon >= -170) & (df.lon <= -66)
        ]
        if limit != "all":
            try:
                n = int(limit)
            except ValueError:
                n = 200
            if len(df) > n:
                df = df.sample(n, random_state=1)
    # else view=="world":  no limit, show all flights

    center = [37.8, -96] if view=="us" else [20, 0]
    zoom   = 4 if view=="us" else 2
    fmap   = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")

    for _, f in df.iterrows():
        icon_html = (
            f"<div style='transform: rotate({f.heading}deg); "
            f"font-size:18px; color:{get_color(f.alt_ft)};'>&#9992;</div>"
        )
        folium.Marker(
            [f.lat, f.lon],
            icon=folium.DivIcon(html=icon_html),
            popup=f"<b>Flight:</b> {f.callsign}"
        ).add_to(fmap)

    pac = datetime.now(ZoneInfo("America/Los_Angeles"))\
           .strftime("%Y-%m-%d %I:%M:%S %p %Z")
    title = "Airlind US Map" if view=="us" else "Airlind World Map"
    fmap.get_root().html.add_child(folium.Element(
        f"<h3 style='text-align:center; font-family:Arial,sans-serif; color:#333'>"
        f"{title} — Last update {pac}"
        f"</h3>"
    ))

    return render_template("index.html",
        map_html      = fmap._repr_html_(),
        current_view  = view,
        current_limit = limit
    )

@app.route("/analysis")
def analysis():
    return render_template("analysis.html")

if __name__ == "__main__":
    app.run(debug=True)
