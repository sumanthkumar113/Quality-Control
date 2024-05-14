import os
import json

from datetime import datetime
from flask import Flask, request, render_template

app = Flask(__name__, template_folder='templates')

# Configuration
import os
LOG_DIR = 'logs'
LOG_FILES = [os.path.join(LOG_DIR, file) for file in os.listdir(LOG_DIR) if file.endswith('.log')]

# Log Ingestor
def write_log(log_data, log_file):
    with open(log_file, 'a') as f:
        f.write(json.dumps(log_data) + '\n')

# Query Interface
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

    results = []
    for log_file in LOG_FILES:
        with open(log_file, 'r') as f:
            for line in f:
                log_data = json.loads(line)
                if (
                        (not level or log_data['level'] == level) and
                        (not log_string or log_string in log_data['log_string']) and
                        (not start_time or datetime.fromisoformat(log_data['timestamp']) >= datetime.fromisoformat(start_time)) and
                        (not end_time or datetime.fromisoformat(log_data['timestamp']) <= datetime.fromisoformat(end_time)) and
                        (not source or log_data['source'] == source)
                    ):
                    results.append(log_data)
                    

    return render_template('results.html', results=results)

if __name__ == '__main__':
    # Create log directory if it doesn't exist
    os.makedirs(LOG_DIR, exist_ok=True)

    # Example log ingestion
    for i in range(1, 10):
        log_file = f'{LOG_DIR}/log{i}.log'
        for j in range(10):
            log_data = {
                    'level': 'error' if j % 3 == 0 else 'info',
                    'log_string': f'Log message {i * 10 + j}',
                    'timestamp': datetime.now().isoformat(),
                    'source': log_file
                }
            write_log(log_data, log_file)

    app.run(debug=True)