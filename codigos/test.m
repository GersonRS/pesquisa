function test(type,percent,window)
    HOME = getenv('HOME');
    load(strcat(HOME,'/data/',type,'-',int2str(percent),'%-',int2str(window),'.mat'),'net');
    dataLigo = getDataLigo(strcat(HOME,'/data/ligo',int2str(window),'.h5'));

    resultLigo = sim(net,dataLigo);

    score_ligo = (resultLigo(1,:)-resultLigo(2,:))/2 + 0.5;

    figure
    hold on;
    histogram(score_ligo,100);
    title({'Histograma com dados Reais LIGO',['Rede treinada com ruido ' type ' de ' int2str(percent) '% com janela de ' int2str(window)]});
    legend('LIGO','Location','best')
    xlabel('Score')
    ylabel('Frequencia')
    hold off;
    saveas(gcf,strcat(HOME,'/data/validation/histogram_simmulation_',type,'_',int2str(percent),'%_',int2str(window)),'png');
    
    figure
    hold on;
    plot(score_ligo);
    title({'plot dos scores com dados Reais LIGO',['Rede treinada com ruido ' type ' de ' int2str(percent) '% com janela de ' int2str(window)]});
    legend('LIGO','Location','best')
    xlabel('Tempo')
    ylabel('Score')
    hold off;
    saveas(gcf,strcat(HOME,'/data/validation/plot_simmulation_',type,'_',int2str(percent),'%_',int2str(window)),'png');
end

