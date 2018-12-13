function pos = llegir()
fid = fopen("entrada1248.txt");
fitxer = fscanf(fid, '%s');
linies = split(fitxer, ';');
x = [];
y = [];
for i=1:length(linies)-1
    xy = split(linies(i), ',');
    x = [x;str2double(xy(1,1))];
    y = [y;str2double(xy(2,1))];
end
scatter(x,y,".");
fclose(fid);
pos = [x,y];
end