from flask import Flask, render_template, jsonify, request
import time  # 1. Import the time module
from data_service import get_student_data
from data_service import get_student_data_excel
from make_sample_data_excel import generate_synthetic_data
import os

from dotenv import load_dotenv

load_dotenv()
app = Flask(__name__)

@app.route('/')
def index():
    start_time = time.perf_counter()
    
    # Step 1: Simulated dashboard processing/auth check/data prep
    time.sleep(0.05) # Simulated brief delay
    
    end_time = time.perf_counter()
    execution_time = round(end_time - start_time, 4)
    
    # Pass the time variable into the template
    return render_template('dashboard1.html', backend_time=execution_time)


@app.route('/dashboard2')
def dashboard2():
    start_time = time.perf_counter()
    
    # Step 1: Analytical view heavy preparation logic
    time.sleep(0.12) # Simulated brief delay
    
    end_time = time.perf_counter()
    execution_time = round(end_time - start_time, 4)
    
    # Pass the time variable into the template
    return render_template('dashboard2.html', backend_time=execution_time)
  
@app.route('/api/data')
def api_data():
    limit = request.args.get('limit', default=100, type=int)
    data = get_student_data_excel(limit)
    return jsonify(data)
    
    
@app.route('/api/api_generate_synthetic_data')
def api_generate_synthetic_data():
    # 1. Get the limit from URL parameters
    limit = request.args.get('limit', default=1000, type=int)
    
    try:
        # 2. Call your logic function (which saves to the static folder)
        file_path = generate_synthetic_data(limit)
        
        # 3. Return a JSON response
        return jsonify({
            "status": "success",
            "message": f"Generated {limit} records",
            "file_path": file_path
        })
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 500

# FIXED: Changed '__app__' to '__main__'
if __name__ == '__main__':
    h = os.getenv("APP_HOST", "0.0.0.0")
    p = int(os.getenv("APP_PORT", 5000))
    app.run(host=h, port=p, debug=True)