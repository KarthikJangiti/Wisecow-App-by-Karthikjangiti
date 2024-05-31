import os
import tarfile
import paramiko
from scp import SCPClient
import logging
from datetime import datetime

# Configure logging
logging.basicConfig(filename='backup.log', level=logging.INFO, format='%(asctime)s - %(message)s')

# Define backup parameters
LOCAL_DIR = '/path/to/local/directory'
BACKUP_NAME = f'backup_{datetime.now().strftime("%Y%m%d%H%M%S")}.tar.gz'
REMOTE_SERVER = 'remote.server.com'
REMOTE_USER = 'username'
REMOTE_PASSWORD = 'password'
REMOTE_DIR = '/path/to/remote/directory'

def create_tarfile(source_dir, output_filename):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))

def log_report(message):
    logging.info(message)
    print(message)

def backup_directory():
    try:
        # Create a tar.gz file of the directory
        log_report(f'Starting backup of directory: {LOCAL_DIR}')
        create_tarfile(LOCAL_DIR, BACKUP_NAME)
        log_report(f'Created tar file: {BACKUP_NAME}')

        # Establish SSH connection
        ssh = paramiko.SSHClient()
        ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        ssh.connect(REMOTE_SERVER, username=REMOTE_USER, password=REMOTE_PASSWORD)
        log_report(f'Connected to remote server: {REMOTE_SERVER}')

        # SCP the tar file to the remote server
        with SCPClient(ssh.get_transport()) as scp:
            scp.put(BACKUP_NAME, REMOTE_DIR)
        log_report(f'Successfully backed up to remote server: {REMOTE_SERVER}/{REMOTE_DIR}/{BACKUP_NAME}')

        # Clean up the local tar file
        os.remove(BACKUP_NAME)
        log_report(f'Local backup file removed: {BACKUP_NAME}')

    except Exception as e:
        log_report(f'Backup failed: {e}')

if __name__ == "__main__":
    backup_directory()
