from chalice import Chalice
from chalicelib.sugar_bliss_backend import calculate
from pdb import set_trace


app = Chalice(app_name='sugar-bliss-backend')
app.debug = True


@app.route('/', methods=('GET',), cors=True)
def ping():
    return 'pong'


@app.route('/submit', methods=('POST',), cors=True)
def submit():
    json_obj = app.current_request.json_body
    errors = calculate.validate(json_obj)

    if errors:
        return {
            'status': 'fail',
            'errors': errors
        }

    preprocessed = calculate.preprocess(json_obj)
    food_obj, time_obj = calculate.split_data(preprocessed)
    res = calculate.calculate(food_obj, time_obj)

    return res
