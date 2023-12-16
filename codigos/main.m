function main(type,percent,window)
    HOME = getenv('HOME');
    path = strcat(HOME,'/data/',type,'-',int2str(percent),'%-',int2str(window),'.h5');
    [x, t] = getData(path);
   
    net = feedforwardnet(10,'traingda');
    net = configure(net,x,t);
    net.trainParam.epochs = 100000;
    net.trainParam.lr = 0.001;
    net.trainParam.min_grad = 1e-15;
    net.trainParam.max_fail = 10;
    net.layers{1}.transferFcn = 'logsig';
    net.layers{2}.transferFcn = 'logsig';

    [net] = train(net,x,t);
%     figure
%     hold on;
%     plotperform(tr);
%     hold off;
%     saveas(gcf,strcat(HOME,'/data/plotperform_',type,'_',int2str(percent),'%_',int2str(window)),'png');

    y = net(x);
    
    save(strcat(HOME,'/data/',type,'-',int2str(percent),'%-',int2str(window),'.mat'),'net')

    score = (y(1,:)-y(2,:))/2 + 0.5;

    contA = 1;
    contB = 1;

    A = zeros(1,length(score)/2);
    B = zeros(1,length(score)/2);

    for i=1:length(score)
       if t(1,i) == 1
           A(contA) = score(i);
           contA = contA + 1;
       else
           B(contB) = score(i);
           contB = contB + 1;
       end
    end

    figure
    hold on;
    [f_A,a] = ecdf(A);
    [f_B,b] = ecdf(B);

    minMax = linspace(min([a', b']),max([a', b']),length(a));
    minMax = round(minMax,4);
    minMax = unique(minMax);
    dist = -1;
    aa = round(a,4);
    bb = round(b,4);
    ia = 1;
    ib = 1;
    for i=1:length(minMax)
        findA = find(aa==minMax(i), 1);
        findB = find(bb==minMax(i), 1);
        temp = abs(f_A(findA) - f_B(findB));
        if (dist < temp)
            dist = temp;
            ia = findA;
            ib = findB;
        end
    end

    plot(a,f_A);
    plot(b,f_B);

    x1 = [a(ia) b(ib)];
    y1 = [f_B(ib) f_B(ib)-dist];
    pl = line(x1,y1);
    pl.Color = 'green';
    pl.LineStyle = '--';
    grid('on');
    xlabel(getString(message('stats:cdfplot:LabelX')));
    ylabel(getString(message('stats:cdfplot:LabelFx')));
    title({'Teste de Kolmogorov–Smirnov de Treinamento',['distancia do KS de ' num2str(dist) ' para ' type ' de ' int2str(percent) '% com janela de ' int2str(window)]});
    legend('Onda','Não Onda','Test Kolmogorov–Smirnov','Location','best');
    hold off;
    saveas(gcf,strcat(HOME,'/data/',type,'/',int2str(window),'/kolmogorov_smirnov_',int2str(percent),'%'),'png');

    figure
    hold on
    histogram(A(1,:),100);
    histogram(B(1,:),100);
    title({'Histograma de Treinamento',['rede treinada com ruido ' type ' de ' int2str(percent) '% com janela de ' int2str(window)]});
    legend({'onda','não onda'},'Location','northeast')
    xlabel('Score')
    ylabel('Quantidade')
    hold off
    saveas(gcf,strcat(HOME,'/data/',type,'/',int2str(window),'/histogram_train_',int2str(percent),'%'),'png');
end