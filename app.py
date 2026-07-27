from flask import Flask, render_template, request, jsonify
from sqlmodel import select

from database import init_db, get_session
from models import Transformation

app = Flask(__name__)

# Creates the SQLite file + table the first time the app runs.
init_db()


@app.route('/')
def home():
    """Serves the main page with the text input form."""
    return render_template('index.html')


@app.route('/transform', methods=['POST'])
def transform():
    """
    Receives raw text and a selected mode from the browser (POST request),
    processes it in Python, saves the record to the database, and returns
    the transformed result.
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

    # Persist this request to the database (Sprint 3: "Persist Inputs")
    with get_session() as session:
        record = Transformation(original_text=raw_text, transformed_text=transformed_text)
        session.add(record)
        session.commit()

    return jsonify({'result': transformed_text})


@app.route('/history')
def history():
    """Displays past submissions, newest first (Sprint 3: "Display History")."""
    with get_session() as session:
        statement = select(Transformation).order_by(Transformation.created_at.desc())
        records = session.exec(statement).all()
        return render_template('history.html', records=records)


if __name__ == '__main__':
    app.run(debug=True)