HOME = getenv('HOME');
[x, t] = getData(strcat(HOME,'/pesquisa/aaaaa/data.h5'));

subplot(3,1,1);
plot(x(:,1));
legend('Template');
ylabel('whitened strain');
title('0 offset.')
subplot(3,1,2);
plot(x(:,2));
legend('Template');
ylabel('whitened strain');
title('0,01 offset.')
subplot(3,1,3);
plot(x(:,3));
legend('Template');
ylabel('whitened strain');
title('0,02 offset.')


