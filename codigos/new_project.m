HOME = getenv('HOME');
[x, t] = getData(strcat(HOME,'/pesquisa/aaaaa/data_uniform.h5'));
waves = {'GW150914', 'GW151012', 'GW151226', 'GW170104', 'GW170608', 'GW170729', 'GW170809', 'GW170814', 'GW170818', 'GW170823'};
ligo = char(waves(1));
hinfo = hdf5info(strcat(HOME,'/pesquisa/aaaaa/',ligo,'_complete.h5'));
GW150914 = hdf5read(hinfo.GroupHierarchy.Datasets(1));

