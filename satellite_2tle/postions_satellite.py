from skyfield.api import load, EarthSatellite
from datetime import datetime, timedelta
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

# Load TLE data
tle_line1 = "1 25544U 98067A   21294.51782528  .00000606  00000-0  17507-4 0  9990"
tle_line2 = "2 25544  51.6416  33.2522 0003490 102.5680 257.5957 15.48907855286238"
satellite = EarthSatellite(tle_line1, tle_line2, 'ISS')

# Load timescale
ts = load.timescale()

# Get current time
current_time = ts.now()

# Calculate satellite position
geocentric = satellite.at(current_time)
subpoint = geocentric.subpoint()

print(f"Satellite Position at {current_time.utc_datetime()}:")
print(f"Latitude: {subpoint.latitude.degrees:.4f}°")
print(f"Longitude: {subpoint.longitude.degrees:.4f}°")
print(f"Altitude: {subpoint.elevation.km:.2f} km")

# Predict positions for the next 90 minutes (every 10 seconds)
future_times = [current_time + timedelta(seconds=i).total_seconds() / 86400 for i in range(0, 5400, 10)]
future_positions = []

for time in future_times:
    geocentric = satellite.at(time)
    subpoint = geocentric.subpoint()
    future_positions.append({
        "time": time.utc_datetime(),
        "latitude": subpoint.latitude.degrees,
        "longitude": subpoint.longitude.degrees,
        "altitude": subpoint.elevation.km
    })

# Convert future positions to a DataFrame
df = pd.DataFrame(future_positions)

# Plot on a 2D map
fig = px.scatter_geo(df, lat="latitude", lon="longitude", hover_name="time",
                     title="Satellite Orbit on Map")
fig.update_layout(showlegend=False)
fig.show()

# Create a 3D scatter plot
fig = go.Figure(data=[go.Scatter3d(
    x=df["longitude"],
    y=df["latitude"],
    z=df["altitude"],
    mode='lines',
    line=dict(width=2, color='blue')
)])

# Update layout
fig.update_layout(
    scene=dict(
        xaxis_title="Longitude",
        yaxis_title="Latitude",
        zaxis_title="Altitude (km)"
    ),
    title="Satellite Orbit in 3D"
)

fig.show()