# CS 122 Project: Airline Traffic Data and Air Traffic Analysis

## Authors:
Tanmay Singh   
Khushi Chandra

## Description:

Through this project, we aim to design an interactive Python-based application with a custom GUI designed to analyze and visualize real-time air traffic data using the OpenSky Network. The interface would enable users to access live web data from the OpenSky Network data. Our plan is to scrape the web data and locally organize the aircraft information for further analysis (in potentially csv files). The application aims to focus on three core analytical components: comparing air traffic patterns between major cities and states, detecting congestion levels near busy airports, and identifying air traffic volume trends over time. Through easy-to-understand visualizations such as heatmaps, line charts, and interactive maps, the tool will provide users with insights into global airspace dynamics. 

## Project Outline

- **Project Goal:** Create an interactive Python application to analyze and visualize real-time air traffic data.  
- **Data Source:** OpenSky Network API for live aircraft tracking data.  
- **GUI Framework:** Tkinter   
- **Key Features:**
  - Fetch live flight data and store it locally.
  - Compare air traffic patterns across cities and states.
  - Detect congestion near major airports.
  - Analyze trends in air traffic volume over time.
- **Visualization Tools:** Matplotlib, Seaborn, and Folium for charts, heatmaps, and interactive maps.  
- **Storage Format:** CSV and JSON files for efficient data management.  

## Detailed Project Plan and Outline:

### Interface Plan (Tanmay Singh and Khushi Chandra)

For the Interface plan we plan on using the Tkinter library of Python and develop a python GUI framework. The GUI will offer an intuitive and user-friendly layout where users can input locations (cities or states), select time ranges, and choose analysis modes such as traffic comparison, airport congestion, or volume trends. Through the GUI, we aim to implement real-time updates and refresh functionality to ensure the interface remains current without overwhelming the user with data. Additional interface features may include dropdowns for selecting airports, buttons for toggling between visualizations, and a dynamic map display for viewing aircraft positions and congestion zones in real-time (not super sure about the full layout yet).

### Data Collection and Storage Plan (Tanmay Singh)

- **Collect data using the OpenSky Network API**  
  I will use the OpenSky Network's REST API and Python client to access real-time flight data.

- **Filter data by key parameters**  
  The data will be pulled based on important criteria such as national boundaries and specific airport codes.

- **Scrape and update data regularly**  
  I plan to set up regular scraping intervals to keep the data fresh and continuously updated.

- **Store data locally in CSV and JSON formats**  
  The scraped data will be saved in local files using CSV and JSON formats for easy access and backup.

- **Use Pandas for data storage and manipulation**  
  I will load the data into Pandas DataFrames to analyze it efficiently without constantly querying the API.

- **Preserve important flight metadata**  
  Key information like timestamps, origin countries, altitudes, and speeds will be kept for analysis.

- **Save historical snapshots for trend analysis**  
  When needed, I will store historical copies of the data to help track changes and identify long-term patterns.

Here is a link to the OpenSky website: https://opensky-network.org/

### Data Analysis and Visualization Plan (Khushi Chandra)

For our analysis, we will utilize Python’s Pandas, NumPy, and SciPy libraries to process and analyze air traffic data efficiently. The three core aspects of our analysis include:

- **Traffic Comparison**: We will calculate aircraft density and movement patterns in different regions, comparing air traffic between cities and states in the U.S. Statistical methods will be applied to identify significant differences.

- **Airport Congestion Analysis**: By tracking the number of flights approaching major airports throughout the day, we will pinpoint peak congestion hours and assess potential bottlenecks.

- **Trend Analysis**: Using historical data, we will visualize air traffic volume fluctuations over different times of the day and across multiple days to detect seasonal or weekly patterns.

For visualization, we will employ Matplotlib, Seaborn, and Folium to generate:

- Heatmaps representing air traffic density over time.

- Line charts illustrating trends in air traffic volume.

- Interactive maps displaying real-time aircraft locations and congestion zones.

These visualizations will help users easily interpret complex air traffic patterns and make data-driven conclusions.

