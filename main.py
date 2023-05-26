import os
import shutil
import sys
import psutil
import glob
from syntes import syntes_int



'''
____________________________________________________

    LENGHT: int - длина массива, используется для генерации
    файла с числами (опционально)
____________________________________________________

    AVAILABLE_MEMORY - доступная оперативная память
____________________________________________________
    TEMPORARY_DIR: str - директория для временных файлов
____________________________________________________
'''

LENGHT: int = 100_000_000
AVAILABLE_MEMORY: float = list(psutil.virtual_memory())[1]
print(f'Обнаружено свободной виртуальной памяти {AVAILABLE_MEMORY}')
TEMPORARY_DIR: str = './temp'




#создаем временную директорию
def create_temp():
    if not os.path.isdir(TEMPORARY_DIR):
        os.mkdir(TEMPORARY_DIR)
    else:
        shutil.rmtree(TEMPORARY_DIR)
        os.mkdir(TEMPORARY_DIR)


    #temporary_dir_abs: path - абсолютный путь к директории
temporary_dir_abs = os.path.abspath(TEMPORARY_DIR)


def create_name_file(
        first_name: str, second_name: str, number_file: str
        ) -> str:
    #Функция для создания уникального имени
    return ''.join(
        [str(temporary_dir_abs), '/' , str(first_name),'_', str(second_name), '_',  str(number_file) ,'.txt']
        )


def initial_sort() -> None:
    #1/20 часть от доступной виртуальной памяти
    memory_array: int = round(AVAILABLE_MEMORY / 20)

    print(f'Выделено для чисел {memory_array}')
    '''
    Открытие input файла, постепенно читаем его.
    В data записываем числа из файла,  count_file
    для создания уникального имени файла
    '''
    with open('input.txt') as f:
        data = []
        count_file = 0
        for item in f:
            data.append(int(item))
            '''
            Если размер массива больше 1/20 часть вирутальной памяти
            минус размер дескриптора на открытый файл, то
            сортируем массив, преобразуем в строки и вставляем во временный
            файл с названием, генерирующимся в create_name_file
            Сохраняется в папке temp
            '''
            if sys.getsizeof(data) > (memory_array - sys.getsizeof(f)):
                data.sort()
                data = [str(i) for i in data]
                count_file += 1
                file_name = create_name_file(
                            data[0],
                            data[-1],
                            count_file
                        )
                print(f'Создан временный файл {file_name}')
                with open(
                        create_name_file(
                            data[0], 
                            data[-1], 
                            count_file
                        ),
                        'w'
                    ) as f_w:
                    f_w.write('\n'.join(data))
                data = []
        '''
        В конце у нас файл может быть полностью прочитан,
        но условие выше не выполняется и тогда мы остатки чисел
        сортируем отдельно и вставляем в файл по той же схеме
        '''

        data.sort()
        data = [str(i) for i in data]
        count_file += 1
        file_name = create_name_file(
                    data[0],
                    data[-1],
                    count_file
                )
        print(f'Создан временный файл {file_name}')
        with open(
                create_name_file(
                    data[0], 
                    data[-1], 
                    count_file
                ),
                'w'
            ) as f_w:
            f_w.write('\n'.join(data))
        #Удаляем на всякий случай
        del data
        del count_file

    
#Функция для создания массива с временными файлами (названиями)
def list_files() -> list:
    files = list(glob.glob('./temp/*.txt'))
    return files


#Сортировка значений во временных файлах
def sort_temp(files: list) -> None:
    '''
    files_open - массив с IO на файлы
    files_flag - массив с флагами, который показывает, закончился
    файл с соответствующим индексом или нет
    data - массив для записи и сортировки
    '''
    files_open = []
    files_flag = []
    data = []
    #добавляем в files_open IO на файлы
    for i in range(len(files)):
        files_open.append(open(files[i]))
        files_flag.append(1)

    '''
    Считаем количество файлов и делим для расчета
    того, сколько нам памяти можно использовать (примерно)
    '''
    num_files = len(files_open)
    memory_array = (AVAILABLE_MEMORY / num_files**2)


    print(f'Количество обнаруженных временных файлов {num_files}')
    print(f'Количество выделенной памяти для сортировки {memory_array}')
    '''
    curr_item - для подсчета количества чисел, прошедших 
    через data
    count - количество раз, когда выкинулось исключение
    '''
    curr_item = 0
    count = 0
    #Пока хоть один файл не закончился
    while 1 in files_flag:
        for i in range(len(files_open)):
            #Если файл закончился, выбрасывается ValueError
            try:
                if files_flag[i] == 1:
                    data.append(int(files_open[i].readline()))
                    #Проверяем условие, если выполнено, то сортируем массив и вставляем в output
                    if sys.getsizeof(data) > memory_array:
                        data.sort()
                        curr_item += len(data)
                        data = [str(i) for i in data]
                        with open('output.txt', 'a') as f:
                            f.write('\n'.join(data))

                        data = []

            #Если выбросилось исключение, флаг обнуляем
            except ValueError:
                files_flag[i] = 0
                count+=1
                print(count)
                
                #Проверяем условие, если выполнено, то сортируем массив и вставляем в output
                if sys.getsizeof(data) > memory_array:
                    data.sort()
                    curr_item += len(data)
                    data = [str(i) for i in data]

                    with open('output.txt', 'a') as f:
                        f.write('\n'.join(data))

                    data = []


    #Когда все файлы закончились, сортим остатки и вставляем в output
    data.sort()
    curr_item += len(data)
    data = [str(i) for i in data]

    with open('output.txt', 'a') as f:
        f.write('\n'.join(data))

    data = []

    for i in files_open:
        i.close()
    del data
    del files_open
    del files_flag
    print(f'curr_item {curr_item}')

    #Строка удаляет все временные файлы
    # shutil.rmtree(TEMPORARY_DIR)


'''
syntes_int - создает входной input файл длинны LENGHT
create_temp - создает папку temp, если ее не было и 
пересоздает полностью, если была
initial_sort - начальное разбиение входного файла
по временным файлам в папку temp
sort_temp - сортирует числа из всех файлов в папке
temp и при надобности удаляет ее
'''
if __name__ == '__main__':
    syntes_int(LENGHT)
    if os.path.exists('./output.txt'):
        os.remove('./output.txt')
    create_temp()
    initial_sort()
    sort_temp(list_files())