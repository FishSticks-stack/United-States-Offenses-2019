"""interactive map/bar graph using plotly dash."""
import json
import dash
# import dash_core_components as dcc ORIGINAL USED BUT NOW DEPRECATED! Replaced with below \/
from dash import dcc
# import dash_html_components as html ORIGINAL USED BUT NOW DEPRECATED! Replaced with below \/
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# to customize style
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

# assume you have a "long-form" data frame
# see https://plotly.com/python/px-arguments/ for more options
data = pd.read_csv('United_States_Offense_Type_by_Agency_2019.csv')

with open('gz_2010_us_040_00_20m.json', 'r', encoding="utf-8") as f:
    stateFile = json.load(f)
    states = stateFile['features']

# take state name
name, location, totalCrimes, stateName = [], [], [], []
# adding all states in name[]
for x in states:
    names = x['properties']['NAME']
    stateNumber = x['properties']['STATE']
    name.append(names)
    # getting state locations
    loc = x['geometry']['coordinates'][0]
    location.append(loc)
name = sorted(name)

for x in range(0, 4169):
    if str(data.iloc[x, 0]).title() in name:
        Y = str(data.iloc[x, 0]).title()
        stateName.append(Y)

# putting total crimes of each state into a list
ITEM = 0
for ITEM in range(0, 4169):
    if str(data.iloc[ITEM, 0]).title() in name:
        Y = int(data.iloc[ITEM, 69])
        totalCrimes.append(Y)

df = pd.DataFrame(
    {"Crime": ['Assault Offenses', 'Aggravated Assault', 'Simple Assault', 'Intimidation',
               'Kidnapping/Abduction','Sex Offenses', 'Rape', 'Sodomy',
               'Burglary/Breaking & Entering', 'Robbery',
               'Drug/Narcotic Offenses','Motor Vehicle Theft',
               'Destruction/Damage/Vandalism of Property',
               'Fraud Offenses'],
     'Amount': [1251480, 250529, 766496, 234455, 18665, 81218, 32730, 7923, 324785, 78956, 636689,
                228987, 603898, 342109]})

# title, layout contains: html.div and dcc.graph
# children property is always the first attribute, you can omit it, same as
# html.H1(children='hello dash') and html.H1('hello dash'), it can contain: a string,
# number, single component, or list of components
app.layout = html.Div([html.Label('Crimes in the United States in 2019'),
                       dcc.Dropdown(id='myDropdown',
                                    options=[{'label': 'Crimes per State', 'value': 'trig'},
                                             {'label': 'Total for each crime', 'value': 'Crime'}],
                                    value='trig', style={"width": "50%"}, clearable=False),
                       dcc.Graph(id='crime-graph', style={'width': '180vh', 'height': '90vh'},)])

# call back
@app.callback(
    Output(component_id='crime-graph', component_property='figure'),
    [Input(component_id='myDropdown', component_property='value')])

def graph_type(myDropdown):
    """creates the bar and map graphs depending on dropdown value crime or trig"""
    if myDropdown == 'Crime':
        blop = px.bar(df, x=myDropdown, y='Amount', color='Crime')
        return blop

    trig = px.choropleth(data, geojson=stateFile, locations=stateName,
                         featureidkey='properties.NAME',
                         color=totalCrimes, color_continuous_scale="viridis",
                         range_color=(0, 900000),
                         scope='usa', labels={'State Total': 'Total Crimes Committed'})

    trig.update_layout(title='Total Crimes per State 2019',
                       geo={"scope":'usa', "projection": {"type": 'albers usa'},
                                "showlakes": True, "lakecolor": 'rgb(204, 224, 255)'},
                       coloraxis_colorbar_title_text="Amount of Crimes")

    return trig

if __name__ == '__main__':
    # this lets us have auto refresh to the graph when data is changed
    app.run_server(debug=True)
