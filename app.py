# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Output, Input
import plotly.express as px
import pandas as pd

app = Dash(__name__)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
df = pd.DataFrame({
    "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
    "Amount": [4, 1, 2, 2, 4, 5],
    "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
})

fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")

"""
    1. Basic setup: We set up the basic application and page view
    At this point we dont apply any styling
"""
# app.layout = html.Div(children=[
#     html.H1(children='Global Fruits Market'),
#     html.Div(children='''
#         Comparing fruits production in different markets.
#     '''),
# ])

"""
    2. Appending Chart: appending a simple chart
"""

# app.layout = html.Div(children=[
#     html.H1(children='Global Fruits Market'),
#     html.Div(children='''
#         Comparing fruits production in different markets.
#     '''),
#         dcc.Graph(
#             id='example-graph',
#             figure=fig
#         )
# ])


"""
    3. Adding inline styling: see the changes in styling
    of html elements. At this point all styling is applied inline.
    This creates another issue: code gets larger, hence confusing
"""

# app.layout = html.Div(children=[
#     html.H1(
#         children='Global Fruits Market',
#         style={
#             'textAlign': 'center',
#             'color': '#FFFF'
#         }
#     ),
# 
#     html.Div(children='Comparing fruits production in different markets.', style={
#         'textAlign': 'center',
#         'color': '#FFFF',
#     }),
# 
# 
#     dcc.Graph(
#         id='example-graph',
#         figure=fig,
#     )
# ], style={'backgroundColor': '#051C2C'})


"""
    4. Moving styling to CSS file: as we want to stick to the clean code,
    moving all inline styling to a separate CSS sheet
"""
# app.layout = html.Div(children=[
#     html.Div(className='header', children=[
#         html.H1(
#             children='Global Fruits Market',
#         ),
#         html.Div(children='Comparing fruits production in different markets'),
#     ]),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig,
#     ),
# ])


"""
    5. Core components
    
    The Dash Core Components module (dash.dcc) includes a component called Graph.
    Graph renders interactive data visualizations using the open source plotly.js 
    JavaScript graphing library. Plotly.js supports over 35 chart types and renders 
    charts in both vector-quality SVG and high-performance WebGL.
"""

df_scatter = pd.read_csv('https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

fig_scatter = px.scatter(df_scatter, x="gdp per capita", y="life expectancy",
                         size="population", color="continent", hover_name="country",
                         log_x=True, size_max=60)

app.layout = html.Div(children=[
    html.Div(className='header', children=[
        html.H1(
            children='Global Fruits Market',
        ),
        html.Div(children='Comparing fruits production in different markets'),
    ]),
    html.Div(className='select-option', children=[
        html.P('Select location'),
        dcc.RadioItems(id='select_option', options=['New York City', 'Montréal', 'San Francisco'], value='Montréal'),
    ], style={'padding': 10, 'flex': 1}),
    dcc.Graph(
        id='example-graph',
        figure=fig,
    ),
    html.Div(className='sub-header', children=[
        html.H2(children='GDP per capita')
    ]),
    dcc.Graph(
        id='example-scatter',
        figure=fig_scatter,
    )
])


@app.callback(
    Output('example-graph', 'figure'),
    Input('select_option', 'value'))
def displayFigure(selected_city):
    ny = 'New York City'
    sn = 'San Francisco'
    dfc = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["Average", "Average", "Average", "Montreal", "Montreal", "Montreal"]
    })
    if selected_city == ny:
        dfc = pd.DataFrame({
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 6, 2, 4],
            "City": ["Average", "Average", "Average", ny, ny, ny]
        })
    elif selected_city == sn:
        dfc = pd.DataFrame({
            "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
            "Amount": [4, 1, 2, 1, 5, 3],
            "City": ["Average", "Average", "Average", ny, ny, ny]
        })

    return px.bar(dfc, x="Fruit", y="Amount", color="City", barmode="group")


if __name__ == '__main__':
    app.run_server(debug=True)