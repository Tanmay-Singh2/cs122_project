from flask import Flask, render_template, request
import requests
import folium
from datetime import datetime
from zoneinfo import ZoneInfo
import pandas as pd
import matplotlib
matplotlib.use('Agg') 
import matplotlib.pyplot as plt
import seaborn as sns
import os, glob

app = Flask(__name__)

def fetch_flights():
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
    df.to_csv(f"data/csv/flights_{timestamp}.csv", index=False)

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
        df = df[(df.lat >= 18) & (df.lat <= 72) & (df.lon >= -170) & (df.lon <= -66)]
        if limit != "all":
            try:
                n = int(limit)
                df = df.sample(min(n, len(df)), random_state=1)
            except:
                df = df.sample(200, random_state=1)

    center = [37.8, -96] if view=="us" else [20, 0]
    zoom   = 4 if view=="us" else 2
    fmap   = folium.Map(location=center, zoom_start=zoom, tiles="CartoDB positron")

    for _, f in df.iterrows():
        icon_html = (
            f"<div style='transform: rotate({f.heading}deg); font-size:18px; color:{get_color(f.alt_ft)};'>&#9992;</div>"
        )
        folium.Marker(
            [f.lat, f.lon],
            icon=folium.DivIcon(html=icon_html),
            popup=f"<b>Flight:</b> {f.callsign}"
        ).add_to(fmap)

    pac = datetime.now(ZoneInfo("America/Los_Angeles")).strftime("%Y-%m-%d %I:%M:%S %p %Z")
    title = "Airline US Map" if view=="us" else "Airline World Map"
    fmap.get_root().html.add_child(folium.Element(
        f"<h3 style='text-align:center; font-family:Arial,sans-serif; color:#333'>{title} — Last update {pac}</h3>"
    ))

    return render_template("index.html",
        map_html=fmap._repr_html_(),
        current_view=view,
        current_limit=limit
    )

@app.route("/analysis")
def analysis_home():
    return render_template("analysis.html")

@app.route("/analysis/top-countries")
def analysis_top_countries():
    files = sorted(glob.glob("data/csv/*.csv"))
    if not files:
        return "No data files found"
    df = pd.read_csv(files[-1])
    top = df["origin_country"].value_counts().head(10)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=top.values, y=top.index, palette="coolwarm")
    plt.title("Top 10 Countries by Number of Flights")
    plt.xlabel("Flights")
    plt.tight_layout()
    plt.savefig("static/flight_analysis.png")
    plt.close()

    return render_template("result.html", title="Top 10 Countries by Flights")

@app.route("/analysis/flight-volume")
def analysis_flight_volume():
    import glob

    # Step 1: Load the latest CSV
    files = sorted(glob.glob("data/csv/*.csv"))
    if not files:
        return "No data snapshots found!"

    df = pd.read_csv(files[-1])

    # Step 2: Create altitude bucket column based on alt_ft
    def classify_altitude(alt_ft):
        if alt_ft < 1000: return "< 1,000 ft"
        elif alt_ft < 5000: return "1,000–4,999 ft"
        elif alt_ft < 10000: return "5,000–9,999 ft"
        elif alt_ft < 20000: return "10,000–19,999 ft"
        elif alt_ft < 30000: return "20,000–29,999 ft"
        elif alt_ft < 40000: return "30,000–39,999 ft"
        else: return "40,000+ ft"

    df["alt_bucket"] = df["alt_ft"].apply(classify_altitude)

    # Step 3: Count how many flights per bucket
    bucket_counts = df["alt_bucket"].value_counts().reindex([
        "< 1,000 ft", "1,000–4,999 ft", "5,000–9,999 ft", 
        "10,000–19,999 ft", "20,000–29,999 ft", 
        "30,000–39,999 ft", "40,000+ ft"
    ], fill_value=0)

    # Step 4: Plot the bar chart
    plt.figure(figsize=(10, 6))
    sns.barplot(x=bucket_counts.index, y=bucket_counts.values, palette="viridis")
    plt.xlabel("Altitude Range")
    plt.ylabel("Number of Flights")
    plt.title("Flights by Altitude Bucket")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("static/flight_analysis.png")
    plt.close()

    return render_template("result.html", title="Flights by Altitude Bucket")

@app.route("/analysis/density")
def analysis_density():
    import glob
    import cartopy.crs as ccrs
    import cartopy.feature as cfeature

    files = sorted(glob.glob("data/csv/*.csv"))
    if not files:
        return "No data snapshots found!"

    df = pd.read_csv(files[-1])
    df = df.dropna(subset=["lat", "lon"])

    # Set up the figure and map
    plt.figure(figsize=(14, 7))
    ax = plt.axes(projection=ccrs.PlateCarree())
    ax.set_global()

    # Add map features
    ax.coastlines(linewidth=1)
    ax.add_feature(cfeature.BORDERS, edgecolor='black', linestyle=':')
    ax.add_feature(cfeature.LAND, facecolor='#f0f0f0')
    ax.add_feature(cfeature.OCEAN, facecolor='#a6cee3')
    ax.add_feature(cfeature.LAKES, facecolor='#a6cee3')
    ax.add_feature(cfeature.RIVERS)

    # Gridlines + ticks
    gl = ax.gridlines(draw_labels=True, linestyle="--", linewidth=0.5, color='gray')
    gl.top_labels = gl.right_labels = False

    # KDE Heatmap overlay
    sns.kdeplot(
        x=df["lon"], y=df["lat"],
        fill=True, cmap="plasma", levels=100, thresh=0.01,
        alpha=0.7, ax=ax, transform=ccrs.PlateCarree()
    )

    # Title and layout
    plt.title("Global Flight Density Heatmap", fontsize=16, weight='bold', pad=20)
    plt.tight_layout()
    plt.savefig("static/flight_analysis.png", dpi=150)
    plt.close()

    return render_template("result.html", title="Global Flight Density Heatmap")


if __name__ == "__main__":
    app.run(debug=True)
