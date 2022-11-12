from flask import Flask
from flask import render_template, request, redirect
from src.parser import parse
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()


@app.route("/", methods=['GET', 'POST'])
def page():
    query = request.args.get('q')
    if query:
        results = parse(query)
        return render_template('index.html', results=results)
    return render_template('index.html')


@app.errorhandler(404)
def not_found_error():
    return '404'


@app.errorhandler(500)
def server_error():
    return '500'


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port)
