import pandas as pd
# import datetime
import plotly
import plotly.graph_objs as go
import json


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
        'datetime': data["counter"],
        'nose_x': data["paddlePosition.x"],  # [0.1, -0.2, 0.3],
        'nose_y': data["paddlePosition.y"],  # [0.2, -0.3, 0.4],
        'ball_x': data["ballPosition.x"],  # [-0.1, 0.2, -0.3],
        'ball_y': data["ballPosition.y"],  # [-0.2, 0.3, -0.4]
    })

    # create the scatter trace for nose position
    nose_trace = go.Scatter(
        x=df['nose_x'],
        y=df['nose_y'],
        name='Nose Position',
        mode='markers',
        marker=dict(
            size=10,
            color='blue'
        )
    )

    # create the scatter trace for ball position
    ball_trace = go.Scatter(
        x=df['ball_x'],
        y=df['ball_y'],
        name='Ball Position',
        mode='markers',
        marker=dict(
            size=10,
            color='red'
        )
    )

    # create the layout with a datetime slider and the nose and ball traces
    layout = go.Layout(
        xaxis=dict(
            range=[-200, 200],
            fixedrange=True,
            title='Nose Position X',
        ),
        yaxis=dict(
            range=[-100, 100],
            fixedrange=True,
            title='Nose Position Y',
        ),
        updatemenus=[
            dict(
                type='buttons',
                showactive=False,
                buttons=[
                    dict(
                        label='Play',
                        method='animate',
                        args=[None, dict(frame=dict(
                            duration=100), fromcurrent=True)]
                    ),
                    dict(
                        label='Pause',
                        method='animate',
                        args=[[None], dict(frame=dict(
                            duration=0), mode="immediate", transition=dict(duration=0))]
                    )
                ]
            )
        ],
        sliders=[
            dict(
                steps=[],
                active=0,
                yanchor='top',
                xanchor='left',
                pad=dict(t=50, b=10),
                len=0.9,
                x=0.1,
                y=0,
                transition={'duration': 300, 'easing': 'cubic-in-out'}
            )
        ],
        showlegend=True
    )

    # create the frames for the animation
    frames = [go.Frame(data=[go.Scatter(x=[df['nose_x'][i]], y=[df['nose_y'][i]], mode='markers', name='nose'),
                             go.Scatter(x=[df['ball_x'][i]], y=[df['ball_y'][i]], mode='markers', name='ball')])
              for i in range(len(df))]

    # set up the layout
    layout = go.Layout(width=800, height=600, title='Nose and Ball Positions',
                       xaxis=dict(range=[-200, 200], title='X Position'),
                       yaxis=dict(range=[-100, 100], title='Y Position'),
                       updatemenus=[dict(type='buttons', showactive=False,
                                         buttons=[dict(label='Play',
                                                       method='animate',
                                                       args=[None, dict(frame=dict(duration=300, redraw=True),
                                                                        fromcurrent=True,
                                                                        transition=dict(
                                                                            duration=0)
                                                                        )
                                                             ]
                                                       ),
                                                  dict(label='Pause',
                                                       method='animate',
                                                       args=[[None], dict(frame=dict(duration=0),
                                                                          mode='immediate',
                                                                          transition=dict(
                                                                              duration=0)
                                                                          )
                                                             ]
                                                       )
                                                  ]
                                         )
                                    ])

    # add the sliders to the layout
    layout.update(sliders=[dict(steps=[dict(method='animate', args=[None, dict(frame=dict(duration=300, redraw=True),
                                                                               fromcurrent=True,
                                                                               transition=dict(
                                                                                   duration=0)
                                                                               )
                                                                    ],
                                            label=df['datetime'][i]
                                            )
                                       for i in range(len(df))
                                       ],
                                transition=dict(duration=0),
                                x=0,
                                y=0,
                                len=1.0
                                )
                           ])

    # update the layout to include the slider
    layout.update(sliders=layout['sliders'])

    # create the figure object and display the animation
    fig = go.Figure(data=[go.Scatter(x=[df['nose_x'][0]], y=[df['nose_y'][0]], mode='markers', name='nose'),
                          go.Scatter(x=[df['ball_x'][0]], y=[df['ball_y'][0]], mode='markers', name='ball')],
                    layout=layout,
                    frames=frames)
    # graph_json = json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)
    graph_json = fig.to_json()
    # fig.show()
    return graph_json
