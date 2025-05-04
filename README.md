# ✈️ CS 122 Project: Airline Traffic Data and Air Traffic Analysis

## 👩‍💻 Authors
- Tanmay Singh  
- Khushi Chandra

## 📌 Overview

This project is a Python web application that analyzes and visualizes real-time air traffic data using the [OpenSky Network API](https://opensky-network.org/). It features a dynamic aircraft map and a multi-option analysis dashboard that helps users understand flight trends globally.

Live data is fetched directly from the web and saved as timestamped CSV files. These snapshots are then analyzed using Pandas and visualized using Matplotlib, Seaborn, and Cartopy.

---

## 🧩 Project Components

### Interface
- Built with Flask
- Pages:
  - `/` — Interactive aircraft map
  - `/analysis` — Analysis dashboard with buttons for visualization options
- Widgets: map filters, analysis buttons, reload button

### Data Collection (Tanmay Singh)
- Pulls live flight data from OpenSky’s public API
- Filters and processes into structured CSVs in `data/csv/`
- Stores metadata like callsign, origin, altitude, speed, lat/lon
- Snapshots saved automatically on each page visit

### Data Analysis & Visualization (Khushi Chandra)

Three visualizations were developed:

1. **Flights by Altitude Bucket**  
   Groups aircraft into altitude ranges (e.g., `<1,000 ft`, `10,000–19,999 ft`) and displays a bar chart.

2. **Top Countries by Flight Origin**  
   Aggregates flight counts by country and plots the top 10 as a horizontal bar chart.

3. **Flight Density Heatmap**  
   Uses latitude and longitude of planes to generate a KDE heatmap overlayed on a world map, showing air traffic hotspots.

---

## 🛠️ Technologies Used

- **Backend:** Flask, Requests
- **Data Analysis:** Pandas, NumPy
- **Visualization:** Matplotlib, Seaborn, Folium, Cartopy
- **Data Format:** CSV
- **Live Data Source:** [OpenSky Network API](https://opensky-network.org/)

---

