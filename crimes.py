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

# new data set
new_datas=data.groupby(['State','State Total']).sum().reset_index()

new_datas=new_datas.drop([6])
#print(new_datas)

# new_datas.shape
# new_datas = new_datas.loc[new_datas['State'] == 'Federal']
# new_datas.shape
#new_datas.drop(labels=['Federal'], axis=0, inplace=True)
#new_datas.to_csv('newest_data.csv')

stateFile = json.load(open('gz_2010_us_040_00_20m.json', 'r'))
states = stateFile['features']

# take state name
name, location, totalCrimes, stateName = [], [], [], []

# adding all states in name[]
for x in states:
    names = x['properties']['NAME']
    stateNumber = x['properties']['STATE']
    # stateNum.append(stateNumber)
    name.append(names)
    # getting state locations
    loc = x['geometry']['coordinates'][0]
    location.append(loc)
name = sorted(name)

for x in range(0, 4169):
    if str(data.iloc[x, 0]).title() in name:
        y = str(data.iloc[x, 0]).title()
        stateName.append(y)

# putting total crimes of each state into a list
item = 0
for item in range(0, 4169):
    if str(data.iloc[item, 0]).title() in name:
        y = int(data.iloc[item, 69])
        totalCrimes.append(y)


# mapping/visual
new_datas=new_datas.to_string(index=False)
#print(new_datas('State'))
cityName, offenses=[], []
cities=json.load(open('usaCities.json', 'r'))
count=0
for x in cities:
    o=str(cities[count]['city'] +' '+ cities[count]['state'])
    cityName.append(o)
    count=count+1

for y in data['Total Offenses']:
    offenses.append(y)
print(offenses)
count=0
for x in cities:
    if cities[count]['city'] not in data['Agency Name']:
        print((cities[count]['city']))
    count=count+1
# check length matching


#print(cities[0]['state'])
# flip=px.choropleth(data, geojson=cities, locations=cityName, featureidkey='state',
#                    color=offenses, color_continuous_scale='ylorrd',
#                    range_color=(0,100000), scope='usa')
# flip.update_layout(title='Total Crimes per City in 2019', geo=dict(scope='usa', projection=dict(type='albers usa'),
#                     showlakes=True, lakecolor='rgb(204, 224, 255)'))
# flip.show()
# print(stateName)

# trig = px.choropleth(new_datas, geojson=stateFile, locations=str('State').title(), featureidkey='properties.NAME',
#                      color='State Total',
#                      color_continuous_scale="ylorrd", range_color=(0,900000),
#                      scope='usa', labels={'State Total': 'Total Crimes Committed'})
#
# trig.update_layout(title='Total Crimes Committed per State 2019', geo=dict(scope='usa', projection=dict(type='albers usa'),
#                     showlakes=True, lakecolor='rgb(204, 224, 255)'))
#
# trig.show()
