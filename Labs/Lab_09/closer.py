import psutil

def close_alacritty_instances():
    for process in psutil.process_iter(['name', 'pid']):
        if process.info['name'] == 'alacritty':
            print(f"Closing Alacritty instance with PID: {process.info['pid']}")
            process.terminate()

if __name__ == "__main__":
    close_alacritty_instances()
