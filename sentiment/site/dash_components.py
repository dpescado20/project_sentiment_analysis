import dash_html_components as html
import dash_bootstrap_components as dbc

navbar = dbc.NavbarSimple(
    children=[
        # dbc.NavItem(dbc.NavLink('DASHBOARD', href='#')),
        dbc.NavItem(dbc.NavLink('API', href='/api/', external_link=True)),
        dbc.NavItem(dbc.NavLink('Login', href='#'))
    ],
    brand='SENTIMENT ANALYSIS',
    brand_href='/',
    brand_external_link=True
)


def create_body(body):
    container = dbc.Container(body)
    return container


# # # # DBC CARDS FUNCTIONS # # # #
def create_card_main(title, content):
    card = dbc.Card(
        dbc.CardBody(
            [
                dbc.CardTitle(html.H5(title)),
                dbc.CardText(dbc.Row(content))
            ]
        )
    )
    return card
