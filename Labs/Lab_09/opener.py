import subprocess

servers = ['5001.py', '6001.py', '6002.py', '7001.py', '7002.py','7003.py','7004.py', '8001.py']

for server in servers:
    subprocess.Popen(['alacritty', '-e', 'python', server])

