import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc

# Load the data
df_merge = pd.read_csv('all_data.csv')
df_merge['order_approved_at'] = pd.to_datetime(df_merge['order_approved_at'])

# Initialize the Dash app
app = Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Define the layout
app.layout = dbc.Container([
    html.H1("Olist E-commerce Dashboard", className="text-center mt-4 mb-4"),
    
    dbc.Row([
        dbc.Col([
            html.H3("Total Sales by State (2018)", className="text-center"),
            dcc.Graph(id='sales-by-state')
        ], width=6),
        dbc.Col([
            html.H3("Monthly Sales Trend (2017)", className="text-center"),
            dcc.Graph(id='monthly-sales-trend')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Payment Type Distribution", className="text-center"),
            dcc.Graph(id='payment-type-dist')
        ], width=6),
        dbc.Col([
            html.H3("Delivery Time vs Total Orders", className="text-center"),
            dcc.Graph(id='delivery-time-orders')
        ], width=6)
    ]),
    
    dbc.Row([
        dbc.Col([
            html.H3("Average Payment Value Over Time", className="text-center"),
            dcc.Graph(id='avg-payment-over-time')
        ], width=12)
    ])
], fluid=True)

# Callback for Sales by State
@app.callback(
    Output('sales-by-state', 'figure'),
    Input('sales-by-state', 'id')
)
def update_sales_by_state(id):
    df_2018 = df_merge[df_merge['order_approved_at'].dt.year == 2018]
    df_state = df_2018.groupby('customer_state')['payment_value'].sum().sort_values(ascending=True)
    
    fig = px.bar(df_state, x=df_state.values, y=df_state.index, orientation='h',
                 color=df_state.values, color_continuous_scale='Viridis')
    fig.update_layout(xaxis_title="Total Sales", yaxis_title="State")
    return fig

# Callback for Monthly Sales Trend
@app.callback(
    Output('monthly-sales-trend', 'figure'),
    Input('monthly-sales-trend', 'id')
)
def update_monthly_sales_trend(id):
    df_2017 = df_merge[df_merge['order_approved_at'].dt.year == 2017]
    df_monthly = df_2017.resample('M', on='order_approved_at').size()
    
    fig = px.line(x=df_monthly.index, y=df_monthly.values, markers=True)
    fig.update_layout(xaxis_title="Date", yaxis_title="Number of Orders")
    return fig

# Callback for Payment Type Distribution
@app.callback(
    Output('payment-type-dist', 'figure'),
    Input('payment-type-dist', 'id')
)
def update_payment_type_dist(id):
    payment_type_counts = df_merge['payment_type'].value_counts()
    fig = px.pie(values=payment_type_counts.values, names=payment_type_counts.index, hole=0.3)
    return fig

# Callback for Delivery Time vs Total Orders
@app.callback(
    Output('delivery-time-orders', 'figure'),
    Input('delivery-time-orders', 'id')
)
def update_delivery_time_orders(id):
    delivery_time_orders = df_merge.groupby('customer_state').agg(
        avg_delivery_time=('lama_pengiriman', 'mean'),
        total_orders=('customer_state', 'count')
    ).reset_index()
    
    fig = px.scatter(delivery_time_orders, x='avg_delivery_time', y='total_orders',
                     color='customer_state', size='total_orders',
                     hover_data=['customer_state'])
    fig.update_layout(xaxis_title="Average Delivery Time (days)", yaxis_title="Total Orders")
    return fig

# Callback for Average Payment Value Over Time
@app.callback(
    Output('avg-payment-over-time', 'figure'),
    Input('avg-payment-over-time', 'id')
)
def update_avg_payment_over_time(id):
    df_merge['year_month'] = df_merge['order_approved_at'].dt.to_period('M')
    monthly_payment = df_merge.groupby('year_month')['payment_value'].mean().reset_index()
    monthly_payment['year_month'] = monthly_payment['year_month'].astype(str)
    
    fig = px.bar(monthly_payment, x='year_month', y='payment_value',
                 color='payment_value', color_continuous_scale='Viridis')
    fig.update_layout(xaxis_title="Year-Month", yaxis_title="Average Payment Value",
                      xaxis_tickangle=-45)
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
