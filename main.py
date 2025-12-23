# main.py
from bear import tick
import time

if __name__ == "__main__":
    while True:
        print(tick())
        time.sleep(5)