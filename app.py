from werkzeug.serving import run_simple, run_with_reloader
from car_prediction import application, db


if __name__ == "__main__":
   application.run(debug = True)



