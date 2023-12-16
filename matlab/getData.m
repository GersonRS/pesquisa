function [X, t, z] = getData(file)
hinfo = hdf5info(file);
X = hdf5read(hinfo.GroupHierarchy.Datasets(1));
t = hdf5read(hinfo.GroupHierarchy.Datasets(2));
z = hdf5read(hinfo.GroupHierarchy.Datasets(3));
end

