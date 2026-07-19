from flask import Flask, render_template, request, jsonify

app = Flask(__name__)


@app.route('/')
def home():
    """Serves the main page with the text input form."""
    return render_template('index.html')


@app.route('/transform', methods=['POST'])
def transform():
    """
    Receives raw text and a selected mode from the browser (POST request),
    processes it in Python, and returns the transformed result.
    """
    data = request.get_json()
    raw_text = data.get('text', '')
    mode = data.get('mode', 'upper')

    if mode == 'upper':
        transformed_text = raw_text.upper()
    elif mode == 'lower':
        transformed_text = raw_text.lower()
    elif mode == 'title':
        transformed_text = raw_text.title()
    elif mode == 'reverse':
        transformed_text = raw_text[::-1]
    else:
        transformed_text = raw_text

    return jsonify({'result': transformed_text})


if __name__ == '__main__':
    app.run(debug=True)
