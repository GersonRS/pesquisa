HOME = getenv('HOME');
% % events = ["170405", "170720", "170630", "161217", "170412", "161202", "151008", "170208", "151012A", "170423", "170616", "170219", "170705", "151116"];
% events = ["GW150914", "GW151012", "GW151226", "GW170104", "GW170608", "GW170729", "GW170809", "GW170814", "GW170823", "GW170817"];
% % for name = events
% hinfo = hdf5info(strcat(HOME,'/pesquisa/dados-4Khz-janela-410/',char(events(1)),'.h5'));
% H1 = hdf5read(hinfo.GroupHierarchy.Datasets(1));
% L1 = hdf5read(hinfo.GroupHierarchy.Datasets(2));
% 
% yH1 = net(H1);
% yL1 = net(L1);
% 
% scoreH1 = (yH1(1,:)-yH1(2,:))/2 + 0.5;
% scoreL1 = (yL1(1,:)-yL1(2,:))/2 + 0.5;
% 
% scoreHL = scoreH1 .* scoreL1;
% figure
% hold on;
% title({char(events(1))});
% plot(smooth(scoreHL,50));
% hold off;
% end
% [x1, x2, x3] = getData();
% y1 = net(x1);
% score1 = (y1(1,:)-y1(2,:))/2 + 0.5;
% y2 = net(x2);
% score2 = (y2(1,:)-y2(2,:))/2 + 0.5;
% y3 = net(x3);
% score3 = (y3(1,:)-y3(2,:))/2 + 0.5;
% 
% hold on;
% plot(smooth(score1,200));
% plot(smooth(score2,200));
% plot(smooth(score3,200));
% hold off;


load(strcat(HOME,'/pesquisa/dados-4Khz-janela-410/','dados-treinamento.mat'),'x','t')

% net = feedforwardnet(20,'traingda');
% net = configure(net,x,t);
% net.trainParam.epochs = 100000;
% net.trainParam.lr = 0.001;
% net.trainParam.min_grad = 1e-05;
% net.trainParam.max_fail = 100;
% net.layers{1}.transferFcn = 'logsig';
% net.layers{2}.transferFcn = 'purelin';
% [net] = train(net,x,t);
% 
% save(strcat(HOME,'/pesquisa/dados-4Khz-janela-',version,'/rede','.mat'),'net')
% load(strcat(HOME,'/pesquisa/dados-4Khz-janela-410/rede.mat'),'net')
% y = net(x);
% 
% score = (y(1,:)-y(2,:))/2 + 0.5;
% 
% contA = 1;
% contB = 1;
% 
% A = zeros(1,length(score)/2);
% B = zeros(1,length(score)/2);
% 
% for i=1:length(score)
%     if t(1,i) == 1
%         A(contA) = score(i);
%         contA = contA + 1;
%     else
%         B(contB) = score(i);
%         contB = contB + 1;
%     end
% end
% 
% 
% figure
% hold on;
% [f_A,a] = ecdf(A);
% [f_B,b] = ecdf(B);
% plot(a,f_A);
% plot(b,f_B);
% 
% pos_x = [0.5 0.5];
% pos_y = [0 1];
% line(pos_x,pos_y,'Color','green','LineStyle','--')
% 
% grid('on');
% xlabel(getString(message('stats:cdfplot:LabelX')));
% ylabel(getString(message('stats:cdfplot:LabelFx')));
% title({'Distribuição Empírica Acumulada do Score', [] });
% legend('Onda','Ruído','Distancia KS','Location','best');
% hold off;
% saveas(gcf,strcat(HOME,'/pesquisa/dados-4Khz-janela-',version,'/Kolmogorov–Smirnov'),'png');

% figure
% hold on
% histogram(A(1,:),100);
% histogram(B(1,:),100);
% title({'Distribuições empíricas do score'});
% legend({'Onda','Ruído'},'Location','best')
% xlabel('Score')
% ylabel('Frequência')
% hold off
% saveas(gcf,strcat(HOME,'/pesquisa/dados-4Khz-janela-',version,'/Histograma'),'png');