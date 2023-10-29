import h5py

import hdf

filepath = 'random.hdf5'

file = hdf.Hdf(filepath)
file.update_observer(0, 1)
file.write_cell(0, 0, 1)
print(file.show_observers())
