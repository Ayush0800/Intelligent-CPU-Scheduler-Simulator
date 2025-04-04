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
def SJF(processes):
    timeline = []
    current_time = 0
    remaining_processes = processes.copy()
    
    while remaining_processes:
        available = [p for p in remaining_processes if p['arrival_time'] <= current_time]
        if not available:
            current_time = min(p['arrival_time'] for p in remaining_processes)
            continue
        
        next_process = min(available, key=lambda x: x['burst_time'])
        timeline.append({
            'process': next_process['id'],
            'start': current_time,
            'end': current_time + next_process['burst_time']
        })
        current_time += next_process['burst_time']
        remaining_processes.remove(next_process)
    
    return calculate_metrics(timeline, processes)
#Alorithm of Round robin
def RoundRobin(processes, quantum):
    timeline = []
    current_time = 0
    remaining_processes = [(p['id'], p['burst_time'], p['arrival_time']) for p in processes]
    
    while remaining_processes:
        available = [p for p in remaining_processes if p[2] <= current_time]
        if not available:
            current_time = min(p[2] for p in remaining_processes)
            continue
        
        pid, burst, arrival = available[0]
        execution_time = min(quantum, burst)
        
        timeline.append({
            'process': pid,
            'start': current_time,
            'end': current_time + execution_time
        })
        
        current_time += execution_time
        remaining_burst = burst - execution_time
        
        remaining_processes.remove((pid, burst, arrival))
        if remaining_burst > 0:
            remaining_processes.append((pid, remaining_burst, arrival))
    
    return calculate_metrics(timeline, processes)

def SRTF(processes):
    timeline = []
    current_time = 0
    remaining_processes = [(p['id'], p['burst_time'], p['arrival_time'], p['burst_time']) for p in processes]
    current_process = None
    start_time = current_time
    
    while remaining_processes:
        # Update available processes at current time
        available = [p for p in remaining_processes if p[2] <= current_time]
        if not available:
            current_time = min(p[2] for p in remaining_processes)
            continue
        
        # Sort by remaining time (p[3] is remaining time)
        next_process = min(available, key=lambda x: x[3])
        
        # If different from current process, add current process to timeline
        if current_process is None or current_process[0] != next_process[0]:
            if current_process is not None:
                timeline.append({
                    'process': current_process[0],
                    'start': start_time,
                    'end': current_time
                })
            current_process = next_process
            start_time = current_time
        
        # Execute for 1 time unit
        current_time += 1
        remaining_time = next_process[3] - 1
        remaining_processes.remove(next_process)
        
        if remaining_time > 0:
            # Update process with new remaining time
            remaining_processes.append((next_process[0], next_process[1], next_process[2], remaining_time))
        else:
            # Process completed
            timeline.append({
                'process': next_process[0],
                'start': start_time,
                'end': current_time
            })
            current_process = None
    
    return calculate_metrics(timeline, processes)
#Alorithm of Priority 
def Priority(processes):
    timeline = []
    current_time = 0
    remaining_processes = [(p['id'], p['burst_time'], p['arrival_time'], p['priority']) for p in processes]
    
    while remaining_processes:
        available = [p for p in remaining_processes if p[2] <= current_time]
        if not available:
            current_time = min(p[2] for p in remaining_processes)
            continue
        
        # Select process with highest priority (lower number = higher priority)
        next_process = min(available, key=lambda x: (x[3], x[2]))  # Break ties with arrival time
        
        timeline.append({
            'process': next_process[0],
            'start': current_time,
            'end': current_time + next_process[1]
        })
        
        current_time += next_process[1]
        remaining_processes.remove(next_process)
    
    return calculate_metrics(timeline, processes)
