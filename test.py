import time

FILEPATH = "./log.txt"


def check_for_update(filepath):
    n = 0
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
    check_for_update(FILEPATH)