from flask import Flask, Response
from flask import render_template, request
from src.parser import parse
from src.logging import write_log
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address
import imgkit
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = os.urandom(24).hex()

limiter = Limiter(
    app,
    key_func=get_remote_address,
    storage_uri="memory://",
)


@app.route("/", methods=['GET', 'POST'])
@limiter.limit("1/second", override_defaults=False)
def searcher_page():
    query = request.args.get('q')
    write_log(request.remote_addr, f"query={query}", 200)
    if query:
        results = parse(query)

        return render_template('index.html', results=results)
    return render_template('index.html')


@app.route('/preview.png', methods=['GET'])
def preview():
    query = request.args.get('q')
    results = {"query": query}

    preview_html = render_template('card.html', results=results)

    try:
        os.remove('card.png')
    except OSError:
        pass

    try:
        imgkit.from_string(preview_html, 'card.png')
    except OSError:
        pass

    preview_img = open('card.png', 'rb').read()

    return Response(preview_img, mimetype='image/png')


@app.errorhandler(404)
def not_found_error(error):
    write_log(request.remote_addr, error, 404)
    return render_template('errors/404.html')


@app.errorhandler(429)
def spam_error(error):
    write_log(request.remote_addr, error, 429)
    return render_template('errors/429.html')


@app.errorhandler(500)
def server_error(error):
    write_log(request.remote_addr, error, 500)
    return render_template('errors/500.html')


if __name__ == '__main__':
    port = int(os.environ.get("PORT", 8001))
    app.run(host='0.0.0.0', port=port)
