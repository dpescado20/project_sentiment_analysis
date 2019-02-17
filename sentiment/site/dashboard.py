import dash_html_components as html
import dash_bootstrap_components as dbc
from sentiment import dashapp
from sentiment.site import dash_components as dac

dashapp.layout = html.Div(
    [
        dac.navbar,
        html.Br(),
        dac.create_body(
            [
                dac.create_card_main(
                    title='Twitter Sentiments Score',
                    content=[
                        dbc.Col(
                            dac.create_card_main(title='graph area', content=None),
                        ),
                        dbc.Col(
                            dac.create_card_main(title='explanation', content=None),
                        )
                    ]
                ),
                html.Br(),
                dac.create_card_main(
                    title='Facebook Sentiments Score',
                    content=[
                        dbc.Col(
                            dac.create_card_main(title='graph area', content=None),
                        ),
                        dbc.Col(
                            dac.create_card_main(title='explanation', content=None),
                        )
                    ]
                ),
                html.Br(),
                dac.create_card_main(
                    title='Youtube Sentiments Score',
                    content=[
                        dbc.Col(
                            dac.create_card_main(title='graph area', content=None),
                        ),
                        dbc.Col(
                            dac.create_card_main(title='explanation', content=None),
                        )
                    ]
                )
            ]
        )
    ]
)
