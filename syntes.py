import random
from memory_profiler import memory_usage

COUNT_NUM = 10000000


def syntes_int(COUNT_NUM: int = COUNT_NUM) -> None:

    with open('input.txt', 'w') as f:

        for i in range(COUNT_NUM):
            f.write(str(random.randint(a=0, b=COUNT_NUM)) + '\n')

    print(memory_usage())