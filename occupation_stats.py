import dash
from dash import dcc, html
import plotly.express as px
from dash.dependencies import Input, Output
import dash_table
import dash_bootstrap_components as dbc
import pandas as pd

# Load and prepare the data
df_occupation = pd.read_csv('csvFile.csv')
df = pd.read_csv('OccupationStats.csv')
df['Employment'] = df['Employment'].str.replace(',', '').astype(int)
df['Mean Income'] = df['Mean Income'].str.replace(',', '').astype(int)
df['Median Income'] = df['Median Income'].str.replace(',', '').astype(int)
df['Automation Percent'] = df['Automation Percent'].str.replace('%', '').astype(float)
df['Augmentation Percent'] = df['Augmentation Percent'].str.replace('%', '').astype(float)
df['Productivity Increase'] = df['Productivity Increase'].str.replace('%', '').astype(float)

# Initialize the Dash app
app = dash.Dash(__name__,external_stylesheets=[dbc.themes.SANDSTONE] )

app.layout = html.Div(children=[
    html.Br(),
    html.H1(children='Occupation Statistics Visualization'),

    # Scatter Plots
    html.Div([
        html.Div([
            
            html.P("There is a positive correlation of approximately 0.41 between employment numbers and the Automation Percent. Conversely, there is a negative correlation of approximately -0.60 between employment numbers and the Augmentation Percent. This analysis suggests that occupations with higher employment numbers might be more susceptible to automation but less likely to see high levels of augmentation. This could imply that more populous occupations face a greater push towards automation, possibly due to the scale efficiencies it offers, while augmentation, which often involves enhancing human capabilities to work alongside technology, might be more prevalent in fields with lower employment numbers.", style={'width': '400px', 'padding-top': '90px'}),
            dcc.Graph(
                figure=px.scatter(df, x='Automation Percent', y='Augmentation Percent',
                                  size='Employment', color='Occupations',
                                  hover_name='Occupations', title='Automation vs. Augmentation by Employment',
                                  range_x=[0,100], range_y=[0,100]),
                style={'width': '800px'}
            ),
        ], style={'display': 'flex', 'justify-content': 'flex-start', 'align-items': 'flex-start', 'margin-bottom': '20px'}),

        html.Div([
            html.P("There is a positive correlation of approximately 0.35 between Median Income and the Automation Percent. There is a positive correlation of approximately 0.67 between Median Income and the Augmentation Percent. While there's a moderate positive relationship between median income and automation, indicating that higher-paying occupations might see somewhat more automation, the stronger positive correlation with augmentation percent suggests that these higher-income roles are more significantly associated with technologies that augment human work. This could imply that higher-paying occupations are more focused on leveraging AI and technology to enhance productivity and capabilities rather than purely automating tasks.", style={'width': '400px', 'padding-top': '90px'}),
            dcc.Graph(
                figure=px.scatter(df, x='Automation Percent', y='Augmentation Percent',
                                  size='Median Income', color='Occupations',
                                  hover_name='Occupations', title='Automation vs. Augmentation by Median Income',
                                  range_x=[0,100], range_y=[0,100]),
                style={'width': '800px'}
            ),
        ], style={'display': 'flex', 'justify-content': 'flex-start', 'align-items': 'flex-start', 'margin-bottom': '20px'}),

        html.Div([
            html.P("There is a strong positive correlation of approximately 0.92 between Median Income and Productivity Increase. Conversely, there is a negative correlation of approximately -0.34 between Employment and Productivity Increase. This analysis suggests a clear trend where higher income levels within occupations are strongly associated with greater increases in productivity, likely reflecting the impact of advanced technologies and automation. On the other hand, the inverse relationship between employment numbers and productivity increase may indicate that more populous occupations face challenges in achieving the same level of productivity gains as more specialized, higher-income roles.", style={'width': '400px', 'padding-top': '90px'}),
            dcc.Graph(
                figure=px.scatter(df, x='Employment', y='Median Income',
                                  size='Productivity Increase', color='Occupations',
                                  hover_name='Occupations', title='Employment vs. Median Income by Productivity Increase',
                                  range_x=[df['Employment'].min()-322000, df['Employment'].max()+200000], 
                                  range_y=[df['Median Income'].min()-15000, df['Median Income'].max()+20000]),
                style={'width': '800px'}
            ),
        ], style={'display': 'flex', 'justify-content': 'flex-start', 'align-items': 'flex-start', 'margin-bottom': '20px'}),
    ]),

    # Bar Charts
    html.Div(style={'display': 'flex', 'justify-content': 'flex-start', 'flex-wrap': 'wrap'}, children=[
        html.Div([
            dcc.Graph(
                id='automation-bar-chart',
                figure=px.bar(df, x='Occupations', y='Automation Percent',
                              title='Automation Percent per Occupation'),
                style={'width': '500px'}
            ),
        ], style={'width': '500px', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='augmentation-bar-chart',
                figure=px.bar(df, x='Occupations', y='Augmentation Percent',
                              title='Augmentation Percent per Occupation'),
                style={'width': '500px'}
            ),
        ], style={'width': '500px', 'display': 'inline-block'}),

        html.Div([
            dcc.Graph(
                id='productivity-increase-bar-chart',
                figure=px.bar(df, x='Occupations', y='Productivity Increase',
                              title='Productivity Increase per Occupation'),
                style={'width': '500px'}
            ),
        ], style={'width': '500px', 'display': 'inline-block'}),
    ]),

    html.Br(),

    html.H1("Occupational Task Analysis"),
    
    html.Label("Select Occupation:"),
    dcc.Dropdown(
        id='occupation-dropdown',
        options=[{'label': i, 'value': i} for i in df_occupation['Occupation'].unique()],
        value=None,  # No default value
        clearable=False
    ),
    html.Br(),
    html.Div(id='occupation-table'),
    html.Br(),
    html.Label("Select Task:"),
    dcc.Dropdown(
        id='task-dropdown',
        options=[],  # Options will be updated based on Occupation selection
        value=None,  # No default value
        clearable=False
    ),
    html.Br(),
    html.Div(id='task-details'),
    html.Br(),html.Br(),html.Br(),html.Br()
], style={'padding-left': '20px'})

# Callback to update Task dropdown and Occupation data table based on selected Occupation
@app.callback(
    [Output('task-dropdown', 'options'),
     Output('occupation-table', 'children')],
    [Input('occupation-dropdown', 'value')]
)
def update_task_dropdown_and_occupation_table(selected_occupation):
    filtered_df = df_occupation[df_occupation['Occupation'] == selected_occupation]
    tasks_options = [{'label': i, 'value': i} for i in filtered_df['Task'].unique()]
    
    occupation_table = dash_table.DataTable(
        columns=[{"name": i, "id": i} for i in ['Occupation', 'Task', 'Automation Percentage', 'Augmentation Percentage', 'Productivity Multiplier']],
        data=filtered_df.to_dict('records'),
        style_table={'overflowX': 'auto'},
        style_cell={'textAlign': 'left', 'whiteSpace': 'normal', 'height': 'auto'},
        page_size=10
    )
    
    return tasks_options, occupation_table

# Callback for updating the task details based on the selected task
@app.callback(
    Output('task-details', 'children'),
    [Input('task-dropdown', 'value')]
)
def update_task_details(selected_task):
    if selected_task:
        filtered_df = df_occupation[df_occupation['Task'] == selected_task].iloc[0]  # Assuming unique tasks for simplicity
        
        details = [
            html.P([html.Strong("Impact on Automation:"), f" {filtered_df['Impact on Automation']}"]),
            html.P([html.Strong("Automation Explanation:"), f" {filtered_df['Automation Explanation']}"]),
            html.P([html.Strong("Impact on Augmentation:"), f" {filtered_df['Impact on Augmentation']}"]),
            html.P([html.Strong("Augmentation Explanation:"), f" {filtered_df['Augmentation Explanation']}"]),
            html.P([html.Strong("Productivity Explanation:"), f" {filtered_df['Productivity Explanation']}"]),
            html.P([html.Strong("Product Example 1:"), f" {filtered_df['Product Example 1']}"]),
            html.P([html.Strong("Product Example 2:"), f" {filtered_df['Product Example 2']}"]),
            html.P([html.Strong("Product Example 3:"), f" {filtered_df['Product Example 3']}"]),
            html.P([html.Strong("Product Example 4:"), f" {filtered_df['Product Example 4']}"]),
            html.P([html.Strong("Case Study 1:"), f" {filtered_df['Case Study 1']}"]),
            html.P([html.Strong("Case Study 2:"), f" {filtered_df['Case Study 2']}"]),
            html.P([html.Strong("Conclusion:"), f" {filtered_df['Conclusion']}"])
        ]
        
        return details

if __name__ == '__main__':
    app.run_server(debug=True)
