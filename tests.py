import glob
import sys

#Проверка на то, сколько чисел в файлах
sys.path.append('.')

from main import LENGHT

def test_temp():
    files = list(glob.glob('./temp/*.txt'))
    print(len(files))

    iter: int = 0

    for file in files:
        for i in open(file):
            iter+=1

    assert iter == LENGHT

def test_output():
    iter = 0
    for i in open('output.txt'):
        iter += 1
    
    assert iter == LENGHT
