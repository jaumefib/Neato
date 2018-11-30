function xy = cluster(xy)
for i=1:1:length(xy)
    cont = 0;
    for j=1:1:length(xy)
        dist = sqrt((xy(i,1)-xy(j,1))^2 + (xy(i,2)-xy(j,2))^2);
        if dist < 500 && i ~= j && dist ~= 0
            cont = cont + 1;
        end
        %xy(i,:)
        %xy(j,:)
    end
    %xy(i,:), cont
    if cont < 1 % 4
        xy(i,:) = nan;
    end
end
end