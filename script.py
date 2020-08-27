import subprocess
import sys
import os
import socket
import urllib.request

task = sys.argv[1]
healthcheck = os.environ.get('CHECKURL_' + task.upper(), None)

def ping(s = ''):
    if healthcheck:
        try:
            urllib.request.urlopen(healthcheck + s, timeout=10)
        except socket.error as e:
            print("Failed to ping healthchecks.io")
            print(e)

ping('/start')
try:
    if task == 'create':
        rclone_destination = os.environ['DESTINATION']
        rclone_args = os.environ.get('RCLONE_ARGS', '--fast-list --delete-after --delete-excluded')
        subprocess.run('borgmatic -c /mnt/borgmatic create prune --stats -v 1', shell=True, check=True)
        subprocess.run(f'rclone sync /mnt/repo {rclone_destination} --config /mnt/rclone_config/rclone.conf {rclone_args}', shell=True, check=True)
    elif task == 'check':
        subprocess.run('borgmatic -c /mnt/borgmatic check -v 1', shell=True, check=True)
    ping()
except subprocess.CalledProcessError as e:
    ping('/fail')
print()