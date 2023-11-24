import psutil
import pandas as pd
from datetime import datetime, timedelta
from collections import OrderedDict

class Process:
    def _init_(self, pid, name, cpu_usage, memory_usage, read_bytes, write_bytes, status, create_time, n_threads, cores):
        self.pid = pid
        self.name = name
        self.cpu_usage = cpu_usage
        self.memory_usage = memory_usage
        self.read_bytes = read_bytes
        self.write_bytes = write_bytes
        self.status = status
        self.create_time = create_time
        self.n_threads = n_threads
        self.cores = cores

class PageReplacementSimulator:
    def _init_(self):
        self.processes = OrderedDict()
        self.page_frames = OrderedDict()
        self.page_replacement_history = []

    def add_process(self, process):
        self.processes[process.pid] = process

    def update_page_frames(self, process_name, algorithm):
        if algorithm == 'LRU':
            self.page_frames = OrderedDict(sorted(self.page_frames.items(), key=lambda x: x[1]['last_used']))
        elif algorithm == 'FIFO':
            self.page_frames = OrderedDict(sorted(self.page_frames.items(), key=lambda x: x[1]['arrival_time']))
        elif algorithm == 'Optimal':
            self.page_frames = OrderedDict(sorted(self.page_frames.items(), key=lambda x: x[1]['optimal_distance']))

    def simulate_page_replacement(self, algorithm):
        replacement_actions = []
        current_time = datetime.now()

        for pid, process in self.processes.items():
            if process.name not in self.page_frames:
                replacement_actions.append((algorithm, process.name, current_time))
                self.page_frames[process.name] = {'last_used': current_time, 'arrival_time': current_time, 'optimal_distance': float('inf')}
                if len(self.page_frames) > 3:
                    del self.page_frames[next(iter(self.page_frames))]
            else:
                self.page_frames[process.name]['last_used'] = current_time

        # Append replacement actions to history
        self.page_replacement_history.extend(replacement_actions)

        self.print_page_replacement_actions(algorithm, replacement_actions)
        return replacement_actions

    def simulate_optimal_page_replacement(self):
        replacement_actions = []
        current_time = datetime.now()

        for pid, process in self.processes.items():
            if process.name not in self.page_frames:
                replacement_actions.append((pid, process.name, current_time))
                self.page_frames[process.name] = {'last_used': current_time, 'arrival_time': current_time, 'optimal_distance': float('inf')}
                if len(self.page_frames) > 3:
                    del self.page_frames[next(iter(self.page_frames))]
            else:
                self.page_frames[process.name]['last_used'] = current_time

        # Append replacement actions to history
        self.page_replacement_history.extend(replacement_actions)

        self.print_page_replacement_actions('Optimal', replacement_actions)
        return replacement_actions

    def print_process_info(self):
        process_data = []
        for pid, process in self.processes.items():
            process_data.append([process.name, process.cpu_usage, process.memory_usage, process.read_bytes,
                                 process.write_bytes, process.status, process.create_time, process.n_threads,
                                 process.cores])

        columns = ["name", "cpu_usage", "memory_usage", "read_bytes", "write_bytes", "status", "create_time",
                   "n_threads", "cores"]
        process_df = pd.DataFrame(process_data, index=self.processes.keys(), columns=columns)
        print("\n=== Process Information ===")
        print(process_df)

    def print_page_replacement_actions(self, algorithm, replacement_actions):
        print(f"\n=== {algorithm} Page Replacement Actions ===")
        for action in replacement_actions:
            print(f"{algorithm} Page Replacement: {action[1]}")

    def display_process_viewer(self):
        process_list = []
        for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters', 'status', 'create_time', 'num_threads', 'cpu_affinity']):
            process_info = {
                'pid': process.info['pid'],
                'name': process.info['name'],
                'cpu_percent': process.info['cpu_percent'],
                'memory_info': process.info['memory_info'],
                'io_counters': process.info['io_counters'],
                'status': process.info['status'],
                'create_time': datetime.fromtimestamp(process.info['create_time']),
                'num_threads': process.info['num_threads'],
                'cpu_affinity': process.info['cpu_affinity'],
            }
            process_list.append(process_info)

        process_df = pd.DataFrame(process_list)
        print("\n=== Process Viewer ===")
        print(process_df)

    def get_recent_replacement_actions(self, milliseconds=100000):
        now = datetime.now()
        current_time = now.strftime("%H:%M:%S.%f")
       

        # Assuming you have a variable 'minutes' with the desired time difference
        threshold_time = now - timedelta(milliseconds=milliseconds)
        print("Start Time:", threshold_time)
        print(" End Time:", current_time)
        
        
        total_time = now - threshold_time
        print("Total Time:", total_time)
        
        total_time_ms = total_time.total_seconds() * 1000
        recent_actions = [action for action in self.page_replacement_history if action[2] >= threshold_time]
        return recent_actions

# Example usage
if _name_ == "_main_":
    simulator = PageReplacementSimulator()

    # Add processes
    for process in psutil.process_iter(['pid', 'name', 'cpu_percent', 'memory_info', 'io_counters', 'status', 'create_time', 'num_threads', 'cpu_affinity']):
        simulator.add_process(Process(
            process.info['pid'],
            process.info['name'],
            process.info['cpu_percent'],
            process.info['memory_info'].rss,
            process.info['io_counters'].read_bytes,
            process.info['io_counters'].write_bytes,
            process.info['status'],
            datetime.fromtimestamp(process.info['create_time']),
            process.info['num_threads'],
            len(process.info['cpu_affinity']) if process.info['cpu_affinity'] is not None else 0,
        ))

    # Simulate LRU Page Replacement
    lru_replacement_actions = simulator.simulate_page_replacement('LRU')

    # Simulate FIFO Page Replacement
    fifo_replacement_actions = simulator.simulate_page_replacement('FIFO')

    # Simulate Optimal Page Replacement
    print("\n\n\n\n\n")
    optimal_replacement_actions = simulator.simulate_optimal_page_replacement()

    # Display process information
    simulator.print_process_info()

    # Display process viewer
    simulator.display_process_viewer()
    recent_replacement_actions = simulator.get_recent_replacement_actions(milliseconds=100000)
    print("\n===Page Replacement Actions during the execution of the current process===")
    for action in recent_replacement_actions:
        print(f"{action[0]} Page Replacement: {action[1]} at {action[2]}")
    print("Process ID:", psutil.Process().pid)
