function data = getDataLigo(file)
hinfo = hdf5info(file);
data = hdf5read(hinfo.GroupHierarchy.Datasets(1));
end