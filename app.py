import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
import dash.html as html
import dash.dcc as dcc
from dash.dependencies import Input, Output
from utils import get_data


external_stylesheets = [
    {
        'rel': "stylesheet",
        'href': "https://cdnjs.cloudflare.com/ajax/libs/bootstrap/5.0.1/css/bootstrap.min.css",
        'integrity': "sha512-Ez0cGzNzHR1tYAv56860NLspgUGuQw16GiOOp/I2LuTmpSK9xDXlgJz3XN4cnpXWDmkNBKXR/VDMTCnAaEooxA==",
        'crossorigin': "anonymous",
        'referrerpolicy': "no-referrer"
    }
]


patients, total, active, recovered, deaths = get_data()
options = [
    'All'
]
options.extend(
    [status for status in patients['current_status'].unique() if pd.notna(status)])


app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
app.layout = html.Div(
    [
        html.H1("Corona Virus Data Analysis",
                className='text-center'),
        html.Div([
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(
                            "Total Cases", className='text-center text-light'),
                        html.H3(
                            total, className='text-center text-light')
                    ], className='card-body')
                ], className='card bg-danger')
            ], className='col-md-3'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(
                            "Active Cases", className='text-center text-light'),
                        html.H3(
                            active, className='text-center text-light')
                    ], className='card-body')
                ], className='card bg-info')
            ], className='col-md-3'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(
                            "Recovered Cases", className='text-center text-light'),
                        html.H3(
                            recovered, className='text-center text-light')
                    ], className='card-body')
                ], className='card bg-warning')
            ], className='col-md-3'),
            html.Div([
                html.Div([
                    html.Div([
                        html.H5(
                            "Deaths Cases", className='text-center text-light'),
                        html.H3(
                            deaths, className='text-center text-light')
                    ], className='card-body')
                ], className='card bg-success')
            ], className='col-md-3'),
        ], className='row'),
        html.Div([], className='row'),
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All',),
                    dcc.Graph(id='bar', config={
                              'displayModeBar': True}, className='mt-2')
                ], className='card-body')
            ], className='col-md-12')
        ], className='row'),
        html.Div([], className='row'),
        html.Div([], className='row'),
    ], className='container')


@app.callback(Output('bar', 'figure'),
              Input('picker', 'value'))
def update_graph(value):
    if value == 'All':
        p_bar = patients['detected_district'].value_counts(
        ).reset_index().reset_index()
    else:
        n_pat = patients[patients['current_status'] == value]
        p_bar = n_pat['detected_district'].value_counts(
        ).reset_index().reset_index()
    return {
        'data': [
            go.Bar(
                x=p_bar['index'],
                y=p_bar['detected_district'],
                text=p_bar['detected_district'],
                textposition='auto',
                marker_color='#FF5733'
            )
        ],
        'layout': go.Layout(
            title=f"Patients by {value}",
            xaxis_title="Districts",
            yaxis_title="Number of Patients",
            template="plotly_dark"
        )
    }


if __name__ == '__main__':
    app.run(debug=True)
