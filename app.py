from flask import Flask, render_template, request
from query_optimizer import analyze_query

app = Flask(__name__)


@app.route('/', methods=['GET', 'POST'])
def home():

    result = None

    if request.method == 'POST':

        query = request.form['query']

        result = analyze_query(query)

    return render_template(
        'index.html',
        result=result
    )


if __name__ == '__main__':
    app.run(debug=True)