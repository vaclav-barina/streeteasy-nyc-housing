import pandas as pd
import dash
from dash import dcc
from dash import html
from dash.dependencies import Input, Output
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Load the dataset
df = pd.read_csv(r"C:\Users\Vaclav Barina\Documents\3. Study\2. Data Science\1. Fun Projects\2023_Streeteasy Housing Data\Cleaned Data\Melted\Melted Master\merged_data.csv")

# Define the list of valid filter columns
valid_filters = ['Days on Market', 'Median Asking Price', 'Median Sales Price', 'Price Cut Share', 'Recorded Sales Volume', 'Sale List Ratio', 'Total Inventory All']

# Get the unique values for Area Name and Borough
area_names = df['Area Name'].unique()
boroughs = df['Borough'].unique()

# Create the Dash app
app = dash.Dash(__name__, external_stylesheets=['https://bootswatch.com/4/slate/bootstrap.min.css'])

# Define the layout
app.layout = html.Div(style={'backgroundColor': '#303030', 'padding': '30px'}, children=[
    html.H1('NYC Housing Data'),
    dcc.Dropdown(
        id='area-dropdown',
        options=[{'label': i, 'value': i} for i in area_names],
        value=area_names[0]
    ),
    dcc.Dropdown(
        id='filter-dropdown',
        options=[{'label': i, 'value': i} for i in valid_filters],
        value=valid_filters[0],
        clearable=False
    ),
    dcc.Graph(
        id='line-chart',
        style={'backgroundColor': '#404040', 'padding': '10px', 'borderRadius': '10px'}
    )
])

# Define the callback
@app.callback(
    Output('line-chart', 'figure'),
    [Input('area-dropdown', 'value'),
     Input('filter-dropdown', 'value')]
)
def update_line_chart(selected_area, selected_filters):
    # Apply filtering by selected area
    filtered_df = df[df['Area Name'] == selected_area] 
    columns_to_display = ['date'] + [selected_filters] if isinstance(selected_filters, str) else ['date'] + selected_filters
    filtered_df = filtered_df[columns_to_display]
    
    # Melt the DataFrame to create a long format
    melted_df = pd.melt(filtered_df, id_vars=['date'], value_vars=selected_filters, var_name='Filter')
    
    # Create the line chart
    fig = px.line(melted_df, x='date', y='value', color='Filter')
    fig.update_xaxes(title_text="Date", tickangle = -45, tickmode='array', tickvals=filtered_df['date'][::6], showgrid=False, title_font=dict(size=30), title_standoff=50)
    fig.update_yaxes(title_text= selected_filters, showgrid=False, title_font=dict(size=30), title_standoff=50)
    fig.update_layout(annotations=[dict(x=-0.05, y=-0.19, showarrow=False, text='Source: StreetEasy', font=dict(size=16), xref='paper', yref='paper', yanchor='bottom')],
                      margin=dict(t=0, r=0, b=25, l=0), # Add margin to bottom of plot area
                      height=700) # Increase height to fit annotation
    
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
