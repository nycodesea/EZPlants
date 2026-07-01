from logging import config

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd
from plantsdb import get_chart_data


def show_temp_range(rows):

    name = [r[0] for r in rows]
    temp_min = [r[1] for r in rows]
    temp_max = [r[2] for r in rows]

    width = [max_t - min_t for min_t, max_t in zip(temp_min, temp_max)]
    gradient = np.linspace(0, 1, 500)
    gradient = np.vstack((gradient, gradient))

    fig, ax = plt.subplots()
    ax.imshow(
        gradient,
        extent=[-20, 50, -1, len(name)],
        aspect="auto",
        cmap="coolwarm",
        alpha=0.8,
    )
    ax.barh(y=name, left=temp_min, width=width, color="green")

    plt.xlabel("Temperature (°C)")
    plt.show()


def create_temp_range(rows):

    fig = go.Figure()

    for temp in range(-20, 50):

        ratio = (temp + 20) / 70

        fig.add_vrect(
            x0=temp,
            x1=temp + 1,
            fillcolor=f"rgba({int(255*ratio)},0,{int(255*(1-ratio))},0.15)",
            line_width=0,
            layer="below",
        )

    names = [r[0] for r in rows]
    temp_min = [r[1] for r in rows]
    temp_max = [r[2] for r in rows]

    fig.add_bar(
        y=names,
        x=[mx - mn for mn, mx in zip(temp_min, temp_max)],
        base=temp_min,
        orientation="h",
        opacity=0.9,
    )
    fig.update_layout(
        title="Temperature Range",
        xaxis_title="Temperature (°C)",
        height=max(200, len(names) * 50),
        bargap=0.5,
        margin=dict(l=60, r=40, t=60, b=10),
    )

    return fig


def create_gantt_chart(rows):
    if not rows:
        return go.Figure()

    name, fertilizer, sow_start, sow_end, harvest_start, harvest_end = rows[0]

    fig = go.Figure()

    events = [
        ("Sowing", sow_start, sow_end),
        ("Fertilizing", fertilizer, fertilizer),
        ("Harvest", harvest_start, harvest_end),
    ]

    for event, start, end in events:

        if start is None or end is None:
            continue

        fig.add_bar(
            y=[event],
            x=[end - start + 1.6],
            base=[start - 0.3],
            orientation="h",
            text=[event],
            textposition="inside",
            insidetextanchor="middle",
        )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=[f"{i}" for i in range(1, 13)],
        range=[0.5, 12.5],
    )

    fig.update_layout(
        title=f"{name} Growing Calendar",
        height=max(200, len(event) * 50),
        showlegend=False,
        margin=dict(l=40, r=40, t=30, b=40),
        bargap=0.5,
    )

    return fig


def create_watering_graph():
    plant_ids, watering_times, watering_durations, moisture_before, moisture_after = (
        get_chart_data()
    )
    fig = go.Figure()

    fig.add_trace(
        go.Bar(
            x=watering_times,
            y=watering_durations,
            name="Watering Duration",
        )
    )
    fig.update_layout(
        title="Watering Logs",
        xaxis_title="Date and Time",
        yaxis_title="Duration (milliseconds)",
    )
    return fig
