function [X, t] = getData(file)
hinfo = hdf5info(file);
X = hdf5read(hinfo.GroupHierarchy.Datasets(1));
t = hdf5read(hinfo.GroupHierarchy.Datasets(2));
end

