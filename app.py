import dataclasses
import json
from typing import Dict, List

from chalice import Chalice

from chalicelib.sugar_bliss_backend import app_types, calculate, constants

app = Chalice(app_name='sugar-bliss-backend')
app.debug = True


@app.route('/data', methods=('GET', ), cors=True)
def data():
    return constants.DATA


@app.route('/submit', methods=('POST', ), cors=True)
def submit():
    json_obj: Dict[str, str] = app.current_request.json_body
    errors: List[str] = calculate.validate(json_obj)

    if errors:
        return {
            'status': 'fail',
            'errors': errors,
        }

    calculation_input: app_types.CalculationInput = calculate.preprocess(
        json_obj)

    try:
        calculation = calculate.calculate(calculation_input)
    except app_types.CalculationException as e:
        return {'status': 'fail', 'errors': [str(e)]}

    as_object = calculate.to_json(calculation)

    return as_object
