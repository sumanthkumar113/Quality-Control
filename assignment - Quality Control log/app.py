import os
import json
import re
import logging
from datetime import datetime
from flask import Flask, request, render_template, jsonify

app = Flask(__name__, template_folder='templates', static_folder='static')

# Configuration
LOG_DIR = 'logs'
os.makedirs(LOG_DIR, exist_ok=True)

# Logging Configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(os.path.join(LOG_DIR, 'app.log')),
        logging.StreamHandler()
    ]
)

# Placeholder for API Integration
def integrate_api(api_name, log_data):
    # Placeholder for integrating with API
    print(f"Capturing log from {api_name}: {log_data}")
    # Example: write_log(log_data, os.path.join(LOG_DIR, f"{api_name}.log"))

# Log Ingestor
def write_log(log_data, log_file):
    try:
        with open(log_file, 'a') as f:
            f.write(json.dumps(log_data) + '\n')
    except Exception as e:
        logging.error(f"Error writing log to {log_file}: {str(e)}")

@app.route('/')
def index():
    message = "Hello, Flask!"
    return render_template('index.html', message=message)

@app.route('/search', methods=['POST'])
def search():
    level = request.form.get('level')
    log_string = request.form.get('log_string')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    source = request.form.get('source')
    regex = request.form.get('regex', False)

    results = []
    for log_file in [os.path.join(LOG_DIR, file) for file in os.listdir(LOG_DIR) if file.endswith('.log')]:
        with open(log_file, 'r') as f:
            for line in f:
                log_data = json.loads(line)
                if (
                    (not level or log_data['level'] == level) and
                    (not log_string or (regex and re.search(log_string, log_data['log_string'])) or (not regex and log_string in log_data['log_string'])) and
                    (not start_time or datetime.fromisoformat(log_data['timestamp']) >= datetime.fromisoformat(start_time)) and
                    (not end_time or datetime.fromisoformat(log_data['timestamp']) <= datetime.fromisoformat(end_time)) and
                    (not source or log_data['metadata']['source'] == source)
                ):
                    results.append(log_data)

    return render_template('results.html', results=results)

if __name__ == '__main__':
    # Example: Integrate with API1
    log_data_api1 = {"level": "info", "log_string": "Log message from API1", "timestamp": datetime.utcnow().isoformat(), "metadata": {"source": "API1"}}
    integrate_api("API1", log_data_api1)
    
    # Example: Integrate with API2
    log_data_api2 = {"level": "info", "log_string": "Log message from API2", "timestamp": datetime.utcnow().isoformat(), "metadata": {"source": "API2"}}
    integrate_api("API2", log_data_api2)
    
    app.run(debug=True)
