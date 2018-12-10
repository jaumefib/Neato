%close all;
figure
%% Posició del laser del Neato
Robot= [-50 -100 0 1;150 0 0 1;-50 100 0 1]'; % The Robot icon is a triangle
patch(Robot(1,:), Robot(2,:), 'b');

hold on;
%% Obtenció i tria dels punts
punts = llegir();
punts = clean(punts);

%% Cerca de cantonades
% Detecció de cantonades
c = cantonades(punts);
% Només mostrar els punts que formen un petit cluster de la cantonada
c = cluster(c);

%% Mostrar el mapa amb les cantonades marcades
%scatter(0,0,"g");

% Tots els punts
if length(punts) >= 1
    scatter(punts(:,1),punts(:,2),'b');
end
% Punts de les cantonades
if length(c) >= 1
    scatter(c(:,1),c(:,2),'r');
end
axis([-2000 2000 -2000 2000])
hold off;