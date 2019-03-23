from chalice import Chalice
from chalicelib.sugar_bliss_backend import calculate, constants

app = Chalice(app_name='sugar-bliss-backend')
app.debug = True


@app.route('/data', methods=('GET', ), cors=True)
def data():
    return constants.DATA


@app.route('/submit', methods=('POST', ), cors=True)
def submit():
    json_obj = app.current_request.json_body
    errors = calculate.validate(json_obj)

    if errors:
        return {'status': 'fail', 'errors': errors}

    preprocessed = calculate.preprocess(json_obj)
    food_obj, time_obj = calculate.split_data(preprocessed)
    res = calculate.calculate(food_obj, time_obj)

    return res
