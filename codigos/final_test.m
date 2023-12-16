HOME = getenv('HOME');
waves = {'GW150914', 'GW151012', 'GW151226', 'GW170104', 'GW170608', 'GW170729', 'GW170809', 'GW170814', 'GW170818', 'GW170823'};
for wave = waves
    ligo = char(wave);
    version = char("410");
    hinfo = hdf5info(strcat(HOME,'/pesquisa/dados-4Khz-janela-',version,'/',ligo,'.h5'));
    H1 = hdf5read(hinfo.GroupHierarchy.Datasets(1));
    L1 = hdf5read(hinfo.GroupHierarchy.Datasets(2));
    save(strcat(HOME,'/pesquisa/dados-4Khz-janela-',version,'/',ligo,'.mat'),'H1','L1')
end
% load(strcat(HOME,'/pesquisa/version_',version,'/rede','.mat'),'net');
% 
% resultLigo = sim(net,dataLigo);
% 
% score_ligo = (resultLigo(1,:)-resultLigo(2,:))/2 + 0.5;
% 
% moving = smooth(smooth(score_ligo,250),250);
% figure;
% hold on;
% plot(moving);
% hold off;
% 
% figure
% hold on;
% plot(score_ligo);
% title({'plot dos scores com dados Reais LIGO',['Rede testada com a ',ligo]});
% legend('LIGO','Location','best')
% xlabel('Tempo')
% ylabel('Score')
% hold off;
% % saveas(gcf,strcat(HOME,'/data/v1/plot_simmulation_',ligo),'png');