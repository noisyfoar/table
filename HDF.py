import numpy as np
import h5py

DATAS = 'data'
OBSERVERS = 'observers'
TYPES = 'types'
TABLE = 'table'
MAX_COLUMN = 20
MAX_ROW = 20
DATA_TYPE = 'i8'
OBS_TYP_TYPES = 'i1'

MAX_SHAPE = (MAX_ROW, MAX_COLUMN)


# обязательно добавить считывание количества строк и столбцов при открытии файла

# в observers в строках указаны столбцы, а в столбцах указаны наблюдатели

# сделать проверку, если существует, иначе создать новый

class Table:
    def __init__(self, filepath):
        self.filepath = filepath
        self.columns = 10
        self.rows = 10

    def show_data(self):
        with h5py.File(self.filepath, 'r') as f:
            data = f[DATAS][:]
            return data

    def show_observers(self):
        with h5py.File(self.filepath, 'r') as f:
            observers = f[OBSERVERS][:]
            return observers

    def show_types(self):
        with h5py.File(self.filepath, 'r') as f:
            types = f[TYPES][:]
            return types

    def write_cell(self, row, object_column, value):
        with h5py.File(self.filepath, 'r+') as f:
            data = f[DATAS]
            data[row, object_column] = value
            # оповещаем всех наблюдателей, что столбец изменился
            self.notify_all(object_column)

    def update_observer(self, column_object, column_observer):
        with h5py.File(self.filepath, 'r+') as f:
            observers = f[OBSERVERS]
            if observers[column_object, column_observer] == 0:
                observers[column_object, column_observer] = 1
                visited = set()
                # проверка на цикличность для того, чтобы наблюдатель не следил за своими обновлениями
                # если цикла нет, то происходит возвращение из функции, иначе не добавляем в список наблюдателя
                if self.dfs(visited, observers, column_observer) is None:
                    return
            else:
                observers[column_object, column_observer] = 0

        # вспомогательная функция для нахождения цикличности для наблюдателя, если возвращает 1, то цикл найден если None, то нет

    def dfs(self, visited, observers, observer):
        visited.add(observer)
        for neighbor in range(self.columns):
            if observers[observer, neighbor] == 1:
                if neighbor not in visited:
                    if self.dfs(visited, observers, neighbor) is not None:
                        return -1
                else:
                    return -1

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
            arr = [0] * self.columns
            # так как мы собрали список всех наблюдателей, то мы можем уже собрать данные с них
            data = f[DATAS][:]
            for column in objects:
                for row in range(self.rows):
                    arr[row] += data[row, column]
            # нужно в цикле пройтись по всем наблюдателем, так как их может быть несколько

            # запишем эти данные в колонку
            data[0, observer_column] = arr[0]
            for row in range(1, self.rows):
                data[row, observer_column] = arr[row] + data[row - 1, observer_column]
        self.notify_all(observer_column)

    def notify_all(self, object_column):
        with h5py.File(self.filepath, 'r') as f:
            observers = f[OBSERVERS][:]
            for observer_column in range(self.columns):
                if observers[object_column, observer_column] == 1:
                    self.update_column(observer_column)

    def update_type(self, column):
        with h5py.File(self.filepath, 'r+') as f:
            types = f[TYPES]
            types[column] = int(not types[column])

    def zeros(self):
        with h5py.File(self.filepath, 'w') as f:
            arr = np.zeros(shape=(self.columns, self.columns))
            data = f.create_dataset(DATAS, data=arr, dtype=DATA_TYPE, maxshape=MAX_SHAPE)
            f.create_dataset(OBSERVERS, data=arr, dtype=OBS_TYP_TYPES, maxshape=(MAX_COLUMN, MAX_COLUMN))
            arr = np.zeros(10)
            f.create_dataset(TYPES, data=arr, dtype=OBS_TYP_TYPES, maxshape=MAX_COLUMN)
            return data

    def load(self):
        with h5py.File(self.filepath, 'r+') as f:
            if DATAS in f:
                data = f[DATAS]
                self.rows, self.columns = data.shape
                return data

    # мысль: лучше сделать изменения отдельно и наложить друг на друга,
    # то есть сначала изменить размер строк потом размер столбцов,
    # а в ресайзе просто вызвать обе функции
    def resize(self, size=None):
        with h5py.File(self.filepath, 'r+') as f:
            rows, columns = size
            f[DATAS].resize(size=size)
            f[OBSERVERS].resize(size=(columns, columns))
            f[TYPES].resize(size=(columns,))
