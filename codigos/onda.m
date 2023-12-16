HOME = getenv('HOME');
waveNoiseInfo = hdf5info(strcat(HOME,'/data/H-H1_LOSC_C01_16_V1-1180922478-32.hdf5'));
waveCleanInfo = hdf5info(strcat(HOME,'/data/H-H1_LOSC_CLN_16_V1-1180922478-32.hdf5'));

waveClean = hdf5read(waveCleanInfo.GroupHierarchy.Groups(3).Datasets(1));
waveNoise = hdf5read(waveNoiseInfo.GroupHierarchy.Groups(3).Datasets(1));

noise = waveNoise - waveClean;

figure
hold on;
plot(waveNoise,'green');
plot(waveClean,'red');
hold off;

figure
hold on;
plot(noise);
hold off;

