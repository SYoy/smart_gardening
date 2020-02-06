import plotly
import plotly.graph_objs as go
import random

def create_figure():
    count = 25
    xScale = [i for i in range(0, count)]
    yScale = [random.randint(135, 213)  for i in range(0, count)]

    layout = go.Layout(autosize=True)

    # Create a trace
    trace = go.Scatter(x=xScale, y=yScale)
    fig = go.Figure(data=trace, layout=layout)
    fig.update_yaxes(automargin=True)
    fig.update_xaxes(automargin=True)
    div = plotly.offline.plot(fig, show_link=False, output_type="div")

    return div