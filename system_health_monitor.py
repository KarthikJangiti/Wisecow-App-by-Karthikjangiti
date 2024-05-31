import psutil
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='system_health.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define thresholds
CPU_THRESHOLD = 80  # CPU usage percentage
MEMORY_THRESHOLD = 80  # Memory usage percentage
DISK_THRESHOLD = 80  # Disk usage percentage
PROCESS_THRESHOLD = 100  # Number of processes

def log_alert(message):
    logging.info(message)
    print(message)

def check_cpu_usage():
    cpu_usage = psutil.cpu_percent(interval=1)
    if cpu_usage > CPU_THRESHOLD:
        log_alert(f'High CPU usage detected: {cpu_usage}%')

def check_memory_usage():
    memory_info = psutil.virtual_memory()
    memory_usage = memory_info.percent
    if memory_usage > MEMORY_THRESHOLD:
        log_alert(f'High Memory usage detected: {memory_usage}%')

def check_disk_usage():
    disk_info = psutil.disk_usage('/')
    disk_usage = disk_info.percent
    if disk_usage > DISK_THRESHOLD:
        log_alert(f'High Disk usage detected: {disk_usage}%')

def check_running_processes():
    process_count = len(psutil.pids())
    if process_count > PROCESS_THRESHOLD:
        log_alert(f'High number of running processes detected: {process_count}')

def monitor_system_health():
    log_alert('Starting system health check...')
    check_cpu_usage()
    check_memory_usage()
    check_disk_usage()
    check_running_processes()
    log_alert('System health check completed.')

if __name__ == "__main__":
    monitor_system_health()
