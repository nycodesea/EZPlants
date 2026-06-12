import plotly.express as px
import pandas as pd

name = "tomato"

df = pd.DataFrame(
    [
        dict(Task="Tomato", Start="2009-01-01", Finish="2009-03-28", Type="植付"),
        dict(Task="Tomato", Start="2009-03-05", Finish="2009-04-15", Type="種まき"),
        dict(Task="Tomato", Start="2009-02-20", Finish="2009-05-30", Type="収穫"),
    ]
)

fig = px.timeline(df, x_start="Start", x_end="Finish", y="Type", color="Type")
fig.update_yaxes(autorange="reversed")  # otherwise tasks are listed from the bottom up
fig.show()
