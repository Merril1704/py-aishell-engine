"""
Executes validated commands in the system shell and orchestrates command engine logic.
"""
import subprocess
from .preprocessor import preprocess_input
from .safety import is_safe_command
from .mapper import map_nl_to_command

"""
Executes validated commands in the system shell and orchestrates command engine logic.
"""
import subprocess
import platform
import psutil
from .preprocessor import preprocess_input
from .safety import is_safe_command, get_confirmation_prompt
from .mapper import map_nl_to_command

class CommandEngine:
    def __init__(self):
        self.running_processes = {}  # PID -> process info
        self.is_windows = platform.system().lower() == 'windows'

    def process_input(self, user_input):
        """
        Main entry point for processing user input
        Returns: (success, output, error_msg)
        """
        try:
            # Stage 1: Input Pre-Processor
            normalized, mode, components = preprocess_input(user_input)
            
            # Stage 2: Command Mapper
            command = self.map_command(normalized, mode, components)
            
            # Stage 3: Safety Net & Validator
            is_safe_result, risk_level, safety_msg = is_safe_command(command)
            if not is_safe_result:
                if risk_level == 'critical':
                    return False, '', safety_msg
                else:
                    # Return confirmation prompt for GUI to handle
                    return False, '', get_confirmation_prompt(command, risk_level)
            
            # Stage 4: Execution Manager
            return self.execute_command(command)
            
        except Exception as e:
            return False, '', f"Error processing command: {str(e)}"

    def map_command(self, normalized, mode, components):
        """Map natural language to system command if needed"""
        if mode == 'nl':
            return map_nl_to_command(normalized, components)
        return normalized

    def execute_command(self, command):
        """
        Execute a validated command
        Returns: (success, stdout, stderr)
        """
        if not command:
            return False, '', 'Empty command'
        
        try:
            # Handle special commands
            if command.startswith('bg '):
                # Background process
                return self.start_background_process(command[3:])
            elif command.startswith('kill '):
                # Kill process
                return self.kill_process(command[5:])
            elif command == 'ps' or command == 'processes':
                # List processes
                return self.list_processes()
            
            # Execute regular command
            result = subprocess.run(
                command,
                shell=True,
                capture_output=True,
                text=True,
                timeout=30  # 30 second timeout
            )
            
            if result.returncode == 0:
                return True, result.stdout, result.stderr
            else:
                return False, result.stdout, result.stderr
                
        except subprocess.TimeoutExpired:
            return False, '', f'Command "{command}" timed out after 30 seconds'
        except Exception as e:
            return False, '', f'Execution error: {str(e)}'

    def start_background_process(self, command):
        """Start a process in the background"""
        try:
            process = subprocess.Popen(
                command,
                shell=True,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            self.running_processes[process.pid] = {
                'process': process,
                'command': command,
                'started': True
            }
            
            return True, f'Background process started with PID: {process.pid}', ''
            
        except Exception as e:
            return False, '', f'Failed to start background process: {str(e)}'

    def kill_process(self, pid_or_name):
        """Kill a process by PID or name"""
        try:
            # Try to parse as PID first
            try:
                pid = int(pid_or_name)
                if pid in self.running_processes:
                    process = self.running_processes[pid]['process']
                    process.terminate()
                    del self.running_processes[pid]
                    return True, f'Process {pid} terminated', ''
                else:
                    # Kill system process
                    psutil.Process(pid).terminate()
                    return True, f'System process {pid} terminated', ''
            except ValueError:
                # Kill by name
                killed_count = 0
                for proc in psutil.process_iter(['pid', 'name']):
                    if proc.info['name'].lower() == pid_or_name.lower():
                        proc.terminate()
                        killed_count += 1
                
                if killed_count > 0:
                    return True, f'Killed {killed_count} process(es) named "{pid_or_name}"', ''
                else:
                    return False, '', f'No process named "{pid_or_name}" found'
                    
        except Exception as e:
            return False, '', f'Failed to kill process: {str(e)}'

    def list_processes(self):
        """List running processes"""
        try:
            processes = []
            
            # Add our managed processes
            for pid, info in self.running_processes.items():
                processes.append(f"[MANAGED] PID: {pid}, Command: {info['command']}")
            
            # Add system processes (top 10 by CPU usage)
            system_procs = []
            for proc in psutil.process_iter(['pid', 'name', 'cpu_percent']):
                try:
                    system_procs.append((proc.info['cpu_percent'], proc.info['pid'], proc.info['name']))
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue
            
            # Sort by CPU usage and take top 10
            system_procs.sort(reverse=True)
            for cpu, pid, name in system_procs[:10]:
                processes.append(f"PID: {pid}, Name: {name}, CPU: {cpu}%")
            
            return True, '\n'.join(processes), ''
            
        except Exception as e:
            return False, '', f'Failed to list processes: {str(e)}'

    def cleanup(self):
        """Clean up any running background processes"""
        for pid, info in self.running_processes.items():
            try:
                info['process'].terminate()
            except:
                pass
        self.running_processes.clear()

# Legacy function for backward compatibility
def execute_command(command):
    """Legacy function for backward compatibility"""
    try:
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        return result.stdout, result.stderr
    except Exception as e:
        return '', str(e)
