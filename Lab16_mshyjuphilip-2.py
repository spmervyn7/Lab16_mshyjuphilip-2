"""
Program Name: Lab16_mshyjuphilip-2.py
Author: Mervyn S. Philip
Purpose: Reads fire detection data from world_fires_1_day.csv and plots
         the fire locations on an interactive world map using plotly.
         Fire brightness is mapped to marker color (with a color bar),
         and while moving the mouse cursor over any fire dot on the 
         interactive map, a small pop-up box will appear showing the 
         exact date the fire was detected.
Starter Code: No starter code was used; written from scratch based on
              Lab 16 (Option 2) assignment instructions
Date: August 5, 2026
"""

import csv
import plotly.express as px
import plotly.graph_objects as go


def parse_fire_row(row):
    """Convert one CSV row (list of strings) into a validated data tuple.

    Returns (latitude, longitude, brightness, date) as
    (float, float, float, str), or None if the row has invalid data.
    """
    latitude = float(row["latitude"])
    longitude = float(row["longitude"])
    brightness = float(row["brightness"])
    date = row["acq_date"]
    return latitude, longitude, brightness, date


def build_hover_text(date, brightness):
    """Build a single hover-text label for one fire data point."""
    return f"Date: {date}<br>Brightness: {brightness:.1f}"


def read_fire_data(csv_path, max_entries = 1000):
    """Read fire data from a CSV file using the csv module.

    Only the first `max_entries` valid data rows are processed, to keep
    the resulting map readable. Uses a try-except-else block per row so
    a single malformed row does not crash the whole read.

    Returns four parallel lists: lats, lons, brightness_values, dates.
    """
    lats = []
    lons = []
    brightness_values = []
    dates = []

    with open(csv_path, newline = "", encoding = "utf-8") as csv_file:
        reader = csv.DictReader(csv_file)

        for row in reader:
            if len(lats) >= max_entries:
                break

            try:
                latitude, longitude, brightness, date = parse_fire_row(row)
            except (ValueError, KeyError):
                # Skip rows with missing fields or bad numeric data
                continue
            else:
                lats.append(latitude)
                lons.append(longitude)
                brightness_values.append(brightness)
                dates.append(date)

    return lats, lons, brightness_values, dates


def save_map(figure, output_path):
    """Save a plotly Figure to an interactive HTML file."""
    figure.write_html(output_path)


def create_fire_map(lats, lons, brightness_values, dates, title="Global Fires"):
    """Build a plotly Figure showing fires on a world map.

    Marker color represents brightness (with a color bar), and hover
    text shows the acquisition date and brightness for each point.
    """
    hover_texts = [
        build_hover_text(date, brightness)
        for date, brightness in zip(dates, brightness_values)
    ]

    data = [
        go.Scattergeo(
            lon = lons,
            lat = lats,
            text = hover_texts,
            hoverinfo = "text",
            mode = "markers",
            marker = dict(
                size = 6,
                color = brightness_values,
                colorscale = px.colors.sequential.Bluered_r,
                colorbar = dict(title = "Brightness"),
                line = dict(width = 0),
            ),
        )
    ]

    layout = go.Layout(title = title, geo = dict(showland = True))

    return go.Figure(data = data, layout = layout)


def main():
    """Wire together reading, transforming, and saving the fire map."""
    input_csv_path = "world_fires_1_day.csv"
    output_html_path = "global_fires.html"
    max_entries = 1000

    lats, lons, brightness_values, dates = read_fire_data(
        input_csv_path, max_entries = max_entries
    )

    fire_map = create_fire_map(
        lats, lons, brightness_values, dates, title = "Global Fires"
    )

    save_map(fire_map, output_html_path)


if __name__ == "__main__":
    main()