% hinfo = hdf5info('dados/Horizons.h5');
% A = hdf5read(hinfo.GroupHierarchy.Groups(1).Datasets(3));
% B = hdf5read(hinfo.GroupHierarchy.Groups(2).Datasets(3));
% 
% tA = A(1,:);
% xA = A(2,:);
% yA = A(3,:);
% zA = A(4,:);
% 
% tB = B(1,:);
% xB = B(2,:);
% yB = B(3,:);
% zB = B(4,:);
% 
% t = zeros(length(tA),2);
% x = zeros(length(xA),2);
% y = zeros(length(yA),2);
% z = zeros(length(zA),2);
% 
% t(:,1) = tA;
% t(:,2) = tB;
% x(:,1) = xA;
% x(:,2) = xB;
% y(:,1) = yA;
% y(:,2) = yB;
% z(:,1) = zA;
% z(:,2) = zB;
% 
% figure
% plot(x,y);
% title('BBH0001 - Orbits');
% legend({'object 1','object 2'},'Location','best')
% xlabel('x')
% ylabel('y')
% 
% figure
% plot(t,x);
% title('BBH0001 - Orbits');
% legend({'object 1','object 2'},'Location','best')
% xlabel('t') 
% ylabel('x')
% 
% figure
% plot3(x,y,z);
% title('BBH0001 - Orbits');
% legend({'object 1','object 2'},'Location','best')
% xlabel('x') 
% ylabel('y')
% zlabel('z')
% 
% figure
% plot3(x,y,t);
% title('BBH0001 - Orbits');
% legend({'object 1','object 2'},'Location','best')
% xlabel('x') 
% ylabel('y')
% zlabel('t')
AA = 10;
isscalar(AA)
BB = AA(1,1);
isscalar(B)