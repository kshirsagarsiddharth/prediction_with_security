from dash import Dash, html

from car_prediction.plotly_dash_apps import _protect_dash_view 




def create_app_two(server):
    app2 = Dash(__name__,url_base_pathname="/dash/app2/", suppress_callback_exceptions=True, server=server)
    app2.layout = html.Div("Hello, Dash app 2!")
    _protect_dash_view(app2)

    return app2.server


