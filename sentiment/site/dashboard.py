import dash_core_components as dcc
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_table as dashtable
from dash.dependencies import Input, Output, State
from plotly import graph_objs as go

from sentiment import dashapp

__navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink('API', href='/api/', external_link=True))
    ],
    brand='SENTIMENT ANALYZER',
    brand_href='#',
    sticky='top'
)

__metrics = dbc.Container(
    [
        html.Br(),
        dbc.Card(
            [
                dbc.CardHeader(html.H5('MODEL TRAINING METRICS')),
                # dbc.CardBody(id='card-body-metrics')
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col('DATA SET'),
                            dbc.Col('MODEL'),
                            dbc.Col('CONFUSION MATRIX'),
                            dbc.Col('CLASSIFICATION REPORT'),
                        ]
                    )
                )
            ]
        ),
        html.Br()
    ]
)
__upper = dbc.Container(
    [
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    [
                        dbc.CardHeader(html.H5('FILTERS')),
                        dbc.CardBody(
                            dbc.InputGroup(
                                [
                                    dbc.InputGroupAddon(
                                        dbc.Button('GENERATE SENTIMENT', color='primary', id='btn-process-tweet'),
                                        addon_type='append'
                                    ),
                                    dbc.Input(placeholder='tweets : event, person, place and etc ...',
                                              value='trump',
                                              id='text-track'),
                                    dbc.Input(placeholder='facebook : page id ...',
                                              value='DonaldTrump',
                                              id='text-page')
                                ], size='sm'
                            )
                        )
                    ]
                )
            )
        ),
        html.Br(),
        html.Br()
    ]
)

__overview = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H5('OVERVIEW : COMPARISON OF SENTIMENTS')),
                # dbc.CardBody(id='card-body-overview')
                dbc.CardBody(
                    dbc.Row(
                        [
                            dbc.Col('TWITTER'),
                            dbc.Col('YOUTUBE'),
                            dbc.Col('FACEBOOK'),
                            dbc.Col('REDDIT'),
                        ]
                    )
                )
            ]
        ),
        html.Br(),
        html.Br()
    ]
)

__twitter = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H5('TWITTER'), style={'background-color': '#38A1F3', 'color': 'white'}),
                dbc.CardBody(id='card-body-twitter')
            ]
        ),
        html.Br(),
        html.Br()
    ]
)

__youtube = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H5('YOUTUBE'), style={'background-color': '#FF0000', 'color': 'white'}),
                dbc.CardBody(id='card-body-youtube')
            ]
        ),
        html.Br(),
        html.Br()
    ]
)

__facebook = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H5('FACEBOOK'), style={'background-color': '#3B5998', 'color': 'white'}),
                dbc.CardBody(id='card-body-facebook')
            ]
        ),
        html.Br(),
        html.Br()
    ]
)

__reddit = dbc.Container(
    [
        dbc.Card(
            [
                dbc.CardHeader(html.H5('REDDIT'), style={'background-color': '#FF4301', 'color': 'white'}),
                dbc.CardBody(id='card-body-reddit')
            ]
        ),
        html.Br(),
        html.Br()
    ]
)

dashapp.layout = html.Div([__navbar, __metrics, __upper, __overview, __twitter, __youtube, __facebook, __reddit])
# dashapp.layout = html.Div([__navbar, __metrics, __upper, __overview, __twitter])


@dashapp.callback(
    Output('card-body-twitter', 'children'),
    [Input('btn-process-tweet', 'n_clicks')],
    [State('text-track', 'value')]
)
def update_twitter_container(n_clicks, value):
    from sentiment.site.data import DataProcess, DataResult
    datapro = DataProcess()
    datares = DataResult(datapro.twitter_convert_searchResult_df(value))

    df_row = datares.get_df_row_count()
    df_original = datares.get_df_original_tweet()
    pos = datares.get_df_positive_score()
    neg = datares.get_df_negative_score()
    df_bow = datares.get_df_features()

    children = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5('SENTIMENT', className='card-title'),
                                dcc.Graph(
                                    # FIGURE DONUT GRAPH
                                    figure=go.Figure(
                                        data=[
                                            go.Pie(
                                                values=[pos, neg],
                                                labels=['Positive', 'Negative'],
                                                hoverinfo='label+percent',
                                                hole=0.4
                                            )
                                        ],
                                        layout=go.Layout(
                                            margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                        )
                                    ),
                                    style={'height': 300}
                                )
                            ]
                        )
                    )
                ),
                # dbc.Col(
                #    dbc.Card(
                #        dbc.CardBody(
                #            [
                #                dbc.CardTitle(html.H5('METRICS')),
                #                dbc.CardText([
                #                    html.H5('CONFUSION MATRIX'),
                #                    html.H5('CLASSIFICATION REPORT')
                #                ])
                #            ]
                #        )
                #    )
                # )
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('TWEETS ({})'.format(df_row), className='card-title'),
                            dashtable.DataTable(
                                data=df_original.to_dict('rows'),
                                columns=[{'id': i, 'name': i} for i in df_original.columns],
                                style_table={
                                    'maxHeight': 300,
                                    'overflowY': 'scroll'
                                },
                                fixed_rows=1,
                                style_cell={
                                    # all three widths are needed
                                    'maxWidth': '100px',
                                    'whiteSpace': 'normal',
                                    'textAlign': 'center',
                                    'padding': '5px'
                                },
                                css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                                style_as_list_view=True,
                                style_header={'fontWeight': 'bold', }
                            )
                        ]
                    )
                )
            )
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('WORD FREQUENCY', className='card-title'),
                            dcc.Graph(
                                figure=go.Figure(
                                    data=[
                                        go.Bar(
                                            x=df_bow.Word,
                                            y=df_bow.Count,
                                            name='Word'
                                        )
                                    ],
                                    layout=go.Layout(
                                        margin=go.layout.Margin(l=40, r=0, t=40, b=80)
                                    )
                                ),
                                style={'height': 300}
                            )
                        ]
                    )
                )
            )
        )
    ]

    return children

@dashapp.callback(
    Output('card-body-youtube', 'children'),
    [Input('btn-process-tweet', 'n_clicks')],
    [State('text-page', 'value')]
)
def update_youtube_container(n_clicks, value):
    from sentiment.site.data import DataProcess, DataResult
    datapro = DataProcess()
    datares = DataResult(datapro.youtube_convert_searchResult_df(value))

    df_row = datares.get_df_row_count()
    df_original = datares.get_df_original_tweet()
    pos = datares.get_df_positive_score()
    neg = datares.get_df_negative_score()
    df_bow = datares.get_df_features()

    children = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5('SENTIMENT',className='card-title'),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            # FIGURE DONUT GRAPH
                                            figure=go.Figure(
                                                data=[
                                                    go.Pie(
                                                        values=[pos, neg],
                                                        labels=['Positive', 'Negative'],
                                                        hoverinfo='label+percent',
                                                        hole=0.4
                                                    )
                                                ],
                                                layout=go.Layout(
                                                    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                )
                                            ),
                                            style={'height': 300}
                                        )
                                    ]
                                )
                            ]
                        )
                    )

                ),
                # dbc.Col(
                #     dbc.Card(
                #        dbc.CardBody(
                #            [
                #                dbc.CardTitle(html.H5('METRICS')),
                #                dbc.CardText([
                #                    html.H5('CONFUSION MATRIX'),
                #                    html.H5('CLASSIFICATION REPORT')
                #                ])
                #            ]
                #        )
                #    )
                # )
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('COMMENTS ({})'.format(df_row), className='card-title'),
                            html.Div(dashtable.DataTable(
                                data=df_original.to_dict('rows'),
                                columns=[{'id': i, 'name': i} for i in df_original.columns],
                                style_table={
                                    'maxHeight': 300,
                                    'overflowY': 'scroll'
                                },
                                fixed_rows=1,
                                style_cell={
                                    # all three widths are needed
                                    'maxWidth': '100px',
                                    'whiteSpace': 'normal',
                                    'textAlign': 'center',
                                    'padding': '5px'
                                },
                                css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                                style_as_list_view=True,
                                style_header={'fontWeight': 'bold', }
                            ))
                        ]
                    )
                )
            )
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('WORD FREQUENCY', className='card-title'),
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[
                                                go.Bar(
                                                    x=df_bow.Word,
                                                    y=df_bow.Count,
                                                    name='Word'
                                                )
                                            ],
                                            layout=go.Layout(
                                                margin=go.layout.Margin(l=40, r=0, t=40, b=80)
                                            )
                                        ),
                                        style={'height': 300}
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        )
    ]

    return children


@dashapp.callback(
    Output('card-body-facebook', 'children'),
    [Input('btn-process-tweet', 'n_clicks')],
    [State('text-track', 'value')]
)
def update_facebook_container(n_clicks, value):
    from sentiment.site.data import DataProcess, DataResult
    datapro = DataProcess()
    datares = DataResult(datapro.facebook_convert_searchResult_df(value))

    df_row = datares.get_df_row_count()
    df_original = datares.get_df_original_post()
    likes = datares.get_df_likes_sum()
    df_bow = datares.get_df_features()

    children = [
        dbc.Row(
            [
                dbc.Col(
                    dbc.Card(
                        dbc.CardBody(
                            [
                                html.H5('SENTIMENT', className='card-title'),
                                html.Div(
                                    [
                                        dcc.Graph(
                                            # FIGURE DONUT GRAPH
                                            figure=go.Figure(
                                                data=[
                                                    go.Pie(
                                                        values=[likes, 5000, 5000, 5000, 5000, 5000],
                                                        labels=['Like', 'Love', 'Haha', 'Angry', 'Wow', 'Sad'],
                                                        hoverinfo='label+percent',
                                                        hole=0.4
                                                    )
                                                ],
                                                layout=go.Layout(
                                                    margin=go.layout.Margin(l=40, r=0, t=40, b=30)
                                                )
                                            ),
                                            style={'height': 300}
                                        )
                                    ]
                                )
                            ]
                        )
                    )

                ),
                # dbc.Col(
                #    dbc.Card(
                #        dbc.CardBody(
                #            [
                #                dbc.CardTitle(html.H5('METRICS')),
                #                dbc.CardText([
                #                    html.H5('CONFUSION MATRIX'),
                #                    html.H5('CLASSIFICATION REPORT')
                #                ])
                #            ]
                #        )
                #    )
                # )
            ]
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('POSTS ({})'.format(df_row), className='card-title'),
                            html.Div(dashtable.DataTable(
                                data=df_original.to_dict('rows'),
                                columns=[{'id': i, 'name': i} for i in df_original.columns],
                                style_table={
                                    'maxHeight': 300,
                                    'overflowY': 'scroll'
                                },
                                fixed_rows=1,
                                style_cell={
                                    # all three widths are needed
                                    'maxWidth': '100px',
                                    'whiteSpace': 'normal',
                                    'textAlign': 'center',
                                    'padding': '5px'
                                },
                                css=[{
                                    'selector': '.dash-cell div.dash-cell-value',
                                    'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
                                }],
                                style_as_list_view=True,
                                style_header={'fontWeight': 'bold', }
                            ))
                        ]
                    )
                )
            )
        ),
        html.Br(),
        dbc.Row(
            dbc.Col(
                dbc.Card(
                    dbc.CardBody(
                        [
                            html.H5('WORD FREQUENCY', className='card-title'),
                            html.Div(
                                [
                                    dcc.Graph(
                                        figure=go.Figure(
                                            data=[
                                                go.Bar(
                                                    x=df_bow.Word,
                                                    y=df_bow.Count,
                                                    name='Word'
                                                )
                                            ],
                                            layout=go.Layout(
                                                margin=go.layout.Margin(l=40, r=0, t=40, b=80)
                                            )
                                        ),
                                        style={'height': 300}
                                    )
                                ]
                            )
                        ]
                    )
                )
            )
        )
    ]

    return children
