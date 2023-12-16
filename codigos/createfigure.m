
f = openfig('/home/gerson/Dropbox/Mestrado/Pesquisa/Imagens de Resultados/GW150914_LabH.fig');

H = findobj(f,'type','line');
x_data = get(H,'xdata');
y_data = get(H,'ydata');

HOME = getenv('HOME');
hinfo = hdf5info(strcat(HOME,'/pesquisa/aaaaaGW150914.h5'));
H1 = hdf5read(hinfo.GroupHierarchy.Datasets(1));
L1 = hdf5read(hinfo.GroupHierarchy.Datasets(2));

close all;

figure;
subplot(2,1,1);
plot(x_data, y_data);
ylabel('Score');
title('Score - Lab H - GW150914');
subplot(2,1,2);
hold on;
plot(H1(205:7987));
ylabel('Sinal');
xlabel('Tempo');
hold off;

