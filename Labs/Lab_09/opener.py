import subprocess

servers = ['5001.py', '6001.py', '7001.py']

for server in servers:
    subprocess.Popen(['alacritty', '-e', 'python', server])

