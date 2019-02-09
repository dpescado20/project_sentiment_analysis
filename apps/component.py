import dash_html_components as html
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem()
    ],
    brand='Sentiment Analysis',
    brand_href='#',
    sticky='top'
)

jumbotron = dbc.Jumbotron(
    [
        html.H1('Jumbotron', className='display-3'),
        html.P(
            'Use a jumbotron to call attention to featured content or information',
            className='lead'
        ),
        html.Hr(className='my-2'),
        html.P(
            'Jumbotrons use utility classes for typography and spacing to suit the larger container'
        )
    ]
)
