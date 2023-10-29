import hdf

filepath = 'random.hdf5'

file = hdf.Hdf(filepath)
file.create_empty_or_load_table()
file.update_type(0)
print(file.show_types())
