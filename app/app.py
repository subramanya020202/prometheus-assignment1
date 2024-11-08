from flask import Flask, render_template, request
from prometheus_client import start_http_server, Gauge
import psutil  # For getting memory and CPU usage

app = Flask(__name__)

# Define Prometheus metrics
REQUEST_COUNT = Gauge('app_request_count', 'Total request count')
CPU_USAGE = Gauge('app_cpu_usage', 'CPU usage in percent')
MEMORY_USAGE = Gauge('app_memory_usage', 'Memory usage in percent')

# Dummy users for login
users = {
    'Sigmoid': 'sigmoid',
    'Deepak': 'deepak'
}

@app.route('/')
def index():
    return render_template('login.html')  # Login page

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in users and users[username] == password:
            return f"Welcome, {username}!"  # Can redirect to a dashboard
        else:
            return "Invalid username or password. Please try again.", 401

    return render_template('login.html')

@app.route('/metrics')
def metrics():
    # Collect metrics for Prometheus
    REQUEST_COUNT.inc()  # Increment request count
    CPU_USAGE.set(psutil.cpu_percent())  # Set CPU usage
    MEMORY_USAGE.set(psutil.virtual_memory().percent)  # Set Memory usage
    
    return "Metrics exposed!"

if __name__ == '__main__':
    # Start the Prometheus metrics server
    start_http_server(8000)  # Expose metrics on port 8000
    app.run(host='0.0.0.0', port=5000)  # Flask app runs on port 5000

