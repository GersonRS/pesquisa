HOME = getenv('HOME');
hinfo = hdf5info(strcat(HOME,'/data/GW150914.h5'));
wave = hdf5read(hinfo.GroupHierarchy.Datasets(1));
template = hdf5read(hinfo.GroupHierarchy.Datasets(2));

figure
hold on;
plot(wave);
plot(template);
hold off;

residual = wave -template;

figure
hold on;
plot(residual);
hold off;

figure
hold on;
histfit (residual, 50, 'normal' )
hold off;

pd = fitdist (residual, 'Normal' );
rng default;  % for reproducibility
x = random(pd,length(template),1);

[h,p] = chi2gof(x,'Alpha',0.01);

generate = x + template;

figure
hold on;
plot(generate);
plot(wave);
plot(template);
hold off;

