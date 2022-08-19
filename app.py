# Run this app with `python app.py` and
# visit http://127.0.0.1:8050/ in your web browser.

from dash import Dash, html, dcc, Output, Input, ClientsideFunction
import plotly.express as px
import pandas as pd

app = Dash(__name__)

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
    - assume you have a "long-form" data frame
    - see https://plotly.com/python/px-arguments/ for more options
"""
#
# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
# app.layout = html.Div(children=[
#     html.H1(children='Global Fruits Market'),
#     html.Div(children='''
#         Comparing fruits production in different markets.
#     '''),
#     dcc.Graph(
#         id='example-graph',
#         figure=fig
#     )
# ])

"""
    3. Adding inline styling: see the changes in styling
    of html elements. At this point all styling is applied inline.
    This creates another issue: code gets larger, hence confusing
"""

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
#
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

# df = pd.DataFrame({
#     "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
#     "Amount": [4, 1, 2, 2, 4, 5],
#     "City": ["SF", "SF", "SF", "Montreal", "Montreal", "Montreal"]
# })
#
# fig = px.bar(df, x="Fruit", y="Amount", color="City", barmode="group")
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

df_scatter = pd.read_csv(
    'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')

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
        dcc.RadioItems(id='select_option', options=['New York City', 'Montreal', 'San Francisco'], value='Montreal'),
    ], style={'padding': 10, 'flex': 1}),
    dcc.Graph(
        id='example-graph',
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
def display_figure(selected_city):
    data = get_data_sets()
    dfc = data[selected_city]
    return px.bar(dfc, x="Fruit", y="Amount", color="City", barmode="group")


"""
    6. JavaScript in Dash
    
    6.1 Dash uses React under the hood, specifically in the dash-renderer. 
    The dash-renderer is basically just a React app that renders the layout defined in your
    Dash app as app.layout. It is also responsible for assigning the callbacks you write in Dash 
    to the proper components, and keeping everything up-to-date.
    
    6.2 You can write some of the client side callback in JavaScript right in the middle of your
    Dash Python code (see example below). This code will be loaded to browser, thus
    decreasing burden on dash. 
    
    Example
    In our example we add a function to redlect the inpout in the text field. 
    we could do it via callbacks, but lets reduce the load on our Dash Engine
    and put this logic into our browser instead
"""

# df_scatter = pd.read_csv(
#     'https://gist.githubusercontent.com/chriddyp/5d1ea79569ed194d432e56108a04d188/raw/a9f9e8076b837d541398e999dcbac2b2826a81f8/gdp-life-exp-2007.csv')
#
# fig_scatter = px.scatter(df_scatter, x="gdp per capita", y="life expectancy",
#                          size="population", color="continent", hover_name="country",
#                          log_x=True, size_max=60)
#
# app.layout = html.Div(children=[
#     html.Div(className='header', children=[
#         html.H1(
#             children='Global Fruits Market',
#         ),
#         html.Div(children='Comparing fruits production in different markets'),
#     ]),
#     html.Div(className='select-option', children=[
#         html.P('Select location'),
#         dcc.RadioItems(id='select_option', options=['New York City', 'Montreal', 'San Francisco'], value='Montreal'),
#     ], style={'padding': 10, 'flex': 1}),
#     dcc.Graph(
#         id='example-graph',
#     ),
#     html.Div(className='sub-header', children=[
#         html.H2(children='GDP per capita')
#     ]),
#     dcc.Graph(
#         id='example-scatter',
#         figure=fig_scatter,
#     ),
#     html.Br(),
#     html.Div(className='sub-header', children=[
#         html.H2(children='Insert your values here')
#     ]),
#     html.Div(id='input_wrapper', className='input-wrapper',
#              children=[
#                  dcc.Input(
#                      id="input_example",
#                      type='text',
#                      placeholder="Put some text here",
#                  ),
#                  html.Div(id="output_for_input")
#              ]),
# ])
#
# @app.callback(
#     Output('example-graph', 'figure'),
#     Input('select_option', 'value'))
# def display_figure(selected_city):
#     data = get_data_sets()
#     dfc = data[selected_city]
#     return px.bar(dfc, x="Fruit", y="Amount", color="City", barmode="group")


# """
# #example for input field with normal callback
#
# @app.callback(
#     Output("output_for_input", "children"),
#     [Input("input_example", "value")],
# )
# def normal_callback(val):
#     return val
# """


#example for input field with client side call ( a call from browser)
# you can put this code to js file
# under /assets/*.js. But the must be additional configuration (see example below)
# app.clientside_callback(
#     """
#     function(val) {
#         return val;
#     }
#     """,
#     Output("output_for_input", "children"),
#     Input("input_example", "value"),
# )


# For this specific example, the code is located at app.js
# The code below ties up the dash to the code definition in js file
# app.clientside_callback(
#     ClientsideFunction(
#         namespace='clientside',
#         function_name='input_change_function'
#     ),
#     Output('output_for_input', 'children'),
#     Input('input_example', 'value'),
# )



# # Helper functions
def get_data_sets():
    ny = 'New York City'
    sn = 'San Francisco'
    mn = "Montreal"

    df1 = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 2, 4, 5],
        "City": ["SF", "SF", "SF", ny, ny, ny]
    })

    df2 = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 6, 2, 4],
        "City": ["Average", "Average", "Average", sn, sn, sn]})

    df3 = pd.DataFrame({
        "Fruit": ["Apples", "Oranges", "Bananas", "Apples", "Oranges", "Bananas"],
        "Amount": [4, 1, 2, 1, 5, 3],
        "City": ["Average", "Average", "Average", mn, mn, mn]})

    return {ny: df1, sn: df2, mn: df3}



if __name__ == '__main__':
    app.run_server(debug=True)
