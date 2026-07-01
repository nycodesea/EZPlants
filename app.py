from dash import Dash, html, dcc, dash_table, Input, Output, State
import pandas as pd
import plantsdb
from graph import create_temp_range, create_gantt_chart, create_watering_graph
from plantsdb import DB
from flask import request
from plantsdb import add_watering_log

TABLE = "plants_data"
FAVTABLE = "plants_fav_data"
# for input
FIELDS = [
    ("name", "Plant name(required)", "text"),
    ("scientific_name", "Scientific name", "text"),
    ("temp_max", "Maximum temperature", "number"),
    ("temp_min", "Minimum temperature", "number"),
    ("grow_pattern", "Grow cycle", "text"),
    ("water_amount", "Water requirements", "text"),
    ("fertilizer", "Fertilizer", "text"),
    ("sow_start", "Sowing start month", "number"),
    ("sow_end", "Sowing end month", "number"),
    ("harvest_start", "Harvest start month", "number"),
    ("harvest_end", "Harvest end month", "number"),
]

plantsdb.init_db()
plantsdb.init_fav_db()

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("EZPlants"),
        html.H2("Add plant(using the same name updates the existing plant)"),
        html.Div(
            [
                html.Div(
                    dcc.Input(
                        id=f"{field}-input",
                        placeholder=placeholder,
                        type=input_type,
                    ),
                    style={"margin": "5px"},
                )
                for field, placeholder, input_type in FIELDS
            ],
        ),
        html.Div(
            html.Button(
                "Save",
                id="save-button",
            ),
            style={
                "display": "flex",
                "justifyContent": "center",
            },
        ),
        html.Div(id="save-message"),
        html.Br(),
        html.Br(),
        html.Div(
            [
                dash_table.DataTable(
                    id="plants-table",
                    page_size=20,
                    row_selectable="single",
                ),
            ],
            style={
                "overflowX": "auto",
                "maxWidth": "100%",
            },
        ),
        html.Div(
            html.Button(
                "Delete",
                id="delete-button",
            ),
            style={
                "display": "flex",
                "justifyContent": "center",
            },
        ),
        html.Div(id="delete-message"),
        html.Br(),
        html.Br(),
        dcc.Input(
            id="search-box",
            placeholder="Enter plant name",
            value="",
        ),
        dcc.Graph(id="temp-graph"),
        dcc.Graph(id="gantt-graph"),
        html.Div(
            [html.H2("Watering Count"), dcc.Graph(figure=create_watering_graph())]
        ),
    ],
    style={
        "backgroundColor": "#FDF3DDFF",
        "minHeight": "100vh",
        "padding": "20px",
    },
)


# get table data
@app.callback(
    [Output(f"{field}-input", "value") for field, _, _ in FIELDS],
    Input("plants-table", "selected_rows"),
    State("plants-table", "data"),
    prevent_initial_call=True,
)
def load_plant(selected_rows, data):

    if not selected_rows:
        return [None] * len(FIELDS)

    row = data[selected_rows[0]]

    return [row.get(field) for field, _, _ in FIELDS]


# delete data
@app.callback(
    Output("delete-message", "children"),
    Input("delete-button", "n_clicks"),
    State("plants-table", "selected_rows"),
    State("plants-table", "data"),
    prevent_initial_call=True,
)
def delete_plant(n_clicks, selected_rows, data):

    if not selected_rows:
        return "Please select a row"

    row = data[selected_rows[0]]
    name = row["name"]

    plantsdb.delete_data(name)

    return f"Deleted {name}"


# Input data
@app.callback(
    Output("save-message", "children"),
    Input("save-button", "n_clicks"),
    *[State(f"{field}-input", "value") for field, _, _ in FIELDS],
    prevent_initial_call=True,
)
def save_plant_callback(n_clicks, *values):

    plants_dict = {field: value for (field, _, _), value in zip(FIELDS, values)}
    plants_dict = {k: (None if v == "" else v) for k, v in plants_dict.items()}
    # Input check
    if not plants_dict["name"]:
        return "Plants name is required."
    if plants_dict["temp_min"] and plants_dict["temp_max"]:
        if plants_dict["temp_min"] > plants_dict["temp_max"]:
            return "Max temperature must be greater than minimum temperature."

    month_fields = [
        "sow_start",
        "sow_end",
        "harvest_start",
        "harvest_end",
    ]

    for field in month_fields:
        value = plants_dict[field]
        if value is not None and not (1 <= value <= 12):
            return f"{month_names[field]} must be between 1 and 12."

    plantsdb.save_plants(plants_dict)

    return f'{plants_dict["name"]} has been saved'


# temp-graph
@app.callback(
    Output("temp-graph", "figure"),
    Input("search-box", "value"),
)
def update_temp_graph(keyword):

    rows = plantsdb.get_temp_rows(keyword)

    return create_temp_range(rows)


# gantt-graph
@app.callback(
    Output("gantt-graph", "figure"),
    Input("search-box", "value"),
)
def update_gantt(keyword):

    if not keyword:
        return {}

    rows = plantsdb.get_gantt_data(keyword)
    return create_gantt_chart(rows)


# table update
@app.callback(
    Output("plants-table", "data"),
    Output("plants-table", "columns"),
    Input("search-box", "value"),
    Input("save-message", "children"),
    Input("delete-message", "children"),
)
def update_table(keyword, save_message, delete_message):
    if keyword:
        rows, columns = plantsdb.get_data(keyword)
    else:
        rows, columns = plantsdb.get_data()
    # if not rows:
    #    return [],[]
    df = pd.DataFrame(rows, columns=columns)

    if "id" in df.columns:
        df = df.drop(columns=["id"])

    return (
        df.to_dict("records"),
        [{"name": c, "id": c} for c in df.columns],
    )


server = app.server


# watering api
@server.route("/api/watering", methods=["POST"])
def api_watering():
    data = request.get_json()

    if not data:
        return {"error": "no json"}, 400

    try:
        add_watering_log(
            data["plant_id"],
            data["watering_time"],
            data["watering_duration"],
            data["moisture_before"],
            data["moisture_after"],
        )
    except Exception as e:
        print("ERROR:", e)
        return {"status": "error", "msg": str(e)}, 500

    return {"status": "ok"}


if __name__ == "__main__":
    # app.run(host="0.0.0.0", debug=True, port=8049)
    app.run(debug=True, port=8049)
