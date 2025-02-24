import pandas as pd
import plotly.express as px
import dash
from dash import dcc, html
from dash.dependencies import Input, Output

# Load the dataset
file_path = "Air_Quality_Cleaned.csv"  # Ensure the file is in the same directory
df_cleaned = pd.read_csv(file_path)

# Convert Start_Date to datetime format
df_cleaned["Start_Date"] = pd.to_datetime(df_cleaned["Start_Date"], errors="coerce")

# Extract useful time-based features
df_cleaned["Year"] = df_cleaned["Start_Date"].dt.year
df_cleaned["Month"] = df_cleaned["Start_Date"].dt.month
df_cleaned["Day_of_Week"] = df_cleaned["Start_Date"].dt.day_name()

# Extracting Season
df_cleaned["Season"] = df_cleaned["Start_Date"].dt.month.map({
    12: "Winter", 1: "Winter", 2: "Winter",
    3: "Spring", 4: "Spring", 5: "Spring",
    6: "Summer", 7: "Summer", 8: "Summer",
    9: "Fall", 10: "Fall", 11: "Fall"
})

# Get unique values for filters
available_years = sorted(df_cleaned["Year"].dropna().unique())
available_locations = sorted(df_cleaned["Geo Place Name"].dropna().unique())
available_seasons = ["Winter", "Spring", "Summer", "Fall"]

# Debugging Print: Available Years
print("Available years in dataset:", available_years)

# Initialize Dash app
app = dash.Dash(__name__)

# Layout of the dashboard with filters
app.layout = html.Div([
    html.H1("Air Quality Dashboard", style={'text-align': 'center'}),

    # Dropdown filters
    html.Div([
        html.Label("Select Year:"),
        dcc.Dropdown(
            id="year-filter",
            options=[{"label": str(year), "value": year} for year in available_years],
            value=available_years[0] if available_years else None,  # Default to first year
            clearable=False
        ),
    ], style={"width": "30%", "display": "inline-block"}),

    html.Div([
        html.Label("Select Location:"),
        dcc.Dropdown(
            id="location-filter",
            options=[{"label": loc, "value": loc} for loc in available_locations],
            value=available_locations[0] if available_locations else None,  # Default to first location
            clearable=False
        ),
    ], style={"width": "30%", "display": "inline-block"}),

    html.Div([
        html.Label("Select Season:"),
        dcc.Dropdown(
            id="season-filter",
            options=[{"label": season, "value": season} for season in available_seasons],
            value="Winter",  # Default value
            clearable=False
        ),
    ], style={"width": "30%", "display": "inline-block"}),

    # Graphs
    dcc.Graph(id="yearly-trend-graph"),
    dcc.Graph(id="top-locations-graph"),
    dcc.Graph(id="heatmap-graph"),
    dcc.Graph(id="day-of-week-graph"),
    dcc.Graph(id="season-graph")
])

# Define callback functions for dynamic updates
@app.callback(
    [Output("yearly-trend-graph", "figure"),
     Output("top-locations-graph", "figure"),
     Output("heatmap-graph", "figure"),
     Output("day-of-week-graph", "figure"),
     Output("season-graph", "figure")],
    [Input("year-filter", "value"),
     Input("location-filter", "value"),
     Input("season-filter", "value")]
)
def update_graphs(selected_year, selected_location, selected_season):
    # Filter data based on user selections
    filtered_df = df_cleaned[df_cleaned["Year"] == selected_year].copy()

    # Handle missing data for year selection
    if filtered_df.empty:
        latest_year = df_cleaned["Year"].max()  # Get latest available year
        filtered_df = df_cleaned[df_cleaned["Year"] == latest_year]
        title = f"No data for {selected_year}, showing {latest_year} instead"
    else:
        title = f"Air Quality Trends in {selected_year}"

    location_filtered_df = df_cleaned[df_cleaned["Geo Place Name"] == selected_location].copy()
    season_filtered_df = df_cleaned[df_cleaned["Season"] == selected_season].copy()

    # Debugging Prints
    print(f"Selected Year: {selected_year}, Available Data: {not filtered_df.empty}")
    print(f"Selected Location: {selected_location}, Data Points: {len(location_filtered_df)}")
    print(f"Selected Season: {selected_season}, Data Points: {len(season_filtered_df)}")

    # Air Quality Trends Over the Years
    yearly_avg = filtered_df.groupby("Year")["Data Value"].mean().reset_index()
    fig1 = px.line(yearly_avg, x="Year", y="Data Value", title=title) if not yearly_avg.empty else px.line(title="No data available")

    # Top 10 Most Polluted Locations
    top_locations = filtered_df.groupby("Geo Place Name")["Data Value"].mean().nlargest(10).reset_index()
    fig2 = px.bar(top_locations, x="Data Value", y="Geo Place Name",
                  title=f"Top 10 Most Polluted Locations in {selected_year}",
                  orientation='h', color="Data Value", color_continuous_scale="reds") if not top_locations.empty else px.bar(title="No data available")

    # Pollution Levels by Location and Year
    pollution_pivot = df_cleaned.pivot_table(index="Geo Place Name", columns="Year", values="Data Value", aggfunc="mean")
    fig3 = px.imshow(pollution_pivot, labels=dict(x="Year", y="Location", color="Pollution Level"),
                     title="Pollution Levels by Location and Year", color_continuous_scale="reds") if not pollution_pivot.empty else px.imshow(title="No data available")

    # Air Quality Variation by Day of the Week
    fig4 = px.box(location_filtered_df, x="Day_of_Week", y="Data Value",
                  title=f"Air Quality Variation in {selected_location}") if not location_filtered_df.empty else px.box(title="No data available")

    # Pollution Levels by Season
    fig5 = px.box(season_filtered_df, x="Season", y="Data Value",
                  title=f"Pollution Levels in {selected_season}") if not season_filtered_df.empty else px.box(title="No data available")

    return fig1, fig2, fig3, fig4, fig5

import webbrowser

if __name__ == '__main__':
    # Open the dashboard automatically in the default web browser
    webbrowser.open("http://127.0.0.1:8060/")
    app.run_server(debug=True, port=8060)


# Comment to run the Dashboard 
#http://127.0.0.1:8060