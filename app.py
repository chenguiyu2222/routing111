import time
import importlib

import dash
import dash_core_components as dcc
import dash_html_components as html
import numpy as np
from dash.dependencies import Input, Output, State
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC

import utils.dash_reusable_components as drc
import utils.map as map

app = dash.Dash(
    __name__,
    meta_tags=[
        {"name": "viewport", "content": "width=device-width, initial-scale=1.0"}
    ],
)
app.title = "Safe Routing"
server = app.server


app.layout = html.Div(
    children=[
        # .container class is fixed, .container.scalable is scalable
        html.Div(
            className="banner",
            children=[
                # Change App Name here
                html.Div(
                    className="container scalable",
                    children=[
                        # Change App Name here
                        html.H2(
                            id="banner-title",
                            children=[
                                html.A(
                                    "Safe Routing in L.A.",
                                    href="https://github.com/plotly/dash-svm",  # TO be changed
                                    style={
                                        "text-decoration": "none",
                                        "color": "inherit",
                                    },
                                )
                            ],
                        ),
                        html.A(
                            id="banner-logo",
                            children=[
                                html.Img(src=app.get_asset_url("dash-logo-new.png"))
                            ],
                            href="https://plot.ly/products/dash/",
                        ),
                    ],
                )
            ],
        ),
        html.Div(
            id="body",
            className="container scalable",
            children=[
                html.Div(
                    id="app-container",
                    # className="row",
                    children=[
                        html.Div(
                            # className="three columns",
                            id="left-column",
                            children=[
                                drc.Card(
                                    id="secoond-card",
                                    children=[html.Div('Please type your origin and destination'),
                                              'Origin:  ',html.Br(),
                                              dcc.Input(
                                                  id="origin",
                                                  value="Ace Hotel Downtown Los Angeles",
                                                  type="text",
                                                  style={
                                                 "color": "inherit",
                                                  }
                                              ),html.Br(),html.Br(),
                                              'Destination:',html.Br(),
                                              dcc.Input(
                                                  id="destination",
                                                  value="Los Angeles Trade Technical College",
                                                  type="text",
                                                  style={
                                                      "color": "inherit",
                                                  }
                                              ),html.Br(),html.Br(),
                                                'Examples:  ',html.Br(),
                                              "Ace Hotel Downtown Los Angeles",html.Br(),
                                              "Walt Disney Concert Hall",html.Br(),
                                              "Freehand Los Angeles",html.Br(),
                                              "Millennium Biltmore Hotel Los Angeles",html.Br(),
                                              "Los Angeles Trade Technical College",html.Br(),
                                              ],
                                ),
                                drc.Card(
                                    id="first-card",
                                    children=[
                                        drc.NamedSlider(
                                            name="Distance Weight",
                                            id="Distance Weight",
                                            min=0,
                                            max=1,
                                            marks={
                                                str(i/10): str(i/10)
                                                for i in range(0, 10, 1)
                                            },
                                            value=1,
                                        ),
                                        drc.NamedSlider(
                                            name="Crime Risk Weight",
                                            id="Crime Risk Weight",
                                            min=0,
                                            max=1,
                                            marks={
                                                i / 10: str(i / 10)
                                                for i in range(0, 10, 1)
                                            },
                                            step=0.1,
                                            value=0.2,
                                        ),
                                        drc.NamedSlider(
                                            name="Perception of safety weight",
                                            id="Perception of safety weight",
                                            min=0,
                                            max=1,
                                            marks={
                                                i / 10: str(i / 10)
                                                for i in range(0, 10, 1)
                                            },
                                            step=0.1,
                                            value=0.2,
                                        ),
                                    ],
                                ),
                            ],
                        ),
                        html.Div(
                            id="div-graphs",
                            children=dcc.Graph(
                                id="graph-sklearn-svm",
                                figure=dict(
                                    layout=dict(
                                        plot_bgcolor="#282b38", paper_bgcolor="#282b38"
                                    )
                                ),
                            ),
                        ),
                    ],
                )
            ],
        ),
    ]
)




@app.callback(
    Output("div-graphs", "children"),
    [
        Input("origin", "value"),
        Input("destination", "value"),
        Input("Distance Weight", "value"),
        Input("Crime Risk Weight", "value"),
        Input("Perception of safety weight", "value"),
    ],
)
def update_svm_graph(
    origin,
    destination,
    Distance,
    CrimeRisk,
    Perception_safetye,
):
    t_start = time.time()
    h = 0.3  # step size in the mesh


    # Plot the decision boundary. For that, we will assign a color to each
    # point in the mesh [x_min, x_max]x[y_min, y_max].

    prediction_figure = map.drawmap(origin,destination,Distance,CrimeRisk,Perception_safetye)
    return [
        html.Div(
            id="svm-graph-container",
            children=dcc.Loading(
                className="graph-wrapper",
                children=dcc.Graph(id="graph-sklearn-svm", figure=prediction_figure),
                style={"display": "none"},
            ),
        ),
    ]


# Running the server
if __name__ == "__main__":
    app.run_server(debug=True)
