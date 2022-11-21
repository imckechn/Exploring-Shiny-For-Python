from dash import Dash, dcc, html, Input, Output
import plotly.express as px
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd

def importData(year):
    df = pd.read_csv('http://gbadske.org:9000/GBADsLivestockPopulation/faostat?year=' + str(year) + '&country=Canada&species=*&format=file')
    print(df.keys)
    return df

yearSelected = 2017
#df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/gapminderDataFiveYear.csv')
#df.to_csv('raw_data.csv', index=False)
df = importData(yearSelected)

app = Dash(__name__)

app.layout = html.Div([
    html.H3("Animal Populations in Canada"),
    #dcc.Graph(id="A histogram"),
    dcc.Slider(
        2010,   #Min
        2020,   #Max
        1,      #Step
        marks={i: '{}'.format(i) for i in range(2010,2021,1)}, #Marks range
        value=2017, #Default
        id="year-slider" #ID
    ),
    #dcc.Slider(
    #    2010,
    #    2018,
    #    step =  1,
    #    value = yearSelected,
    #    marks={2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018},
    #    id='year-slider'
    #)
    dcc.Graph(id='graph-with-slider'),
    #dcc.Slider(
    #    2010,
    #    2018,
    #    step=1,
    #    value=yearSelected,
    #    marks={2010, 2011, 2012, 2013, 2014, 2015, 2016, 2017, 2018},
    #    id='year-slider'
    #)
])

@app.callback(
    Output('graph-with-slider', 'figure'),
    Input('year-slider', 'value'))
def update_figure(selected_year):
    df = importData(selected_year)

    fig = px.bar(df, x="species", y="population", color="species", barmode="group")

    #fig = px.scatter(filtered_df, x="country", y="species",
                     #size="population", color="species", hover_name="species",
                     #log_x=True, size_max=55)

    #fig.update_layout(transition_duration=500)

    return fig


if __name__ == '__main__':
    app.run_server(debug=True)