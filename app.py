from dash import Dash, html, dcc, dash_table, Input, Output, State
import pandas as pd
import plantsdb
from graph import create_temp_range, create_gantt_chart
from plantsdb import DB
import graph

TABLE = "plants_data"
FAVTABLE = "plants_fav_data"
# for input
FIELDS = [
    ("name", "植物名(※必須)", "text"),
    ("scientific_name", "学名", "text"),
    ("temp_max", "最高温度", "number"),
    ("temp_min", "最低温度", "number"),
    ("grow_pattern", "成長パターン", "text"),
    ("water_amount", "水やり量", "text"),
    ("fertilizer", "肥料", "text"),
    ("sow_start", "種まき開始月", "number"),
    ("sow_end", "種まき終了月", "number"),
    ("harvest_start", "収穫開始月", "number"),
    ("harvest_end", "収穫終了月", "number"),
]

plantsdb.init_db()
plantsdb.init_fav_db()

app = Dash(__name__)
app.layout = html.Div(
    [
        html.H1("EZPlants"),
        dcc.Input(
            id="search-box",
            placeholder="植物名を入力",
            value="",
        ),
        html.Br(),
        html.Br(),
        html.Div(
            [
                dash_table.DataTable(
                    id="plants-table",
                    hidden_columns=["id"],
                    page_size=20,
                    row_selectable="single",
                ),
            ],
            style={
                "overflowX": "auto",
                "maxWidth": "100%",
            },
        ),
        html.Button(
            "削除",
            id="delete-button",
        ),
        html.Div(id="delete-message"),
        dcc.Graph(id="temp-graph"),
        dcc.Graph(id="gantt-graph"),
        html.H2("植物追加"),
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
        html.Button(
            "保存",
            id="save-button",
        ),
        html.Div(id="save-message"),
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
        return "行を選択してください"

    row = data[selected_rows[0]]
    name = row["name"]

    plantsdb.delete_data(name)

    return f"{name} を削除しました"


# Input data
@app.callback(
    Output("save-message", "children"),
    Input("save-button", "n_clicks"),
    *[State(f"{field}-input", "value") for field, _, _ in FIELDS],
    prevent_initial_call=True,
)
def save_plant_callback(n_clicks, *values):

    plants_dict = {field: value for (field, _, _), value in zip(FIELDS, values)}

    if not plants_dict["name"]:
        return "植物名は必須です"

    plantsdb.save_plants(plants_dict)

    return f'{plants_dict["name"]} を保存しました'


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
    print("called")
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
    print("update_table called", save_message, delete_message)
    if keyword:
        rows, columns = plantsdb.get_data(keyword)
    else:
        rows, columns = plantsdb.get_data()
    print(rows[-1])
    print(len(rows))
    df = pd.DataFrame(rows, columns=columns)

    return (
        df.to_dict("records"),
        [{"name": c, "id": c} for c in df.columns],
    )


if __name__ == "__main__":
    app.run(debug=True, port=8049)
