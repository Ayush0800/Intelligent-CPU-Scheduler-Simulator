from flask import Flask, render_template, request, jsonify
from scheduling_algorithms import FCFS, SJF, RoundRobin, SRTF, Priority

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/simulate', methods=['POST'])
def simulate():
    try:
        data = request.json
        if not data:
            return jsonify({'error': 'No data provided'}), 400

        processes = data.get('processes')
        if not processes:
            return jsonify({'error': 'No processes provided'}), 400

        algorithm = data.get('algorithm')
        if not algorithm:
            return jsonify({'error': 'No algorithm specified'}), 400

        quantum = data.get('quantum', 2)  # Default quantum for Round Robin

        # Validate process data
        for process in processes:
            if not all(key in process for key in ['id', 'arrival_time', 'burst_time']):
                return jsonify({'error': 'Invalid process data'}), 400
            if algorithm == 'Priority' and 'priority' not in process:
                return jsonify({'error': 'Priority value required for Priority scheduling'}), 400

        # Run the selected algorithm
        if algorithm == 'FCFS':
            result = FCFS(processes)
        elif algorithm == 'SJF':
            result = SJF(processes)
        elif algorithm == 'RR':
            if not isinstance(quantum, (int, float)) or quantum < 1:
                return jsonify({'error': 'Invalid quantum value'}), 400
            result = RoundRobin(processes, quantum)
        elif algorithm == 'SRTF':
            result = SRTF(processes)
        elif algorithm == 'Priority':
            result = Priority(processes)
        else:
            return jsonify({'error': f'Invalid algorithm: {algorithm}'}), 400

        # Validate result format
        required_keys = ['timeline', 'turnaround_time', 'waiting_time', 'avg_turnaround_time', 'avg_waiting_time']
        if not all(key in result for key in required_keys):
            return jsonify({'error': 'Invalid algorithm result format'}), 500

        return jsonify(result)

    except Exception as e:
        app.logger.error(f'Error in simulation: {str(e)}')
        return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    app.run(debug=True)