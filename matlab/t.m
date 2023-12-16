pd = makedist('Normal');
% 
x = -5:.01:5;
y = normpdf(x,0,1);

r = normrnd(0,1,[1,5000]);

xx = random(pd,100000,1)'-1.5;
yy = random(pd,100000,1)'+1.5;

p = cdf(pd,xx);

% figure
% hold on;
% histogram(xx,100);
% histogram(yy,100);
% xlabel('Score');
% ylabel('Frequência');
% title({'Problema Binário, Distribuição empírica do score.', [] });
% hold off;

% figure;
% yyyy = pdf(pd,x);
% plot(x,yyyy,'LineWidth',2);


figure
hold on;
% histogram(xx,100);
% plot(xx,p);
grid('on');
% [f_A,a] = ecdf(xx);
% plot(a,f_A, 'LineWidth', 5);
[f_B,b] = ecdf(yy);
xb = (b - min(b))/(max(b) - min(b));
plot(xb,f_B, 'LineWidth', 5);
% txt = '\leftarrow Classe Y';
% text(5,0.5,txt,'FontSize',14);

% txt = 'Classe X \rightarrow';
% text(-3.3,0.5,txt,'FontSize',14, 'LineWidth', 5);
% 
% dim = [0.46 0.4 0.09 0.1];
% str = {'Distância','      KS'};
% annotation('textbox',dim,'String',str);
% 
% xa = [.5 .5];
% ya = [.6 .9];
% annotation('arrow',xa,ya);
% 
% xa = [.5 .5];
% ya = [.495 .12];
% annotation('arrow',xa,ya);

% xlabel('Score')
% ylabel('Distribuição Empírica Acumulada')
%title({'Problema Binário, Distribuição empírica acumulada do score.', [] });
hold off;

