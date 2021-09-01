import time
from pathlib import Path


def main():
    hs_path = Path('/') / 'Applications' / 'Hearthstone' / 'Logs' / 'Power.log'
    file = open(hs_path, "r")
    while True:
        line = file.readline()
        if line:
            print(line)
        else:
            time.sleep(0.2)


if __name__ == '__main__':
    main()
