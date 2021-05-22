# data from crimes in the u.s. in 2019 from all states and cities, along with the types of crimes committed

# take in data .xls file, put it into a dictionary to organize it into each state
# then extract information w/ for loop, just to make sure all data is in the correct category
# use plotly to make a visual bar graph x for each state and y for total crimes committed in those states
# plan is to have multiple bar graphs to display different data on crimes
#   -total crimes for each state in 2019, see who had the most
#   -see which crime was committed the most overall in the country, show overall amount for each type, x type of crime and y number of times committed
#   -find what city has the most crime
#   -include federal agencies, army, navy, and marines

import pandas
import json
import plotly.express as px


data = pandas.read_csv('United_States_Offense_Type_by_Agency_2019.csv',
                       dtype={'State': str, 'Agency Type': str, 'Population': str, 'Total Offenses': str,
                              'Crimes Against Persons': str, 'Crimes Against Property': str,
                              'Crimes Against Society': str,
                              'Assault Offenses': str, 'Aggravated Assault': str, 'Simple Assault': str,
                              'Intimidation': str, 'Sex Offenses': str, 'Burglary/Breaking & Entering': str,
                              'Counterfeiting/Forgery': str,
                              'Destruction/Damage/Vandalism of Property': str, 'Fraud Offenses': str,
                              'False Pretenses/Swindle/Confidence Game': str,
                              'Credit Card/Automated Teller Machine Fraud': str,
                              'Impersonation': str, 'Identity Theft': str, 'Larceny/Theft Offenses': str,
                              'Shoplifting': str, 'Theft From Building': str, 'Theft From Motor Vehicle': str,
                              'Theft of Motor Vehicle Parts or Accessories': str, 'All Other Larceny': str,
                              'Motor Vehicle Theft': str, 'Robbery': str, 'Stolen Property Offenses': str,
                              'Drug/Narcotic Offenses': str, 'Drug/Narcotic Violations': str,
                              'Drug Equipment Violations': str, 'Prostitution Offenses': str,
                              'Weapon Law Violations': str, 'State Total': int})

stateFile = json.load(open('gz_2010_us_040_00_20m.json', 'r'))
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

for x in range(0, 6583):
    if str(data.iloc[x, 0]).title() in name:
        y = str(data.iloc[x, 0]).title()
        stateName.append(y)

# putting total crimes of each state into a list
item = 0
for item in range(0, 6583):
    if str(data.iloc[item, 0]).title() in name:
        y = int(data.iloc[item, 69])
        totalCrimes.append(y)

# print(str(data['State'][0:6582]).title())
# print(stateFile['features'][0]['properties']['NAME'])

# mapping/visual

trig = px.choropleth(data, geojson=stateFile, locations=stateName, featureidkey='properties.NAME',
                     color=totalCrimes,
                     color_continuous_scale="ylorrd", range_color=(0,900000),
                     scope='usa', labels={'State Total': 'Total Crimes Committed'})

trig.update_layout(title='Total Crimes per State 2019', geo=dict(scope='usa', projection=dict(type='albers usa'),
                    showlakes=True, lakecolor='rgb(204, 224, 255)'))

trig.show()