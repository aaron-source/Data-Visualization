# %%
import pandas as pd
import dash 
import dash_html_components as html
import dash_core_components as components

import plotly.express as express
import dash_core_components as core
data = pd.read_csv("Gender.csv", encoding="ISO-8859-1")
"""
Countries:
    - 44 countries
    - 60 examples for each country
UNICEF Regions are
    - Eastern and Southern Africa
    - West and Central Africa
Gender:
    - same number of samples between both males and females
Ages:
    between the ages of 10-19 only
Estimated incidence rate of new HIV infection per 1000 uninfected population

"""
def hiv_per_1000(dataframe):
    newInfections = dataframe.groupby(["Year", "Sex"])["Estimated incidence rate of new HIV infection per 1 000 uninfected population "].mean()
    incident_rate = [(i, newInfections.loc[i]["Male"], newInfections.loc[i]["Female"]) for i in range(1990, 2020)]
    Frame = pd.DataFrame(incident_rate, columns=["Year", "Male", "Female"])
    return Frame

def living_with_hiv(dataframe):
    Total_number = dataframe.groupby(["Year", "Sex"])["Estimated number of people living with HIV"].sum()
    lw_hiv = [(j, Total_number.loc[j]["Male"], Total_number.loc[j]["Female"]) for j in range(1990, 2020)]
    Frame = pd.DataFrame(lw_hiv, columns=["Year", "Male", "Female"])
    return Frame

def new_infections(dataframe):
    infections = data.groupby(["Country", "Sex"])["Estimated number of annual new HIV infections"].mean()
    estimated = [(country, infections[country]["Male"], infections[country]["Female"]) for country in dataframe["Country"].unique()]
    Frame = pd.DataFrame(estimated, columns=["Country", "Male", "Female"])
    return Frame

def aids_related_deaths(dataframe):
    data_temp = dataframe.groupby(["Country", "Sex"])["Estimated number of annual AIDS related deaths"].mean()
    results = [(country, data_temp[country]["Female"], data_temp[country]["Male"]) for country in dataframe["Country"].unique()]
    Frame = pd.DataFrame(results, columns=["Country", "Female", "Male"])
    Frame = Frame.dropna()
    Frame = Frame.reset_index(drop=True)
    Frame = Frame.sort_values(["Male", "Female"], ascending=False)
    return Frame

def aids_related_deaths_per100000(dataframe):
    rate = dataframe.groupby(["Year", "Sex"])["Estimated rate of annual AIDS related deaths  per 100 000 population "].mean()
    per_100000 = [(i, rate.loc[i]["Female"], rate.loc[i]["Male"]) for i in range(1990, 2020)]
    Frame = pd.DataFrame(per_100000, columns=["Year", "Female", "Male"])
    return Frame

per_1000 = hiv_per_1000(data)
livingWhiv = living_with_hiv(data)
newly_infected = new_infections(data)
related_deaths = aids_related_deaths(data)
per_100000 = aids_related_deaths_per100000(data)
style = ['https://codepen.io/chriddp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=style)

@app.callback(dash.dependencies.Output('show-by-gender', 'children'), [dash.dependencies.Input('menu', 'value')])
def show_Africa(value):
    chart_africa = express.choropleth(newly_infected, locationmode="country names", locations=newly_infected["Country"], color=value, hover_name="Country", color_continuous_scale=express.colors.sequential.Plasma, scope="africa", width=1000, height=1000)
    return components.Graph(id="Chart_Of_Africa", figure=chart_africa)


linegraph = express.line(per_1000, x="Year", y=["Female", "Male"], width=1000, height=500)
barchart = express.bar(livingWhiv, x="Year", y=["Female", "Male"], width=1300, height=500, barmode='group')
horizontalBar = express.bar(related_deaths, y="Country", x=["Male", "Female"], orientation='h', width=700, height=700, barmode='group')
scatterPlot = express.scatter(per_100000, x="Year", y=["Female", "Male"], width=1000, height=500)
app.layout = html.Div([
    html.H1("Gender Inequality in HIV/AIDs Infections Among Adolscents", style={'textAlign': 'center'}),
    html.Div([
        html.P("Thank you for visiting my dashboard on visualizing gender inequality among countries in Africa"),
        html.P("First I would  like to thank data world for providing this dataset, it is well structured and easy to understand"),
        html.P("To find this dataset you can visit https://data.world/makeovermonday/")
    ], style={"textAlign": "center"}),
    html.Div([
        components.Graph(
            id='Line_Chart',
            figure=linegraph,
        ),
    ], style={"height": "40px"}),
    html.Div([
        components.Graph(
            id="Scatter",
            figure=scatterPlot
        )
    ], style={"marginTop": "400px"}),
    html.Div([
        components.Dropdown(id='menu', options=[{'label': Gender, 'value': Gender} for Gender in ["Female", "Male"]], value="Female", style={"width": "100px", "marginLeft": "50px", "marginBottom": "0px"}),
        html.Div(id="show-by-gender")
    ], style={'marginLeft': '1000px', 'marginTop': '-900px'}),
    html.Div([
        components.Graph(id='Bar_Chart', figure=barchart)
    ], style={"marginLeft": '600px', 'height': '700px'}),
    html.Div([
        components.Graph(
            id='h_bar_chart',
            figure=horizontalBar
        )
    ], style={"marginTop": '-950px', "marginTop": "-900px"})

])

if __name__ == '__main__':
    app.run_server(debug=True)




