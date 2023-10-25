import numpy as np
import h5py

DATAS = 'data'
OBSERVERS = 'observers'
TYPES = 'types'


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

    def update_observer(self, choice, column_object, column_observer):
        with h5py.File(self.filepath, 'w') as f:
            observers = f[OBSERVERS]
            observers[column_object, column_observer] = int(choice)

    def update_type(self, choice, column):
        with h5py.File(self.filepath, 'w') as f:
            types = f[TYPES]
            types[column] = choice

    def create_empty_table(self):
        with h5py.File(self.filepath, 'w') as f:
            arr = np.zeros(shape=(10, self.columns))
            data = f.create_dataset(DATAS, data=arr)

            arr = np.zeros(10)
            f.create_dataset(TYPES, data=arr)

            arr = np.zeros(shape=(self.columns, self.columns), dtype=np.bool)
            f.create_dataset(OBSERVERS, dtype='u1', data=arr)  # u1-unsigned 1 byte
            # observers[:] = arr[:]
            return data

    # def update_column(self, r):
    #       with h5py.File(self.filepath, 'r+') as f:
