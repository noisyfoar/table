import numpy as np
import h5py

DATAS = 'data'
OBSERVERS = 'observers'
TYPES = 'types'

#обязательно добавить считывание количества строк и столбцов при открытии файла
# в obsevers в строке указаны столбцы, а в столбцах указаны наблюдатели
class Hdf:
    def __init__(self, filepath):
        self.filepath = filepath
        self.columns = 10
        self.rows = 10

    def show_data(self):
        with h5py.File(self.filepath, 'r') as f:
            data = f[DATAS][:]
            return data

    def write_cell(self, row, column, data):
        with h5py.File(self.filepath, 'w') as f:
            dataset = f[DATAS]
            dataset[row, column] = data
            self.notifyAll(column)
            # нужно еще оповестить всех наблюдателей, что мы обновились

    def update_observer(self, column_object, column_observer):
        with h5py.File(self.filepath, 'r+') as f:
            observers = f[OBSERVERS][:]

            if observers[column_object, column_observer] == 0:
                observers[column_object, column_observer] = 1
                visited = set()
                # проверка на цикличность для того, чтобы наблюдатель не следил за своими обновлениями
                if self.dfs(visited, observers, column_observer) is None:
                    return
                # если цикла нет, то происходит возвращение из функции, иначе не добавляем в список наблюдателя
                observers[column_object, column_observer] = 0
            else:
                observers[column_object, column_observer] = 0

    def update_type(self, column):
        with h5py.File(self.filepath, 'w') as f:
            types = f[TYPES]
            types[column] = int(types[column] == 0)

    def create_empty_table(self):
        with h5py.File(self.filepath, 'w') as f:
            arr = np.zeros(shape=(self.rows, self.columns))
            data = f.create_dataset(DATAS, data=arr)

            arr = np.zeros(10)
            f.create_dataset(TYPES, data=arr)

            arr = np.zeros(shape=(self.columns, self.columns))
            f.create_dataset(OBSERVERS, data=arr)
            # observers[:] = arr[:] если верхние две строки не заработают
            return data

    def update_column(self, observer_column):
        with h5py.File(self.filepath, 'r+') as f:
            observers = f[OBSERVERS]
            # Сначала надо посмотреть подписан ли он на кого-нибудь. Если да, то собрать их список. Если нет, то выходим из функции
            objects = set()
            for column in range(self.columns):
                if observers[column, observer_column] > 0:
                    objects.add(column)
            if len(objects) == 0:
                return
            arr = []
            # так как мы собрали список всех наблюдателей, то мы можем уже собрать данные с них
            data = f[DATAS]
            for column in objects:
                for row in range(self.rows):
                    arr[row] += data[row, column]
            for row in range(self.rows):
                data[row, observer_column] = arr[row]
        self.notifyAll(observer_column)


    def notifyAll(self, object_column):




    # вспомогательная функция для нахождения цикличности для наблюдателя, если возвращает 1, то цикл найден если None, то нет
    def dfs(self, visited, observers, observer):
        visited.add(observer)
        for neighbor in range(observers[:, observer]):
            if neighbor not in visited:
                self.dfs(visited, observers, neighbor)
            else:
                return 1
