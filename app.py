from flask import Flask, request, jsonify, render_template, redirect, url_for, session
from Scheduling_algorithm import FCFS, SJF, RoundRobin, SRTF, Priority
from functools import wraps

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['TEMPLATES_AUTO_RELOAD'] = True
app.secret_key = 'your-secret-key-here'  # Change this to a secure secret key

# Demo users (replace with database in production)
USERS = {
    'admin': 'password123',
    'demo': 'demo123'
}

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session and request.endpoint != 'simulator':
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        
        if username in USERS and USERS[username] == password:
            session['username'] = username
            return redirect(url_for('simulator'))
        else:
            return render_template('login.html', error='Invalid credentials')
    
    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('login'))

@app.route('/simulator')
def simulator():
    return render_template('index.html', username=session.get('username', 'Guest'))

@app.route('/simulate', methods=['POST'])
@login_required
def simulate():
    try:
        data = request.get_json()
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        processes = data.get('processes')
        algorithm = data.get('algorithm')
        quantum = data.get('quantum', 2)

        if not processes:
            return jsonify({'error': 'No processes provided'}), 400
        if not algorithm:
            return jsonify({'error': 'No algorithm specified'}), 400

        # Validate process data
        for process in processes:
            if not isinstance(process.get('arrival_time'), int) or not isinstance(process.get('burst_time'), int):
                return jsonify({'error': 'Invalid process data: arrival_time and burst_time must be integers'}), 400
            if process.get('burst_time') <= 0:
                return jsonify({'error': 'Invalid process data: burst_time must be positive'}), 400
            if process.get('arrival_time') < 0:
                return jsonify({'error': 'Invalid process data: arrival_time cannot be negative'}), 400
            if algorithm == 'priority' and not isinstance(process.get('priority'), int):
                return jsonify({'error': 'Invalid process data: priority must be an integer for Priority scheduling'}), 400

        # Run the selected algorithm
        result = None
        if algorithm == 'fcfs':
            result = FCFS(processes)
        elif algorithm == 'sjf':
            result = SJF(processes)
        elif algorithm == 'rr':
            if not isinstance(quantum, int) or quantum <= 0:
                return jsonify({'error': 'Invalid quantum value'}), 400
            result = RoundRobin(processes, quantum)
        elif algorithm == 'srtf':
            result = SRTF(processes)
        elif algorithm == 'priority':
            result = Priority(processes)
        else:
            return jsonify({'error': 'Invalid algorithm specified'}), 400

        if not result:
            return jsonify({'error': 'Algorithm execution failed'}), 500

        return jsonify(result)

    except Exception as e:
        print(f"Error in simulate: {str(e)}")
        return jsonify({'error': f'Server error: {str(e)}'}), 500

@app.route('/algorithm_info/<algorithm>')
def algorithm_info(algorithm):
    info = {
        'fcfs': {
            'name': 'First Come First Serve (FCFS)',
            'description': 'Processes are executed in the order they arrive in the ready queue.',
            'characteristics': [
                'Non-preemptive scheduling algorithm',
                'Simple and easy to implement',
                'Poor average waiting time',
                'Can cause convoy effect'
            ],
            'best_for': [
                'Batch systems',
                'Simple task processing',
                'When process times are similar'
            ],
            'example': 'If processes P1, P2, P3 arrive at times 0, 2, 4 with burst times 5, 3, 3, they will execute in order: P1 → P2 → P3'
        },
        'sjf': {
            'name': 'Shortest Job First (SJF)',
            'description': 'Processes are executed based on their burst time, shortest first.',
            'characteristics': [
                'Non-preemptive scheduling algorithm',
                'Optimal average waiting time',
                'Requires knowing/estimating burst time',
                'May cause starvation of longer processes'
            ],
            'best_for': [
                'When burst times are known',
                'Batch processing systems',
                'Minimizing average waiting time'
            ],
            'example': 'If P1(5), P2(3), P3(3) arrive together, execution order: P2 → P3 → P1'
        },
        # Add other algorithms...
    }
    return jsonify(info.get(algorithm, {'error': 'Algorithm not found'}))

@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, post-check=0, pre-check=0, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '-1'
    return response

if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)
