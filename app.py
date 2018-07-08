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
    data = app.current_request.json_body
    set_trace()
    res = calculate.calculate(data)
    return res
