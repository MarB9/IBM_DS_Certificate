# Import required libraries
import pandas as pd
import dash
import dash_html_components as html
import dash_core_components as dcc
from dash.dependencies import Input, Output
import plotly.express as px

# Read the airline data into pandas dataframe
spacex_df = pd.read_csv("spacex_launch_dash.csv")
max_payload = spacex_df['Payload Mass (kg)'].max()
min_payload = spacex_df['Payload Mass (kg)'].min()

# Create a dash application
app = dash.Dash(__name__)

# Create an app layout
app.layout = html.Div(children=[html.H1('SpaceX Launch Records Dashboard',
                                        style={'textAlign': 'center', 'color': '#503D36',
                                               'font-size': 40}),
                                # TASK 1: Add a dropdown list to enable Launch Site selection
                                # The default select value is for ALL sites
                                dcc.Dropdown(
                                    id='site-dropdown',
                                    options=[
                                        {'label': 'All Sites', 'value': 'ALL'},
                                        {'label': spacex_df['Launch Site'].unique()[0], 'value': spacex_df['Launch Site'].unique()[0]},
                                        {'label': spacex_df['Launch Site'].unique()[1], 'value': spacex_df['Launch Site'].unique()[1]},
                                        {'label': spacex_df['Launch Site'].unique()[2], 'value': spacex_df['Launch Site'].unique()[2]},
                                        {'label': spacex_df['Launch Site'].unique()[3], 'value': spacex_df['Launch Site'].unique()[3]},
                                        ],
                                    value='ALL',
                                    placeholder='Select a Launch Site here',
                                    searchable=True
                                             ),
                                html.Br(),

                                # TASK 2: Add a pie chart to show the total successful launches count for all sites
                                # If a specific launch site was selected, show the Success vs. Failed counts for the site
                                html.Div(dcc.Graph(id='success-pie-chart')),
                                html.Br(),

                                html.P("Payload range (Kg):"),
                                # TASK 3: Add a slider to select payload range
                                dcc.RangeSlider(id='payload-slider',
                                                min=0, max=10000, step=1000,
                                                marks={0: '0', 2500: '2500', 5000 : '5000', 7500 : '7500', 10000 : '10000'},
                                                value=[min_payload, max_payload]),

                                # TASK 4: Add a scatter chart to show the correlation between payload and launch success
                                html.Div(dcc.Graph(id='success-payload-scatter-chart')),
                                ])

# TASK 2:
# Add a callback function for `site-dropdown` as input, `success-pie-chart` as output
# Function decorator to specify function input and output
@app.callback(Output(component_id='success-pie-chart', component_property='figure'),
              Input(component_id='site-dropdown', component_property='value'))

def get_pie_chart(entered_site):
    filtered_df = spacex_df

    if entered_site == 'ALL':
        fig = px.pie(filtered_df, values='class', 
        names='Launch Site', 
        title='Total Success Launches By Site')
        return fig
    else:
        # return the outcomes piechart for a selected site
        filtered_df=filtered_df.groupby('Launch Site')['class'].value_counts().reset_index()
        data=filtered_df[filtered_df['Launch Site']==entered_site]
        fig = px.pie(data, values='count', names='class', title='Total Success Launches for {}'.format(entered_site))
        return fig

# TASK 4:
# Add a callback function for `site-dropdown` and `payload-slider` as inputs, `success-payload-scatter-chart` as output
@app.callback(Output(component_id='success-payload-scatter-chart', component_property='figure'),
              [Input(component_id='site-dropdown', component_property='value'),Input(component_id='payload-slider',component_property='value')])

def get_scatter_chart(entered_site,value):
    
    filtered_df2 = spacex_df
    filtered_df2=filtered_df2[(filtered_df2['Payload Mass (kg)']>= value[0])&(filtered_df2['Payload Mass (kg)']<= value[1])]

    if entered_site == 'ALL':
        fig = px.scatter(filtered_df2,x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Correlation between Payload and Success for all Sites')
        #fig.update_xaxes(range=[value[0]-250, value[1]+250])
        return fig
    else:
        filtered_df2=filtered_df2[filtered_df2['Launch Site']==entered_site]
        fig = px.scatter(filtered_df2, x='Payload Mass (kg)', y='class',
        color='Booster Version Category',
        title='Total Success Launches for {}'.format(entered_site))
        #fig.update_xaxes(range=[value[0]-250, value[1]+250])
        return fig

# Run the app
if __name__ == '__main__':
    app.run_server()