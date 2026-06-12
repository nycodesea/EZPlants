from logging import config

import matplotlib.pyplot as plt
import numpy as np
import plotly.graph_objects as go
import pandas as pd


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
        alpha=0.3,
    )
    ax.barh(y=name, left=temp_min, width=width, color="green")

    plt.xlabel("Temperature (°C)")
    plt.show()


def show_gantt_chart(rows):
    if not rows:
        print("No gantt data found.")
        return

    name, fertilizer, sow_start, sow_end, harvest_start, harvest_end = rows[0]

    fig = go.Figure()

    events = [
        ("種まき", sow_start, sow_end),
        ("肥料", fertilizer, fertilizer),
        ("収穫", harvest_start, harvest_end),
    ]

    for event, start, end in events:

        if start is None:
            continue

        fig.add_bar(
            y=[event],
            x=[end - start + 1],
            base=[start],
            orientation="h",
        )

    fig.update_xaxes(
        tickmode="array",
        tickvals=list(range(1, 13)),
        ticktext=[f"{i}月" for i in range(1, 13)],
        range=[0.5, 12.5],
    )

    fig.update_layout(
        title=f"{name} 栽培カレンダー",
        height=300,
        showlegend=False,
    )

    fig.show(config={"responsive": True})
