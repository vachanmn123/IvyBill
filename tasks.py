import time
import subprocess

while True:
    try:
        subprocess.run(["python3", "manage.py", "serverFunc"])
        time.sleep(60)
    except KeyboardInterrupt:
        print("KeyboardInterrupt")
        exit(0)
