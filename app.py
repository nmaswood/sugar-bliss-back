from chalice import Chalice
from sugar_bliss_backend import calculate

app = Chalice(app_name='sugar-bliss-backend')
app.debug = True


@app.route('/submit', methods=('POST',))
def submit():
    data = app.current_request.json_body
    res = calculate.calculate(data)

    return res

