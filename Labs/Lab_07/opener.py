import subprocess

servers = ['5001.py', '5002.py','5003.py','5004.py', '5005.py']

for server in servers:
    subprocess.Popen(['alacritty', '-e', 'python', server])

