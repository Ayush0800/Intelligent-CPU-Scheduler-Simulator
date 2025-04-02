def calculate_metrics(timeline, processes):
    n = len(processes)
    completion_time = {}
    turnaround_time = {}
    waiting_time = {}
    
    for t in timeline:
        if t['process'] not in completion_time:
            completion_time[t['process']] = t['end']
        else:
            completion_time[t['process']] = max(completion_time[t['process']], t['end'])
    
    for p in processes:
        pid = p['id']
        turnaround_time[pid] = completion_time[pid] - p['arrival_time']
        waiting_time[pid] = turnaround_time[pid] - p['burst_time']
    
    avg_turnaround = sum(turnaround_time.values()) / n
    avg_waiting = sum(waiting_time.values()) / n
    
    return {
        'timeline': timeline,
        'completion_time': completion_time,
        'turnaround_time': turnaround_time,
        'waiting_time': waiting_time,
        'avg_turnaround_time': avg_turnaround,
        'avg_waiting_time': avg_waiting
    }
#Alorithm of First come first Search
def FCFS(processes):
    timeline = []
    current_time = 0
    sorted_processes = sorted(processes, key=lambda x: x['arrival_time'])
    
    for p in sorted_processes:
        if current_time < p['arrival_time']:
            current_time = p['arrival_time']
        
        timeline.append({
            'process': p['id'],
            'start': current_time,
            'end': current_time + p['burst_time']
        })
        current_time += p['burst_time']
    
    return calculate_metrics(timeline, processes)
#Alorithm of Shortest JOb First