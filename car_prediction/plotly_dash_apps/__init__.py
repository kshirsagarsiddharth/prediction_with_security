from flask_login import login_required

def _protect_dash_view(dashapp):
    for view_function in dashapp.server.view_functions:
       
        if view_function.startswith(dashapp.config.url_base_pathname):
            dashapp.server.view_functions[view_function] = login_required(dashapp.server.view_functions[view_function])

import pandas as pd 
df = pd.read_csv('car_prediction/plotly_dash_apps/dashboard_utils/car_price_data.csv').drop('Unnamed: 0', axis=1)
            