import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import pandas as pd
import plotly.express as px

# Load the dataset
df = pd.read_csv('superstore.csv')

# Convert 'Order.Date' to a datetime object to work with years
df['Order.Date'] = pd.to_datetime(df['Order.Date'])

# Print columns for debugging purposes (optional)
print(df.columns)

# Initialize the Dash app
app = dash.Dash(__name__)

# Create different graphs
fig_bar = px.bar(df, x='Category', y='Sales', title='Sales by Category')
fig_pie = px.pie(df, names='Region', values='Sales', title='Sales by Region')
fig_scatter = px.scatter(df, x='Sales', y='Profit', color='Category', title='Sales vs Profit')

# Define the layout of the app
app.layout = html.Div(children=[
    html.H1(children='Superstore Sales Dashboard'),

    # Dropdown for selecting the graph
    dcc.Dropdown(
        id='graph-selector',
        options=[
            {'label': 'Bar Chart: Sales by Category', 'value': 'bar'},
            {'label': 'Pie Chart: Sales by Region', 'value': 'pie'},
            {'label': 'Scatter Plot: Sales vs Profit', 'value': 'scatter'}
        ],
        value='bar',  # Default graph
        clearable=False
    ),

    # Graph that will change based on the dropdown selection
    dcc.Graph(id='main-graph'),

    # Slider for filtering by order year
    html.Label('Select Order Year:'),
    dcc.Slider(
        id='year-slider',
        min=df['Order.Date'].dt.year.min(),
        max=df['Order.Date'].dt.year.max(),
        step=1,
        value=df['Order.Date'].dt.year.min(),  # Default value
        marks={str(year): str(year) for year in range(df['Order.Date'].dt.year.min(), df['Order.Date'].dt.year.max() + 1)},
    ),

    # Checkbox to filter by ship mode
    html.Label('Ship Mode:'),
    dcc.Checklist(
        id='ship-mode-selector',
        options=[{'label': mode, 'value': mode} for mode in df['Ship.Mode'].unique()],
        value=df['Ship.Mode'].unique(),
        inline=True
    )
])

# Define callback to update the graph based on interactions
@app.callback(
    Output('main-graph', 'figure'),
    [Input('graph-selector', 'value'),
     Input('year-slider', 'value'),
     Input('ship-mode-selector', 'value')]
)
def update_graph(selected_graph, selected_year, selected_modes):
    # Filter data based on selected year and ship modes
    filtered_df = df[(df['Order.Date'].dt.year == selected_year) & (df['Ship.Mode'].isin(selected_modes))]

    # Return the selected graph
    if selected_graph == 'bar':
        fig = px.bar(filtered_df, x='Category', y='Sales', title='Sales by Category')
    elif selected_graph == 'pie':
        fig = px.pie(filtered_df, names='Region', values='Sales', title='Sales by Region')
    elif selected_graph == 'scatter':
        fig = px.scatter(filtered_df, x='Sales', y='Profit', color='Category', title='Sales vs Profit')
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
