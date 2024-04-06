import dash
from dash import dcc, html, Input, Output
import plotly.express as px
import pandas as pd

import plotly.io as pio

pio.templates.default = "plotly_dark"


airports_df = pd.read_csv("airports_df.csv")
columns_to_group_by = [
    "Airport.Code",
    "Airport.Name",
    "Time.Label",
    "Time.Month",
    "Time.Month Name",
    "Time.Year",
    "Statistics.# of Delays.Carrier",
    "Statistics.# of Delays.Late Aircraft",
    "Statistics.# of Delays.National Aviation System",
    "Statistics.# of Delays.Security",
    "Statistics.# of Delays.Weather",
    "Statistics.Carriers.Names",
    "Statistics.Carriers.Total",
    "Statistics.Flights.Cancelled",
    "Statistics.Flights.Delayed",
    "Statistics.Flights.Diverted",
    "Statistics.Flights.On Time",
    "Statistics.Flights.Total",
    "Statistics.Minutes Delayed.Carrier",
    "Statistics.Minutes Delayed.Late Aircraft",
    "Statistics.Minutes Delayed.National Aviation System",
    "Statistics.Minutes Delayed.Security",
    "Statistics.Minutes Delayed.Total",
    "Statistics.Minutes Delayed.Weather",
    "Time.Datetime",
    "Proportions.Flights.On Time",
    "Proportions.Flights.Cancelled or Diverted",
    "Proportions.Flights.Security Delays",
    "Statistics.# of Delays.Total",
    "Season",
]

x_axis_options = [
    "Airport.Code",
    "Airport.Name",
    "Time.Datetime",
    "Time.Month",
    "Time.Season",
    "Time.Year",
]

y_axis_options = columns_to_group_by = [
    "Statistics.# of Delays.Carrier",
    "Statistics.# of Delays.Late Aircraft",
    "Statistics.# of Delays.National Aviation System",
    "Statistics.# of Delays.Security",
    "Statistics.# of Delays.Weather",
    "Statistics.# of Delays.Total",
    "Statistics.Carriers.Total",
    "Statistics.Flights.Cancelled",
    "Statistics.Flights.Delayed",
    "Statistics.Flights.Diverted",
    "Statistics.Flights.On Time",
    "Statistics.Flights.Total",
    "Statistics.Minutes Delayed.Carrier",
    "Statistics.Minutes Delayed.Late Aircraft",
    "Statistics.Minutes Delayed.National Aviation System",
    "Statistics.Minutes Delayed.Security",
    "Statistics.Minutes Delayed.Total",
    "Statistics.Minutes Delayed.Weather",
    "Proportions.Flights.On Time",
    "Proportions.Flights.Cancelled or Diverted",
    "Proportions.Flights.Security Delays",
]

airports_list = airports_df["Airport.Code"].unique()
# months_list = airports_df["Time.Month"].unique().sort()
months_list = [i for i in range(1, 13)]
years_list = airports_df["Time.Year"].unique()

app = dash.Dash(__name__)


app.layout = html.Div(
    [
        html.Div(
            [
                html.H1("Airport Data Dashboard", style={"textAlign": "center"}),
                html.P(
                    "Here is a dashboard for investigating your dataset about airports. You can investigate certain features over time as well as the proportions of types of flights, delays, and minutes delayed.",
                    style={"textAlign": "center"},
                ),
            ],
            className="section",
        ),
        html.Div(  # Wrapper for both halves to ensure they have the same height
            [
                html.Div(  # Left half
                    [
                        dcc.Graph(id="xy-plot"),
                        html.Div(  # Wrapper for controls with className="section"
                            [
                                html.Label("X-axis:"),
                                dcc.Dropdown(
                                    id="x-axis-dropdown",
                                    options=[
                                        {"label": "Time", "value": "Time.Datetime"},
                                        {"label": "Month", "value": "Time.Month"},
                                        {"label": "Season", "value": "Time.Season"},
                                        {"label": "Year", "value": "Time.Year"},
                                        {
                                            "label": "Airports (code)",
                                            "value": "Airport.Code",
                                        },
                                        {
                                            "label": "Airports (name)",
                                            "value": "Airport.Name",
                                        },
                                    ],
                                    value="Time.Datetime",
                                ),
                                html.Label("Y-axis:"),
                                dcc.Dropdown(
                                    id="y-axis-dropdown",
                                    options=[
                                        {"label": option, "value": option}
                                        for option in y_axis_options
                                    ],
                                    value=y_axis_options[0],
                                ),
                                html.Label("Aggregator:"),
                                dcc.Dropdown(
                                    id="aggregator-dropdown",
                                    options=[
                                        {"label": "Mean", "value": "mean"},
                                        {"label": "Sum", "value": "sum"},
                                        {"label": "Median", "value": "median"},
                                        {"label": "Min", "value": "min"},
                                        {"label": "Max", "value": "max"},
                                    ],
                                    value="mean",
                                ),
                            ],
                            className="section",
                        ),
                    ],
                    style={
                        "width": "35%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                    className="section",
                ),
                html.Div(  # Right half
                    [
                        html.Div(  # Top row
                            [
                                html.Div(  # Top left quadrant (Graph 1)
                                    [dcc.Graph(id="delays-by-type-pie")],
                                    style={"width": "40%", "display": "inline-block"},
                                    className="section",
                                ),
                                html.Div(  # Top right quadrant (Graph 2)
                                    [dcc.Graph(id="flights-by-type-pie")],
                                    style={"width": "40%", "display": "inline-block"},
                                    className="section",
                                ),
                            ],
                            style={"width": "100%"},
                        ),
                        html.Div(  # Bottom row
                            [
                                html.Div(  # Bottom left quadrant (Graph 3)
                                    [dcc.Graph(id="minutes-delayed-by-type-pie")],
                                    style={"width": "40%", "display": "inline-block"},
                                    className="section",
                                ),
                                html.Div(  # Bottom right quadrant (Filters)
                                    [
                                        html.P(
                                            "Select items to exclude from the analysis:"
                                        ),
                                        dcc.Dropdown(
                                            id="month-dropdown",
                                            options=months_list,
                                            multi=True,
                                            placeholder="Exclude Months...",
                                        ),
                                        dcc.Dropdown(
                                            id="year-dropdown",
                                            options=years_list,
                                            multi=True,
                                            placeholder="Exclude Years...",
                                        ),
                                        dcc.Dropdown(
                                            id="airport-dropdown",
                                            options=airports_list,
                                            multi=True,
                                            placeholder="Exclude Airports...",
                                        ),
                                    ],
                                    style={"width": "40%", "display": "inline-block"},
                                    className="section",
                                ),
                            ],
                            style={"display": "flex", "width": "100%"},
                        ),
                    ],
                    style={
                        "width": "65%",
                        "display": "inline-block",
                        "verticalAlign": "top",
                    },
                    # className="section",
                ),
            ],
            style={
                "display": "flex",
                "justifyContent": "space-between",
                "width": "100%",
            },  # Ensures equal height and spacing
        ),
    ],
    className="app-container",  # Ensures app-wide styling,
    style={"height": "100vh"},
)


def aggregate_data(df, x_axis, y_axis, aggregator):
    # Group by the x_axis and then aggregate the y_axis with the selected aggregator
    if aggregator == "mean":
        aggregated = df.groupby(x_axis)[y_axis].mean().reset_index()
    elif aggregator == "sum":
        aggregated = df.groupby(x_axis)[y_axis].sum().reset_index()
    elif aggregator == "median":
        aggregated = df.groupby(x_axis)[y_axis].median().reset_index()
    elif aggregator == "min":
        aggregated = df.groupby(x_axis)[y_axis].min().reset_index()
    elif aggregator == "max":
        aggregated = df.groupby(x_axis)[y_axis].max().reset_index()
    else:
        # Default to mean if aggregator is not recognized
        aggregated = df.groupby(x_axis)[y_axis].mean().reset_index()
    return aggregated


@app.callback(
    Output("xy-plot", "figure"),
    [
        Input("x-axis-dropdown", "value"),
        Input("y-axis-dropdown", "value"),
        Input("aggregator-dropdown", "value"),
    ],
)
def update_xy_plot(x_axis, y_axis, aggregator):
    # Aggregate data
    aggregated_df = aggregate_data(airports_df, x_axis, y_axis, aggregator)

    # Determine plot type based on x_axis value
    if x_axis in ["Airport.Code", "Airport.Name"]:
        # Categorical data might be better represented with a bar chart
        fig = px.bar(aggregated_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")
    else:
        # Assuming continuous or ordinal data
        fig = px.line(aggregated_df, x=x_axis, y=y_axis, title=f"{y_axis} by {x_axis}")

    return fig


def filter_dataset(months, years, airports):
    months = [] if months is None else months
    years = [] if years is None else years
    airports = [] if airports is None else airports

    # Filter the DataFrame based on the selected filter options

    filtered_df = airports_df.copy()

    filtered_df = filtered_df[~filtered_df["Time.Month"].isin(months)]

    filtered_df = filtered_df[~airports_df["Time.Year"].isin(years)]

    filtered_df = filtered_df[~airports_df["Airport.Code"].isin(airports)]

    return filtered_df


@app.callback(
    Output("delays-by-type-pie", "figure"),
    [
        Input("month-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("airport-dropdown", "value"),
    ],
)
def update_delays_by_type_pie(months, years, airports):

    filtered_df = filter_dataset(months, years, airports)

    # Assuming delays are categorized into columns like 'Statistics.# of Delays.Weather'
    # Sum up each delay type to get total counts
    delay_types = [
        "Weather",
        "Late Aircraft",
        "Security",
        "National Aviation System",
        "Carrier",
    ]
    delay_counts = [
        filtered_df[f"Statistics.# of Delays.{type}"].sum() for type in delay_types
    ]

    # Create the pie chart
    fig = px.pie(
        names=delay_types, values=delay_counts, title="Number of Delays by Type"
    )
    return fig


@app.callback(
    Output("flights-by-type-pie", "figure"),
    [
        Input("month-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("airport-dropdown", "value"),
    ],
)
def update_flights_by_type_pie(months, years, airports):

    filtered_df = filter_dataset(months, years, airports)

    # Assuming delays are categorized into columns like 'Statistics.# of Delays.Weather'
    # Sum up each delay type to get total counts

    flight_types = ["Cancelled", "Delayed", "Diverted", "On Time"]

    delay_counts = [
        filtered_df[f"Statistics.Flights.{type}"].sum() for type in flight_types
    ]

    # Create the pie chart
    fig = px.pie(
        names=flight_types, values=delay_counts, title="Number of Flights by Type"
    )
    return fig


@app.callback(
    Output("minutes-delayed-by-type-pie", "figure"),
    [
        Input("month-dropdown", "value"),
        Input("year-dropdown", "value"),
        Input("airport-dropdown", "value"),
    ],
)
def update_delays_by_type_pie(months, years, airports):

    filtered_df = filter_dataset(months, years, airports)

    # Assuming delays are categorized into columns like 'Statistics.# of Delays.Weather'
    # Sum up each delay type to get total counts
    delay_types = [
        "Weather",
        "Late Aircraft",
        "Security",
        "National Aviation System",
        "Carrier",
    ]

    minutes_delayed_counts = [
        filtered_df[f"Statistics.Minutes Delayed.{type}"].sum() for type in delay_types
    ]

    # Create the pie chart
    fig = px.pie(
        names=delay_types,
        values=minutes_delayed_counts,
        title="Number of Minutes Delayed by Type",
    )
    return fig


if __name__ == "__main__":
    app.run_server(debug=True)
