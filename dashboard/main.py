from dash.dependencies import Input, Output, State
from dash import dcc, html
import dash
import dash_bootstrap_components as dbc
import pandas as pd
import pathlib
import logging
import requests

import config
import preprocess
from dashboard import Dashboard


# Whether if we should preprocess the data after a hot reload
REALTIME = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Check if the data are already preprocessed.
if REALTIME or not (
    pathlib.Path(config.PREPROCESSED_DATASET_FILE).exists()
    and pathlib.Path(config.PREPROCESSED_GEO_DATASET_FILE).exists()
):
    logger.info("Preprocessing of the dataset...")
    dataframe = preprocess.preprocess(
        config.RAW_DATASET_FILE,
        config.PREPROCESSED_DATASET_FILE,
        config.RAW_GEO_DATASET_FILE,
        config.PREPROCESSED_GEO_DATASET_FILE,
    )
else:
    logger.info("Loading of the dataset...")
    dataframe = pd.read_excel(config.PREPROCESSED_DATASET_FILE)
    logger.info("Dataset loaded!")


# Initialize the dashboard
dashboard = Dashboard(dataframe)

# Initialize Dash app
app = dash.Dash(
    __name__,
    suppress_callback_exceptions=True,
    external_stylesheets=[dbc.themes.BOOTSTRAP, dbc.icons.BOOTSTRAP],
)

# Useful when deploying with gunicorn
server = app.server

# Sidebar
offcanvas = html.Div(
    [
        dbc.Offcanvas(
            html.Div(
                [
                    html.H2("📊 Available Dashboards", className="fs-4 mb-3"),
                    html.Hr(),
                    html.P(
                        "Navigate between the following dashboards to explore insights.",
                        className="lead mb-4",
                    ),
                    dbc.Nav(
                        [
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-map me-2"),
                                    "Blood Donor Distribution by Arrondissement",
                                ],
                                href="/donor-distribution",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-heart-pulse me-2"),
                                    "Blood Donation Eligibility Analysis",
                                ],
                                href="/donor-elligibility",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-person-badge me-2"),
                                    "Profiling Ideal Donors",
                                ],
                                href="/donor-profiling",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-bar-chart-line me-2"),
                                    "Campaign Effectiveness Analysis",
                                ],
                                href="/campaign-effectiveness",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-arrow-repeat me-2"),
                                    "Donor Retention Analysis",
                                ],
                                href="/donor-retention",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-search-heart me-2"),
                                    "Survey/Feedback Sentiment Analysis",
                                ],
                                href="/feedback",
                                active="exact",
                                className="mb-2",
                            ),
                            dbc.NavLink(
                                [
                                    html.I(className="bi bi-robot me-2"),
                                    "Eligibility Prediction AI Model",
                                ],
                                href="/eligibility-prediction",
                                active="exact",
                                className="mb-2",
                            ),
                        ],
                        vertical=True,
                        pills=True,
                        className="nav-pills-custom",  # Custom class for additional styling
                    ),
                ],
                className="mb-3",
            ),
            id="offcanvas",
            title=[
                html.I(className="bi bi-droplet me-2"),
                "Blood Donation Dashboard",
            ],
            is_open=False,
            placement="start",  # Offcanvas opens from the left
            style={"width": "300px"},  # Adjust width for better readability
            backdrop=True,  # Enable backdrop to darken the rest of the page
            scrollable=True,  # Make the offcanvas scrollable if content overflows
        ),
    ]
)

# Navbar
navbar = dbc.Navbar(
    dbc.Container(
        [
            # Offcanvas Toggle Button
            dbc.Button(
                html.I(className="bi bi-list"),  # Menu icon
                id="open-offcanvas",
                color="primary",
                className="me-2",
            ),
            # Navbar Brand (Title)
            dbc.NavbarBrand("Blood Donation Dashboard", className="ms-2"),
            # Navbar Links (Right-aligned)
            dbc.Nav(
                [
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-book me-1"),
                            "User Manual",
                        ],
                        href="/",
                        active="exact",
                        className="ms-auto",
                    ),
                    dbc.NavLink(
                        [
                            html.I(className="bi bi-github me-1"),
                            "GitHub",
                        ],
                        href="https://github.com/pythonbrad/indabax_hack_2025",
                        active="exact",
                        className="ms-auto",
                    ),
                ],
                navbar=True,
                className="ms-auto",
            ),
        ],
        fluid=True,
    ),
    color="dark",
    dark=True,
)

# Body
content = dbc.Container(
    [
        dbc.Spinner(
            [
                html.Div(id="page-content"),
            ],
            delay_show=1000,
            spinner_style={"width": "10rem", "height": "10rem"},
            type="grow",
            color="primary",
            fullscreen=True,
        )
    ],
    class_name="my-5",
)


app.layout = html.Div([dcc.Location(id="url"), offcanvas, navbar, content])


@app.callback(
    Output("offcanvas", "is_open"),
    Input("open-offcanvas", "n_clicks"),
    [State("offcanvas", "is_open")],
)
def toggle_offcanvas(n1, is_open):
    if n1:
        return not is_open
    return is_open


@app.callback(Output("page-content", "children"), [Input("url", "pathname")])
def render_page_content(pathname):
    if pathname == "/":
        with open("USER-MANUAL.md") as f:
            return dcc.Markdown(f.read())
    elif pathname == "/donor-distribution":
        return html.Div(
            [
                html.H1(
                    "Blood Donor Distribution by Arrondissement",
                    style={"textAlign": "center"},
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="donor-map", figure=dashboard.map_donor_distribution()
                        ),
                    ],
                ),
                html.Div(
                    [
                        dcc.Graph(
                            id="donor-map-2",
                            figure=dashboard.map_donor_distribution(map_view=False),
                        ),
                    ],
                ),
            ]
        )
    elif pathname == "/donor-elligibility":
        return html.Div(
            [
                html.H1(
                    "Blood Donation Eligibility Analysis",
                    style={"textAlign": "center"},
                ),
                # Pie Chart - Overall Eligibility
                dcc.Graph(
                    id="eligibility-pie",
                    figure=dashboard.health_conditions_and_eligibility(),
                ),
                # Select for selecting health condition
                dbc.Select(
                    id="eligibility-condition-select",
                    options=[
                        {"label": cond, "value": cond}
                        for cond in dashboard.health_conditions
                    ],
                    value=dashboard.health_conditions[0],  # Default selection
                ),
                # Bar Chart - Health Condition Impact
                dcc.Graph(id="eligibility-condition-bar"),
                # Bar Chart - Overall Health Condition Impact
                dcc.Graph(
                    id="eligibility-condition-2-bar",
                    figure=dashboard.health_conditions_and_eligibility("all"),
                ),
            ]
        )
    elif pathname == "/donor-profiling":
        religion_figure, religion_insights = dashboard.profiling_ideal_donors(
            paired_with="Religion"
        )
        profession_figure, profession_insights = dashboard.profiling_ideal_donors(
            paired_with="Profession"
        )

        return html.Div(
            [
                html.H1(
                    "Blood Donor Profiling Using Clustering",
                    style={"textAlign": "center"},
                ),
                html.Div(
                    [
                        html.H3(
                            "Gender - Religion",
                            style={"textAlign": "center"},
                        ),
                        # Scatter Plot - PCA Visualization of Clusters
                        dcc.Graph(
                            id="profiling-cluster-scatter",
                            figure=religion_figure,
                        ),
                        # Display Ideal Donor Insights
                        html.H4("Ideal Donor Insights:"),
                        html.Ul(
                            [
                                html.Li(f"Average Age: {religion_insights[0]}"),
                                html.Li(f"Most Common Gender: {religion_insights[1]}"),
                                html.Li(
                                    f"Most Common Religion: {religion_insights[2]}"
                                ),
                            ]
                        ),
                    ]
                ),
                html.Div(
                    [
                        html.H3(
                            "Gender - Profession",
                            style={"textAlign": "center"},
                        ),
                        # Scatter Plot - PCA Visualization of Clusters
                        dcc.Graph(
                            id="profiling-cluster-scatter-2",
                            figure=profession_figure,
                        ),
                        # Display Ideal Donor Insights
                        html.H4("Ideal Donor Insights:"),
                        html.Ul(
                            [
                                html.Li(f"Average Age: {profession_insights[0]}"),
                                html.Li(
                                    f"Most Common Gender: {profession_insights[1]}"
                                ),
                                html.Li(
                                    f"Most Common Profession: {profession_insights[2]}"
                                ),
                            ]
                        ),
                    ]
                ),
            ],
        )
    elif pathname == "/campaign-effectiveness":
        return html.Div(
            [
                html.H1(
                    "Campaign Effectiveness Analysis", style={"textAlign": "center"}
                ),
                # Select to select year
                dbc.Select(
                    id="campaign-year-select",
                    options=[
                        {"label": str(year), "value": year} for year in dashboard.years
                    ],
                    value=max(dashboard.years),  # Default to most recent year
                ),
                # Line Chart - Donations Over Time
                dcc.Graph(id="campaign-donation-trend"),
                # Bar Chart - Donations by Gender
                dcc.Graph(id="campaign-donation-gender"),
                # Bar Chart - Donations by Education Level
                dcc.Graph(id="campaign-donation-education"),
                # Bar Chart - Donations by Profession
                dcc.Graph(id="campaign-donation-profession"),
            ]
        )
    elif pathname == "/donor-retention":
        return html.Div(
            [
                html.H1("Donor Retention Analysis", style={"textAlign": "center"}),
                # Select to select year
                dbc.Select(
                    id="retention-year-select",
                    options=[
                        {"label": str(year), "value": year} for year in dashboard.years
                    ],
                    value=max(dashboard.years),  # Default to most recent year
                ),
                # Pie Chart - Repeat Donation Frequency
                dcc.Graph(id="retention-donation"),
                # Bar Chart - Retention by Age Group
                dcc.Graph(id="retention-age"),
                # Bar Chart - Retention by Genre Group
                dcc.Graph(id="retention-genre"),
                # Bar Chart - Retention by Profession
                dcc.Graph(id="retention-profession"),
                # Bar Chart - Retention by Region
                dcc.Graph(id="retention-region"),
            ]
        )
    elif pathname == "/feedback":
        groups = ["Age", "Genre", "Profession"]

        return html.Div(
            [
                html.H1(
                    "Survey/Feedback Sentiment Analysis", style={"textAlign": "center"}
                ),
                # Select to select year
                dbc.Select(
                    id="feedback-year-select",
                    options=[
                        {"label": year, "value": year} for year in dashboard.years
                    ],
                    value=max(dashboard.years),  # Default to last
                ),
                # Select to select group
                dbc.Select(
                    id="feedback-group-select",
                    options=[{"label": group, "value": group} for group in groups],
                    value=groups[0],  # Default to first
                ),
                # Pie Chart - Overall feedback analysis
                dcc.Graph(id="feedback-donation"),
                # Bar Chart - Feedback analysis per group
                dcc.Graph(id="feedback-group"),
            ]
        )
    elif pathname == "/eligibility-prediction":
        try:
            if not config.ELIGIBILITY_PREDICTION_API:
                raise Exception("Eligibility prediction API not set!")

            data = requests.get(config.ELIGIBILITY_PREDICTION_API + "/entries").json()
        except Exception as err:
            logging.error(f"API error: {err}")

            return dbc.Alert(
                "Error: Unable to contact the Elibility Prediction AI model API",
                color="danger",
            )

        return html.Div(
            [
                html.H1(
                    "Eligibility Predicton AI Model", style={"textAlign": "center"}
                ),
                dbc.Alert(
                    "The AI model assumpt that the patient is eligible at first before any prediction. "
                    "The result of this prediction is not accurate and can change based on the provided information.",
                    color="warning",
                ),
                # Input to enter the age
                html.Label("Type the age (optional)"),
                dbc.Input(
                    id="eligibility-predict-age-input",
                    type="number",
                    min=0,
                    max=100,
                    step=1,
                ),
                # Select to select the genre
                html.Label("Select the gender (optional)"),
                dbc.Select(
                    id="eligibility-predict-genre-select",
                    options=[
                        {"label": genre, "value": genre}
                        for genre in [None] + sorted(data["genres"])
                    ],
                    value=None,  # Default
                ),
                # Select to select the profession
                html.Label("Select the profession (optional)"),
                dbc.Select(
                    id="eligibility-predict-profession-select",
                    options=[
                        {"label": profession, "value": profession}
                        for profession in [None] + sorted(data["professions"])
                    ],
                    value=None,  # Default
                ),
                # Select to select the health condition
                html.Label("Select the health condition (optional)"),
                dbc.Select(
                    id="eligibility-predict-health-condition-select",
                    options=[
                        {"label": cond, "value": cond}
                        for cond in [None] + sorted(data["health_conditions"])
                    ],
                    value=None,  # Default
                ),
                html.Br(),
                # Result
                html.H3("Result", style={"textAlign": "center"}),
                dbc.Progress(id="eligibility-predict-output"),
            ]
        )

    # If the user tries to reach a different page, return a 404 message
    return html.Div(
        [
            html.H1("404: Not found", className="text-danger"),
            html.Hr(),
            html.P(f"The pathname {pathname} was not recognised..."),
        ],
        className="p-3 bg-light rounded-3",
    )


@app.callback(
    Output("eligibility-condition-bar", "figure"),
    Input("eligibility-condition-select", "value"),
)
def update_eligibiliy_chart(condition: str):
    return dashboard.health_conditions_and_eligibility(condition)


@app.callback(
    [
        Output("campaign-donation-trend", "figure"),
        Output("campaign-donation-gender", "figure"),
        Output("campaign-donation-education", "figure"),
        Output("campaign-donation-profession", "figure"),
    ],
    [Input("campaign-year-select", "value")],
)
def update_campaign_charts(selected_year: str):
    return dashboard.campaign_effectiveness(int(selected_year))


@app.callback(
    [
        Output("retention-donation", "figure"),
        Output("retention-age", "figure"),
        Output("retention-genre", "figure"),
        Output("retention-profession", "figure"),
        Output("retention-region", "figure"),
    ],
    [Input("retention-year-select", "value")],
)
def update_retention_charts(selected_year: str):
    return dashboard.donor_retention(int(selected_year))


@app.callback(
    [
        Output("feedback-donation", "figure"),
        Output("feedback-group", "figure"),
    ],
    [
        Input("feedback-year-select", "value"),
        Input("feedback-group-select", "value"),
    ],
)
def update_feedback_charts(year: str, group: str):
    return dashboard.feedback_analysis(int(year), group)


@app.callback(
    [
        Output("eligibility-predict-output", "label"),
        Output("eligibility-predict-output", "color"),
        Output("eligibility-predict-output", "value"),
    ],
    [
        Input("eligibility-predict-age-input", "value"),
        Input("eligibility-predict-genre-select", "value"),
        Input("eligibility-predict-profession-select", "value"),
        Input("eligibility-predict-health-condition-select", "value"),
    ],
)
def update_eligibility_predict_result(
    age: str, genre: str, profession: str, health_condition: str
):
    data = requests.post(
        config.ELIGIBILITY_PREDICTION_API + "/input",
        json={
            "age": age,
            "genre": genre,
            "professions": [profession] if profession else [],
            "health_conditions": [health_condition] if health_condition else [],
        },
    ).json()
    score = int(data["score"] * 100)
    color = ["danger", "warning", "info", "primary", "success"][score // 25]

    return f"{score}%", color, score


# Run server
if __name__ == "__main__":
    app.run(debug=True)
