from flask import Blueprint, render_template
from flask_login import login_required
dash_blue_print = Blueprint('dashapps', __name__, template_folder='templates')

@dash_blue_print.route("/app2/")
@login_required
def dash_app_2():
    return render_template('dash_app.html', dash_url='/dash/app2/')

@dash_blue_print.route("/app1/")
@login_required
def dash_app_1():
    return render_template('dash_app.html', dash_url='/dash/app1/')