from flask import Flask, render_template, jsonify, request
from data_service import get_student_data
import os
from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('dashboard1.html')

@app.route('/dashboard2')
def dashboard2():
    # This renders the specialized analytical view
    return render_template('dashboard2.html')


@app.route('/api/data')
def api_data():
    limit = request.args.get('limit', default=100, type=int)
    data = get_student_data(limit)
    return jsonify(data)

if __name__ == '__main__':
    h = os.getenv("APP_HOST", "0.0.0.0")
    p = int(os.getenv("APP_PORT", 5000))
    app.run(host=h, port=p, debug=True)