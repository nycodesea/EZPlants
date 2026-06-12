from dash import Dash, html, dcc, dash_table, Input, Output
import pandas as pd
import plantsdb
from graph import create_temp_range, create_gantt_chart
from plantsdb import DB
import graph

TABLE = "plants_data"
FAVTABLE = "plants_fav_data"

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
        dash_table.DataTable(
            id="plants-table",
            page_size=20,
        ),
        dcc.Graph(id="temp-graph"),
        dcc.Graph(id="gantt-graph"),
    ],
    style={
        "backgroundColor": "#FDF3DDFF",
        "minHeight": "100vh",
        "padding": "20px",
    },
)


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


@app.callback(
    Output("plants-table", "data"),
    Output("plants-table", "columns"),
    Input("search-box", "value"),
)
def update_table(keyword):

    if keyword:
        rows, columns = plantsdb.get_data(keyword)
    else:
        rows, columns = plantsdb.get_data()

    df = pd.DataFrame(rows, columns=columns)

    return (
        df.to_dict("records"),
        [{"name": c, "id": c} for c in df.columns],
    )


if __name__ == "__main__":
    app.run(debug=True, port=8049)
