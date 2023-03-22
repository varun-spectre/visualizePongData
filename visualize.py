import pandas as pd
# import datetime
import plotly
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import json
import plotly.offline as pyo


def visualize(file):
    data = pd.read_csv(file)
    datetimes = []
    for i in data['timestamp']:
        datetimes.append(pd.Timestamp(i))
    data["datetimes"] = datetimes
    data['counter'] = range(1, len(data)+1)
    data["counter"] = data['counter'].astype(str)

    # create a sample DataFrame with datetime, nose position, and ball position
    df = pd.DataFrame({
        # ['2022-01-01 00:00:00', '2022-01-01 00:01:00', '2022-01-01 00:02:00'],
        'counter': data["counter"].astype(int),
        'nose_x': data["paddlePosition.x"],  # [0.1, -0.2, 0.3],
        'nose_y': data["paddlePosition.y"],  # [0.2, -0.3, 0.4],
        'ball_x': data["ballPosition.x"],  # [-0.1, 0.2, -0.3],
        'ball_y': data["ballPosition.y"],  # [-0.2, 0.3, -0.4]
    })

    # Create figure layout
    fig = make_subplots(rows=1, cols=1)

    # Define frames for animation
    frames = [go.Frame(data=[go.Scatter(x=df[df['counter'] == i]['ball_x'],
                                        y=df[df['counter'] == i]['ball_y'],
                                        mode='markers',
                                        marker=dict(color='blue', size=10),
                                        name='Ball Position'),
                             go.Scatter(x=df[df['counter'] == i]['nose_x'],
                                        y=df[df['counter'] == i]['nose_y'],
                                        mode='markers',
                                        marker=dict(color='red', size=10),
                                        name='Nose Position')
                             ],
                       name=str(i)
                       ) for i in df['counter'].unique()]

    # Create the initial trace
    ball_trace = go.Scatter(x=df['ball_x'], y=df['ball_y'], mode='markers', marker=dict(
        color='blue', size=10), name='Ball Position')
    nose_trace = go.Scatter(x=df['nose_x'], y=df['nose_y'], mode='markers', marker=dict(
        color='red', size=10), name='Nose Position')

    # Add the initial trace to the figure
    fig.add_trace(ball_trace, row=1, col=1)
    fig.add_trace(nose_trace, row=1, col=1)

    # Define the animation
    fig.update(frames=frames)
    fig.update_layout(updatemenus=[dict(type='buttons',
                                        showactive=False,
                                        buttons=[dict(label='Play',
                                                      method='animate',
                                                      args=[None, dict(frame=dict(duration=300, redraw=True), fromcurrent=True, transition=dict(duration=0, easing='linear'), mode='immediate')]),
                                                 dict(label='Pause',
                                                      method='animate',
                                                      args=[[None], dict(frame=dict(duration=0, redraw=True), mode='immediate', transition=dict(duration=0))])],
                                        direction='left',
                                        pad=dict(r=10, t=87),
                                        x=0.1,
                                        y=0,
                                        xanchor='right',
                                        yanchor='top',
                                        active=0
                                        )
                                   ],
                      sliders=[dict(
                          visible=True,
                          active=0,
                          y=0,
                          x=0.1,
                          xanchor='right',
                          yanchor='top',
                          len=0.9,
                          pad=dict(t=10, b=10, l=100, r=10),
                          steps=[dict(
                              label=str(i),
                              method='animate',
                              args=[[str(i)], dict(frame=dict(duration=300, redraw=True), mode='immediate', transition=dict(duration=0))])
                              for i in df['counter'].unique()
                          ]
                      )]
                      )

    # Define animation settings
    fig.update_layout(
        xaxis=dict(range=[-200, 200]),
        yaxis=dict(range=[-100, 100]),
        title='Ball and Nose Positions'
    )
    # graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    # graph_json = fig.to_json()
    # fig.show()
    # Use the `plot()` function to create an HTML file
    pyo.plot(fig, filename='templates/results.html', auto_open=False)
    return True
