

import joblib
from car_prediction.plotly_dash_apps.utils import row1, row2, row3, row4
from car_prediction.plotly_dash_apps.utils2 import row5, navbar
import pandas as pd
from dash import Dash, html, Input, Output, State
import dash_bootstrap_components as dbc
import dash_daq as daq
from car_prediction.plotly_dash_apps import _protect_dash_view
from car_prediction.plotly_dash_apps import df
#df = pd.read_csv('car_price_data.csv').drop('Unnamed: 0', axis=1)
loaded_model = joblib.load('car_prediction/plotly_dash_apps/dashboard_utils/final_car_prediction_model.pkl')


def create_app_one(server):

    app = Dash(__name__, external_stylesheets=[
               dbc.themes.SUPERHERO], url_base_pathname="/dash/app1/", suppress_callback_exceptions=True, server=server)

    app.layout = html.Div([
        navbar,
        html.Div([row1,
                  # html.Hr(),
                  row2,
                  #   html.Hr(),
                  row3,
                  #   html.Hr(),
                  row4,

                  ], className='container', style={'padding-top': '25px', 'padding-bottom': '25px'}),

        #html.Button(id='submit-button-state', n_clicks=0, children='Submit'),


        html.Div([
            html.Div([
                row5,
                html.Div(id='model-dropdown-output',
                         style={'font-size': '30px'}),
                html.Div(id='prediction', style={'font-size': '60px'}),
                dbc.Button("Submit", className="me-1",
                           id='submit-button-state', color="dark",),
            ],
                className="container"
            ),
        ])

    ])

    @app.callback(
        Output('prediction', 'children'),

        Input('submit-button-state', 'n_clicks'),
        State('km-travelled-slider', 'value'),
        State('year-picker', 'value'),
        State('engine-size-slider', 'value'),
        State('tax-slider', 'value'),
        State('km-per-liters-slider', 'value'),
        State('model-dropdown', 'value'),
        State('transmission-dropdown', 'value'),
        State('fuel-type-dropdown', 'value')
    )
    def update_output(n_clicks, km_travelled, date_value, engine_size, tax_value, km_per_liters, model_name, transmission, fuel_type):
        prediction = loaded_model.predict(pd.DataFrame(
            data=[[str(date_value), km_travelled, tax_value, engine_size,
                km_per_liters, model_name, transmission, fuel_type]],
            columns=joblib.load('car_prediction/plotly_dash_apps/dashboard_utils/column_names.pkl')))

        return (


            f"Car Price: {round(prediction[0])}"
        )


    @app.callback(Output('km-travelled-gauge', 'value'), Input('km-travelled-slider', 'value'))
    def km_travelled_update(km_travelled):
        return km_travelled


    @app.callback(Output('km-per-liters-slider-output', 'value'), Input('km-per-liters-slider', 'value'))
    def km_travelled_update(km_per_lit):
        return km_per_lit


    @app.callback(Output('engine-size-slider-output', 'value'), Input('engine-size-slider', 'value'))
    def km_travelled_update(engine_slider):
        return engine_slider


    def return_card_content(header, value_to_update, info=None):
        card_content = [
            dbc.CardHeader(header, style={'font-size':'x-large'}),
            dbc.CardBody(
                [
                    html.H5(str(value_to_update), className="card-title"),
                    html.P(
                        info,
                        className="card-text",
                    ),
                ]
            ),
        ]
        return card_content


    @app.callback(Output('tax-slider-output', 'children'), Input('tax-slider', 'value'),)
    def year_update(tax_value):
        card_content = return_card_content("Tax", tax_value, "Tax Value")
        return card_content
        


    @app.callback(Output('year-picker-output', 'children'), Input('year-picker', 'value'),)
    def tax_update(year):
        card_content = return_card_content("Year", year, "Model Year")
        return card_content


    @app.callback(Output('fuel-type-dropdown-output', 'children'), Input('fuel-type-dropdown', 'value'),)
    def fuel_update(fuel_type):
        card_content = return_card_content("Fuel Type", fuel_type, "Type Of Fuel")
        return card_content


    @app.callback(Output('transmission-dropdown-output', 'children'), Input('transmission-dropdown', 'value'),)
    def transmisssion_update(transmission_type):
        card_content = return_card_content(
            "Transmission Type", transmission_type, "Type Of Transmission")
        return card_content


    @app.callback(Output('model-dropdown-output', 'children'), Input('model-dropdown', 'value'),)
    def transmisssion_update(model_name):
        return f"Selected Model: {model_name}",

    _protect_dash_view(app)

    return app.server
