import hdf

filepath = 'random.hdf5'

file = hdf.Hdf(filepath)
file.create_empty_table()
print(file.show_data())
