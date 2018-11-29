
% Inicialització de punts
%{
points = []
for i=0:10
    points = [points;i,10] 
end

for i=0:10
    points = [points;10,i] 
end

scatter(points(:,1),points(:,2))
%}
figure;

fid = fopen("vista_robot.txt");
fitxer = fscanf(fid, '%s');
linies = split(fitxer, ';')
x = [];
y = [];
for i=1:length(linies)-1
    xy = split(linies(i), ',');
    x = [x;str2double(xy(1,1))];
    y = [y;str2double(xy(2,1))];
end
scatter(x,y,".");
fclose(fid);
axis([-2000 2000 -2000 2000])
points = [x,y];

% Detecció de corners
cantonada = [];
xy = [];
w = 30 %30;
max_dist = 100000 %5000;
for i=1:1:length(points)-w
    dist = sqrt((points(i+w,1)-points(i,1))^2 + (points(i+w,2)-points(i,2))^2);
    if dist < max_dist
        ux = points(i+w,1) - points(i+w/2,1);
        uy = points(i+w,2) - points(i+w/2,2);
        vx = points(i+w/2,1) - points(i,1);
        vy = points(i+w/2,2) - points(i,2);
        pas2 = (ux*vx) + (uy*vy);
        pas3 = sqrt(ux^2 + uy^2) * sqrt(vx^2 + vy^2);
        pas1 = pas2/pas3;
        beta = acos(pas1)*(180/pi);
        if (beta > 80 && beta < 100) || (beta > 260 && beta < 280)
            xy = [xy; points(i+3,:)];
        end
    end
end

xy
hold on
scatter(0,0,"g")
if length(xy) >= 1
    scatter(xy(:,1),xy(:,2),'r')
end
