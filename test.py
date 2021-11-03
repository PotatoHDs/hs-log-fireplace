import time

from hslog import LogParser

FILEPATH = "test.log"


def check_for_update(filepath):
    with open(filepath, "r") as file:
        while True:
            time.sleep(0.1)
            temp = file.readlines()
            if len(temp) > 0:
                for t in temp:
                    if t != "\n":
                        fun_to_exec(t.replace("\n", ""))


def fun_to_exec(data):
    print(data)


if __name__ == '__main__':
    # check_for_update(FILEPATH)
    p = LogParser()
    with open(FILEPATH, "r") as file:
        while True:
            time.sleep(0.1)
            lines = file.readlines()
            if lines:
                for line in lines:
                    if line != '\n':
                        p.read_line(line)
                print(p.games[-1].export().game)
